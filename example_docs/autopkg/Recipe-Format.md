## Overview

An AutoPkg recipe is a file that contains several sections describing a sequence of tasks that can be used to automate tasks involving retrieval, patching, building, packaging, and/or importing some piece of software. These files can be in either the **XML plist** format or **yaml** format. (See examples below.)

### Recipe file extensions

- **plist**: `.recipe`, `.recipe.plist`

- **yaml**: `.recipe.yaml`
  - `.recipe.yml` is NOT supported

### Top-level keys

<table>
  <tr><th>Key</th><th>Type</th><th>Description</th></tr>
  <tr><td>Description</td><td>String</td><td>(Optional, but highly encouraged) A helpful description of what the recipe does, and any application-specific values the admin may wish to override.</td></tr>
  <tr><td>Identifier</td><td>String</td><td>A unique string identifying this recipe. A suggested format for the identifier is a reverse-domain string followed by the recipe type and product name. For example, com.github.autopkg.munki.AdobeAIR is an identifier for the AdobeAir.munki recipe in the repo maintained at github.com/autopkg/recipes.</td></tr>
<tr><td>Input</td><td>Dict</td><td>A set of variables that the admin can override without needing to directly modify any parameters or logic of the recipe itself.</td></tr>
<tr><td>MinimumVersion</td><td>String</td><td>(Optional) Minimum version of autopkg required to run this recipe. For .recipe.yaml files, this should be 2.3.</td></tr>
<tr><td>ParentRecipe</td><td>String</td><td>(Optional) If this recipe inherits Input and Process from another recipe, this exists and is the Identifier of the parent recipe.</td></tr>
<tr><td>Process</td><td>Array of dicts</td><td>A sequence of processors used to perform the recipe, along with their parameters.</td></tr>
</table>

### Variables

The recipe processing chain maintains an "environment" of variables and their values, which can be thought of similar to shell environment variables, and which are present for the duration of that recipe's execution. Certain variables are present before the processing starts, for example all values in the `Input` section, and application preferences read from AutoPkg's defaults domain.

Each processor has read/write access to the entire environment, and may require certain input variables to perform its task. Often it will set at least one output variable on completion, and these are saved back to the environment and made available to the next processor in the chain. A list of conventional `Input` variables is available on the [[Input Variables]] page.

### String substitution

Any text enclosed in percent-signs (ie. `%RELEASE%`) will be substituted with the data present for that key name in the `Input` section. This is how processor-specific variables can be controlled, for example:

- a specific version number to fetch for an application's own "update feed info" provider
- certain values substituted directly into URLs (for example, an application with multiple sparkle feeds for beta and normal releases: `https://some.app/sparkle/%RELEASE%/feed.xml`

## Example 1: Firefox.download

Here's the recipe plist for the Firefox.download recipe:

**Firefox.download.recipe**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Description</key>
    <string>Download recipe for Firefox. Finds and downloads a Firefox release disk image.
Some useful values for RELEASE are: 'latest', 'esr-latest', 'beta-latest'.
LOCALE controls the language localization to be downloaded.
Examples include 'en-US', 'de', 'sv-SE', and 'zh-TW'
See the following URLs for more info:
    http://ftp.mozilla.org/pub/firefox/releases/latest/README.txt
    http://ftp.mozilla.org/pub/firefox/releases/latest-esr/README.txt
    http://ftp.mozilla.org/pub/firefox/releases/latest-beta/README.txt</string>
    <key>Identifier</key>
    <string>com.github.autopkg.download.firefox-rc-en_US</string>
    <key>Input</key>
    <dict>
        <key>RELEASE</key>
        <string>latest</string>
        <key>LOCALE</key>
        <string>en-US</string>
        <key>NAME</key>
        <string>Firefox</string>
        <key>DISABLE_CODE_SIGNATURE_VERIFICATION</key>
        <false />
    </dict>
    <key>MinimumVersion</key>
    <string>2.0</string>
    <key>Process</key>
    <array>
        <dict>
            <key>Arguments</key>
            <dict>
                <key>product_name</key>
                <string>firefox</string>
                <key>release</key>
                <string>%RELEASE%</string>
                <key>locale</key>
                <string>%LOCALE%</string>
            </dict>
            <key>Processor</key>
            <string>MozillaURLProvider</string>
        </dict>
        <dict>
            <key>Arguments</key>
            <dict>
                <key>filename</key>
                <string>%NAME%.dmg</string>
            </dict>
            <key>Processor</key>
            <string>URLDownloader</string>
        </dict>
        <dict>
            <key>Processor</key>
            <string>EndOfCheckPhase</string>
        </dict>
        <dict>
            <key>Processor</key>
            <string>CodeSignatureVerifier</string>
            <key>Arguments</key>
            <dict>
                <key>comment</key>
                <string>Use wildcard matching for the app so it will also match FirefoxDeveloperEdition.app and FirefoxNightly.app</string>
                <key>input_path</key>
                <string>%pathname%/Firefox*.app</string>
                <key>requirement</key>
                <string>anchor apple generic and certificate leaf[field.1.2.840.113635.100.6.1.9] /* exists */ or anchor apple generic and certificate 1[field.1.2.840.113635.100.6.2.6] /* exists */ and certificate leaf[field.1.2.840.113635.100.6.1.13] /* exists */ and certificate leaf[subject.OU] = "43AQ936H96"</string>
            </dict>
        </dict>
    </array>
</dict>
</plist>
```

### Input

Under `Input`, there are certain conventional variables present in all recipes, such as `NAME` (more on these in a separate page). Others are recipe-specific (or in this case, Mozilla-specific): `RELEASE` and `LOCALE`. The latter two correspond to the release branch and language version, respectively. The purpose of and possible values for these parameters should be described in the `Description` key for the recipe.

### Process

Let's examine the `Process` section. Each item in the array should contain two keys: `Processor`, the name of a processor, and `Arguments`, values for any arguments supported by the processor.

The list of processors available can be found in `/Library/AutoPkg/autopkglib`, each a separate file ending in `.py`, or via:

`autopkg list-processors`

When a processor is only useful for a specific recipe (or set of related recipes), it can instead be located in the same directory as the recipe. This allows recipe creators to implement new processors as needed.

You can get basic information on a processor (a description and expected input and output variables):

`autopkg processor-info PROCESSORNAME`

If the processor is not one of the core processors, but is instead a processor included with a specific recipe (or set of related recipes), provide a recipe name or identifier as well:

`autopkg processor-info MozillaURLProvider --recipe Firefox.download`

See [Processor Locations](https://github.com/autopkg/autopkg/wiki/Processor-Locations) for more details on how AutoPkg can locate processors.

We'll look at an example below:

#### MozillaURLProvider

##### Description
Provides URL to the latest Firefox release.

##### Input variables

- **release**:
    - **required**: False
    - **description**: Which release to download. Examples: 'latest', 'esr-latest', 'beta-latest'. Defaults to 'latest'
- **locale**:
    - **required**: False
    - **description**: Which localization to download, default is 'en_US'.
- **product\_name**:
    - **required**: True
    - **description**: Product to fetch URL for. One of 'firefox', 'thunderbird'.
- **base_url**:
    - **required**: False
    - **description**: Default is  'https://download.mozilla.org/?product=%s-%s&os=osx&lang=%s.

##### Output variables

- **url**:
    - description: URL to the latest Mozilla product release.

Here, **product_name** is the only input variable that's required, and the rest are optional. `url` is the variable that's expected to be set by a processor that provides a download URL, which the `URLDownloader` processor will look to use by default.

### URLDownloader

This processor downloads a url to the recipe's cache folder and also saves some metadata given by the webserver's response header: `Content-Length` and `ETag`, if either are available. If the recipe is run a second time, these are used to compare our cached copy with what's currently available at the download URL. This means it's possible to run the recipe many times and know that it will not re-download the file every time, but it will check every time.

### EndOfCheckPhase

This is a dummy processor that is used only by `autopkg` for the purposes of stopping the recipe processing if the `--check` option was given. This is to allow `autopkg` to be run on a schedule and have it not do a full processing run every time, if it deems it not necessary. The assumption here is that if we've cached it, we've already processed the rest of the recipe, which is typically any final post-processing steps and importing it into a repository. Since this step is near the end of this particular download recipe, it would only skip the CodeSignatureVerifier processor, but when a download recipe is used as the basis for a recipe that imports into Munki or builds a package, this step would become more useful.

### CodeSignatureVerifier

As a part of ensuring that the product we have downloaded is what we expect and has not been altered, a `CodeSignatureVerifier` processor is added to almost every modern download recipe. The [Using CodeSignatureVerification page in this wiki](https://github.com/autopkg/autopkg/wiki/Using-CodeSignatureVerification) goes into detail on how to properly implement this in your own download recipes.

## Example 2: Firefox.munki

Firefox.munki builds upon Firefox.download.

**Firefox.munki.recipe**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Description</key>
    <string>Downloads Firefox disk image and imports into Munki.
Some useful values for RELEASE are: 'latest', 'esr-latest', 'beta-latest'.
LOCALE controls the language localization to be downloaded.
Examples include 'en-US', 'de', 'sv-SE', and 'zh-TW'
See the following URLs for more info:
    http://ftp.mozilla.org/pub/firefox/releases/latest/README.txt
    http://ftp.mozilla.org/pub/firefox/releases/latest-esr/README.txt
    http://ftp.mozilla.org/pub/firefox/releases/latest-beta/README.txt</string>
    <key>Identifier</key>
    <string>com.github.autopkg.munki.firefox-rc-en_US</string>
    <key>Input</key>
    <dict>
        <key>MUNKI_REPO_SUBDIR</key>
        <string>apps/firefox</string>
        <key>NAME</key>
        <string>Firefox</string>
        <key>pkginfo</key>
        <dict>
            <key>catalogs</key>
            <array>
                <string>testing</string>
            </array>
            <key>description</key>
            <string>Mozilla Firefox is a free and open source web browser.</string>
            <key>display_name</key>
            <string>Mozilla Firefox</string>
            <key>name</key>
            <string>%NAME%</string>
            <key>unattended_install</key>
            <true/>
        </dict>
    </dict>
    <key>MinimumVersion</key>
    <string>0.2.0</string>
    <key>ParentRecipe</key>
    <string>com.github.autopkg.download.firefox-rc-en_US</string>
    <key>Process</key>
    <array>
        <dict>
            <key>Arguments</key>
            <dict>
                <key>pkg_path</key>
                <string>%pathname%</string>
                <key>repo_subdirectory</key>
                <string>%MUNKI_REPO_SUBDIR%</string>
            </dict>
            <key>Processor</key>
            <string>MunkiImporter</string>
        </dict>
    </array>
</dict>
</plist>
```

This introduces a new top-level key:

### ParentRecipe

Since this recipe builds upon Firefox.download, rather than duplicating it here, we use it instead. The ParentRecipe for Firefox.munki (identifier: com.github.autopkg.munki.firefox-rc-en_US) is Firefox.download (com.github.autopkg.download.firefox-rc-en_US). Our Input values in this child recipe will replace or add to those for Firefox.download, and any Process steps will be added to the end of the Process for Firefox.download.

Let's look at **Input** and **Process** to understand how these modify the parent recipe.

### Input

**MUNKI_REPO_SUBDIR** is added to the Input dictionary; it specifies the subdirectory of the Munki repo in which to import the item; this is equivalent to the the `--subdirectory` option to the `makepkginfo` and `munkiimport` commands.

**pkginfo** is an input variable used by the MunkiImporter processor. We define it in the Input dictionary so it can by overridden by others who might want to customize some elements.

### Process

All of the steps of the parent recipe are performed first: **MozillaURLProvider** finds the URL to the latest version of Firefox, and **URLDownloader** downloads it. One of the output variables of the **URLDownloader** step is `pathname`, which is the path to the downloaded item. This variable is used in the **CodeSignatureVerifier** step via [string substitution](#string-substitution) to help locate the app whose code signature is to be verified.

The Firefox.munki recipe defines one new step, which uses the **MunkiImporter** processor. Let's look at the information for this processor:

```sh
% autopkg processor-info MunkiImporter
Description: Imports a pkg or dmg to the Munki repo.
Input variables:
   MUNKI_REPO:
     description: Path to a mounted Munki repo.
     required: True
   MUNKI_REPO_PLUGIN:
     description: Munki repo plugin. Defaults to FileRepo. Munki must be installed and available  at MUNKILIB_DIR if a plugin other than FileRepo is specified.
     required: False
     default: FileRepo
   MUNKILIB_DIR:
     description: Directory path that contains munkilib. Defaults to /usr/local/munki
     required: False
     default: /usr/local/munki
   force_munki_repo_lib:
     description: When True, munki code libraries will be utilized when the FileRepo plugin is used. Munki must be installed and available at MUNKILIB_DIR
     required: False
     default: False
   pkg_path:
     required: True
     description: Path to a pkg or dmg to import.
   munkiimport_pkgname:
     required: False
     description: Corresponds to --pkgname option to munkiimport.
   munkiimport_appname:
     required: False
     description: Corresponds to --appname option to munkiimport.
   repo_subdirectory:
     required: False
     description: The subdirectory under pkgs to which the item will be copied, and under pkgsinfo where the pkginfo will be created.
   pkginfo:
     required: False
     description: Dictionary of pkginfo keys to copy to generated pkginfo.
   extract_icon:
     required: False
     description: If not empty, attempt to extract and import an icon from the installer item. Munki must be installed and available at MUNKILIB_DIR.
   force_munkiimport:
     required: False
     description: If not False or Null, causes the pkg/dmg to be imported even if there is a matching pkg already in the repo.
   additional_makepkginfo_options:
     required: False
     description: Array of additional command-line options that will be inserted when calling 'makepkginfo'.
   version_comparison_key:
     required: False
     description: String to set 'version_comparison_key' for any generated installs items.
   uninstaller_pkg_path:
     required: False
     description: Path to an uninstaller pkg, supported for Adobe installer_type items.
   MUNKI_PKGINFO_FILE_EXTENSION:
     description: Extension for output pkginfo files. Default is 'plist'.
     required: False
   metadata_additions:
     description: A dictionary that will be merged with the pkginfo _metadata.  Unique keys will be added, but overlapping keys will replace existing values.
     required: False
Output variables:
   pkginfo_repo_path:
     description: The repo path where the pkginfo was written. Empty if item not imported.
   pkg_repo_path:
     description: The repo path where the pkg was written. Empty if item not imported.
   munki_info:
     description: The pkginfo property list. Empty if item not imported.
   munki_repo_changed:
     description: True if item was imported.
   munki_importer_summary_result:
     description: Description of interesting results.
```

The `pkg_path` and `repo_subdirectory` input variables are in the step's Arguments array, both defined via variable [string substitution](#string-substitution). There's one more input variable that is used; it was defined in the **Input** dictionary: `pkginfo`. **MunkiImporter** then will import our download of Firefox.dmg to apps/firefox in the Munki repo. The following changes/additions will be made to the generated pkginfo:

```xml
<dict>
    <key>catalogs</key>
    <array>
        <string>testing</string>
    </array>
    <key>description</key>
    <string>Mozilla Firefox is a free and open source web browser.</string>
    <key>display_name</key>
    <string>Mozilla Firefox</string>
    <key>name</key>
    <string>Firefox</string>
    <key>unattended_install</key>
    <true/>
</dict>
```
