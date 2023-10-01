### Using CodeSignatureVerification in your recipe

The [CodeSignatureVerifier](https://github.com/autopkg/autopkg/wiki/Processor-CodeSignatureVerifier) processor was added to allow signature verification for both:

1. Installer packages (.pkg or .mpkg).

2. Application bundles (.app). This option is necessary since not all software is supplied as packages. Instead, software is commonly released for download 'bare' at the root of a zip archive. CodeSignatureVerifier can look inside a DMG mount, but zip's must use the [Unarchiver](https://github.com/autopkg/autopkg/wiki/Processor-Unarchiver) processor first.

Take into account the fact that both the computer running autopkg and the one that generates the required configuration settings should have the default `spctl` settings, meaning Gatekeeper allows apps from the App Store and those signed with an Apple-recognized Developer ID. 
#### Adding Application bundle (.app) verification to your recipe

For drag-drop apps downloaded as zip archives, you'd run `codesign --display -r- --deep -v /path/to/.appBundle` and paste the entire output of the `designated` key into [the format below](https://github.com/autopkg/hjuutilainen-recipes/blob/9a064b9e84771bfa2cea3e47411d3191ac39774e/SmileOnMyMac/TextExpander.download.recipe#L33-L60) (with the precursor step of adding the Unarchiver processor as necessary). Make sure that there is `Sealed Resources version=2` in the output, to verify that the developer signed it with the second version of Apple's signature format, as that is what the processor is strict about when checking.

Also notice the processors placement after an `EndOfCheckPhase` step below, so that folks who run autopkg in 'check-only' mode won't needlessly unarchive the app and verify its contents every time the recipe runs. 

```
<dict>
    <key>Processor</key>
    <string>EndOfCheckPhase</string>
</dict>
<dict>
    <key>Processor</key>
    <string>Unarchiver</string>
    <key>Arguments</key>
    <dict>
        <key>archive_path</key>
        <string>%pathname%</string>
        <key>destination_path</key>
        <string>%RECIPE_CACHE_DIR%/%NAME%</string>
        <key>purge_destination</key>
        <true/>
    </dict>
</dict>
<dict>
    <key>Processor</key>
    <string>CodeSignatureVerifier</string>
    <key>Arguments</key>
    <dict>
        <key>input_path</key>
        <string>%RECIPE_CACHE_DIR%/%NAME%/TextExpander.app</string>
        <key>requirement</key>
        <string>anchor apple generic and identifier "com.smileonmymac.textexpander" and (certificate leaf[field.1.2.840.113635.100.6.1.9] /* exists */ or certificate 1[field.1.2.840.113635.100.6.2.6] /* exists */ and certificate leaf[field.1.2.840.113635.100.6.1.13] /* exists */ and certificate leaf[subject.OU] = "7PKJ6G4DXL")</string>
    </dict>
</dict>
```

Please note that even getting valid output from one part of an application does not guarantee all resources that are part of it will pass verification.

#### Adding package installer (.pkg) verification to your recipe
To check for a valid signature from a _package_, run this command: `pkgutil --check-signature /path/to/pkg` and fit it into [this format](https://github.com/autopkg/recipes/blob/master/MSOfficeUpdates/MSOffice2011Updates.download.recipe#L51-L65) (assuming, as in the example, it's pulled down from the vendor in a DMG, and therefore the `pathname` can essentially point to its mount):

```
<dict>   
    <key>Processor</key>   
    <string>CodeSignatureVerifier</string>   
    <key>Arguments</key>   
    <dict>   
        <key>input_path</key>   
        <string>%pathname%/Office*.*pkg</string>
        <key>expected_authority_names</key>
        <array>
            <string>Developer ID Installer: Microsoft Corporation (UBF8T346G9)</string>
            <string>Developer ID Certification Authority</string>
            <string>Apple Root CA</string>
        </array>
    </dict>
</dict>
```

### How Application bundle (.app) verification works

**CodeSignatureVerifier key:** `requirement`

**Apple binary utility used:** `codesign`

**What Autopkg does:**

1. Verifies the developer ID cert was issued by Apple.

2. Commonly, also verifies a specific developer ID by checking the value in the OU field. This prevents an attacker from tricking the user into trusting it because it's signed by another developer's cert instead of the actual expected author.

Code signature verification for .app bundles uses the `codesign` tool, which first uses 'deep' verification to ensure all resources that make up the app are signed with [version 2 signatures](https://indiestack.com/2014/10/gatekeepers-opaque-whitelist/).  This does not guarantee that trust will be evaluated, as no system policies are run within the tool itself to consult a chain of trust. (The requirement itself could be bypassed along with Gatekeeper, although it should cause failures instead of false-positives.) Then it looks at the provided authority names to make sure they are as expected.

You can use `codesign` to evaluate self-signed signatures given a proper requirement string, which is what the CodeSignatureVerifier processor does when fed an app bundle. If there's no requirement string, CodeSignatureVerifier verifies the bundle against it's own designated requirement (which would allow it to succeed for specific Developer ID-signed apps with no OU designation). In most cases the requirement string should be copied by a recipe author from the apps designated requirement. Let's break down one of these requirement strings:

`anchor apple generic and identifier "com.hjuutilainen.MunkiAdmin" and (certificate leaf[field.1.2.840.113635.100.6.1.9] /* exists */ or certificate 1[field.1.2.840.113635.100.6.2.6] /* exists */ and certificate leaf[ field.1.2.840.113635.100.6.1.13] /* exists */ and certificate leaf[subject.OU] = "8XXWJ76X9Y")`


- `anchor apple generic` means that the code must be signed by Apple, including code signed using a signing certificate issued by Apple to other developers.
- `identifier "com.hjuutilainen.MunkiAdmin"` means that the unique identifier string embedded in the code signature is exactly equal to "com.hjuutilainen.MunkiAdmin".
- `certificate leaf[field.1.2.840.113635.100.6.1.9]` means that the leaf (the private Developer ID certificate) must have a particular field present.
- `certificate leaf[subject.OU] = "8XXWJ76X9Y"` means that the leaf must have a specific subject value of "8XXWJ76X9Y" in the Organizational Unit field.

### How installer package (.pkg) verification works

**CodeSignatureVerifier key:** `expected_authority_names`

**Apple binary utility used:** `pkgutil` with the `--check-signature` flag

**What Autopkg does:**

1. Checks that the package is signed by a root cert which is trusted by the System root store.

2. Checks the `expected_authority_names` array to make sure that the specific issuers we expect were used.

Installer package verification uses the `pkgutil` tool, which verifies that the item hasn't been tampered with and if it is trusted by the system as correctly signed with Apple at the root of trust. This check is done first and it must pass. Only if the package is valid and trusted with Apple as the root is the expected_authority_names array used and matched against the strings we'd get back after running pkgutil.

### Disabling CodeSignatureVerification in an existing recipe

It is possible to disable Code Signature Verification in an override or with the command line [`-k/--key`](https://github.com/autopkg/autopkg/wiki/Recipe-Overrides#command-line-the--k--key-option) option. If you want to do this on every run, create an override for the recipe in question and add the following key pair in the `Input` stanza:

```
        <key>DISABLE_CODE_SIGNATURE_VERIFICATION</key>
        <string>True</string>
```

The value listed as "True" in this example can be any non-empty value.

If you only want to disable the CodeSignatureVerification processor part for a single run, you can specify that option like this:

```
autopkg run -k DISABLE_CODE_SIGNATURE_VERIFICATION=1 [recipename]`
```
