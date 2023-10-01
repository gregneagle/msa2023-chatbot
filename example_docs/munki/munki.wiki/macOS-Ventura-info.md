### Munki tools version
Munki 5.7.2 or later is recommended for macOS Ventura, but Munki 6.0 or later is recommended even more.

Releases of Munki are available here: https://github.com/munki/munki/releases

#### Known issues
Munki 5.x cannot install/upgrade macOS on Apple silicon. This includes upgrades from Big Sur to Monterey.  
Munki 6 adds support for macOS upgrades on Apple silicon. See [this](Staging-macOS-Installers) for more info.

#### Ventura App Management "Privacy" Protection
macOS Ventura adds yet another new "Privacy" protection; "App Management". This feature can interfere with Munki's ability to install and update software. With Munki 6.3 and later, it is recommended to use MDM to install a PPPC/TCC profile granting either App Management or Full Disk Access rights to `/usr/local/munki/managedsoftwareupdate`. It's best if `/usr/local/munki/managedsoftwareupdate` is signed by a Developer ID. (If you don't sign the tool, you'll need to update your PPPC/TCC profile every time there's a new release of Munki.) Releases of Munki signed by MacAdmins Open Source are available here: https://github.com/macadmins/munki-builds/releases . Of course you can build and sign Munki with your own identity. See [Building Munki Packages](Building-Munki-packages) for more info.

#### Limitations
Due to Apple changes in the `profiles` command, Munki can no longer install configuration profiles on macOS Big Sur or later. Apple's recommendation is to use MDM to install all configuration profiles.

Munki 5.2 and later have a partial substitute for configuration profile installation on Big Sur or later that might help during your transition: [[Configuration Profile Emulation]]. Use this only as you transition to MDM delivery of profiles; this feature is likely to break and/or be removed in the future.
