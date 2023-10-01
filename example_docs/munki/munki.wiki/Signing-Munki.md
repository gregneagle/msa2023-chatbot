### Signing Munki Packages 

In some workflows it's helpful or even required to have signed packages. The official Munki packages are not signed. If you need them to be signed, you need to get a "Developer ID Installer" signing certificate from Apple and import it into a keychain.  
You can then use that signing identity, together with the `productsign` tool, to sign the munkitools package:

```
% productsign --sign "Developer ID Installer: Some Developer (12ABCDE3FG)" ~/Downloads/munkitools-3.2.0.3476.pkg ~/Downloads/munkitools_signed-3.2.0.3476.pkg 
productsign: using timestamp authority for signature
productsign: signing product with identity "Developer ID Installer: Some Developer (12ABCDE3FG)" from keychain /Users/sdeveloper/Library/Keychains/login.keychain-db
productsign: adding certificate "Developer ID Certification Authority"
productsign: adding certificate "Apple Root CA"
productsign: Wrote signed product archive to /Users/sdeveloper/Downloads/munkitools_signed-3.2.0.3476.pkg
```

Some information about Apple Developer IDs can be found here:  
https://developer.apple.com/support/developer-id/

You may also sign packages you build yourself using the scripts in code/tools, either using the above process, or by using the `-s` flag to the `make_munki_mpkg*` scripts with the same Developer ID Installer string as you would use with `productsign`.

### Signing Munki Applications 

Munki includes several applications: Managed Software Center.app, MunkiStatus.app, and munki-notifier.app. When [building from source](https://github.com/munki/munki/wiki/Building-Munki-packages), as of [this commit](https://github.com/munki/munki/blob/11ec1535a15e4d42262c4a3aa14cd2053e311d59/code/tools/make_munki_mpkg.sh), if you have a Developer ID Application certificate, you can use the `-S` flag to sign the component apps. (Note that Developer ID Application certificates are _different_ from Developer ID Installer certificates and cannot be used interchangeably.)

`./code/tools/make_munki_mpkg_from_git.sh -S "Developer ID Application: Some Developer (12ABCDE3FG)" -s "Developer ID Installer: Some Developer (12ABCDE3FG)"`

Signed apps are allowed (as of macOS Mojave) to display notifications as alerts by default. Unsigned apps may only display banner-style alerts by default.

### Signing and notarizing Munki Applications
LifeUnexpected has created 2 scripts that lets you package, sign and notarize munkitools.pkg.
[Notarization scripts](https://github.com/lifeunexpected/Scripts)