Since Munki 5 no longer uses `softwareupdate` to install Apple updates that require a restart on macOS Mojave and later, any Apple update metadata-provided `force_install_after_date` info will be ignored on macOS Mojave and later.

See [Pkginfo for Apple Software Updates](Pkginfo-For-Apple-Software-Updates) for more information on Munki's support for additional metadata for Apple updates.

Consider using [Unattended Apple Updates](Apple-Software-Updates-With-Munki#unattended-apple-updates) to have Munki install many Apple software updates (those that do not require a restart) without user involvement.