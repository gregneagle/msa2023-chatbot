[make_munki_mpkg.sh](https://github.com/munki/munki/blob/main/code/tools/make_munki_mpkg.sh) is a script included in `/munki/code/tools/` to compile Munki from source.

When running `make_munki_mpkg.sh`, a number of flags are available for different options.

```
SYNOPSIS
     % sh make_munki_mpkg.sh [-i id] [-r root] [-o dir] [-c package] [-s cert]

OPTIONS
    -i id       Specify the base package bundle ID
    -r root     Specify the Munki source root
    -o dir      Specify the output directory
    -n orgname  Specify the name of the organization
    -p          Build Python.framework even if one exists
    -B          Include a package that sets Munki's bootstrap mode
    -m          Build the package in a manner suitable for install via MDM;
                specifically, attempt to start all the launchd agents and
                daemons without requiring a restart. Such a package is not
                suited for upgrade installs or install via Munki itself.
    -c plist    Build a configuration package using the preferences defined in a
                plist file.
    -R          Include a pkg to install Rosetta2 on ARM-based hardware.
    -s cert_cn  Sign distribution package with a Developer ID Installer
                certificate from keychain. Provide the certificate's Common
                Name. Ex: "Developer ID Installer: Munki (U8PN57A5N2)"
    -S cert_cn  Sign apps with a Developer ID Application certificated from
                keychain. Provide the certificate's Common Name.
                Ex: "Developer ID Application: Munki (U8PN57A5N2)"
```