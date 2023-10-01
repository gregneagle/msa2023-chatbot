Munki 5 is a major new release of the Munki tools.  
You can find it here: https://github.com/munki/munki/releases

The most important change in Munki 5 is [how it handles Apple software updates that require a restart](manual-apple-updates-in-munki-5) on macOS 10.14 and above.

Munki 5 is supported on macOS 10.10 through macOS 10.15.

Like Munki 4, Munki 5 includes its own Python 3 interpreter by default, and is not dependent on Apple's included Python. See [[About Munki's Embedded Python]] and [[Customizing Python for Munki]] for more information on Munki's Python interpreter.

## More information:

* [Manual Apple Updates](manual-apple-updates-in-Munki-5)
* [force_install_after_date for Apple Updates](force_install_after_date-for-Apple-Updates-in-munki-5)
* [Additional update encouragement](additional-update-encouragement-in-munki-5)
* [Aggressive update notifications](aggressive-update-notifications-in-munki-5)
* [AggressiveUpdateNotificationDays preference](aggressiveupdatenotificationdays-preference)
* [[Additional Munki 5 changes]]
* [Configuration profile notes](softwareupdate-and-configuration-profile-notes)
* [Major macOS upgrade notes](major-macos-upgrade-notes)
* [[Upgrading to Munki 5]]
