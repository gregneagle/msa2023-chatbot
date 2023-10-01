### Munki tools version
Munki 5.6 or later is recommended for macOS Monterey.

Releases of Munki 5.6 and later are available here: https://github.com/munki/munki/releases

#### Known issues
Munki 5 cannot install/upgrade macOS on Apple silicon. This includes upgrades from Big Sur to Monterey.  
Munki 6 adds support for macOS upgrades on Apple silicon. See [this](Staging-macOS-Installers) for more info.

#### Limitations
Due to changes in the `profiles` command, Munki cannot install configuration profiles on macOS Big Sur or macOS Monterey. Apple's recommendation is to use MDM to install all configuration profiles.

Munki 5.2 and later have a partial substitute for configuration profile installation on Big Sur that might help during your transition: [[Configuration Profile Emulation]]

