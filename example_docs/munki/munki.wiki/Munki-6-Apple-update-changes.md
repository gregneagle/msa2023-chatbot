### Details

Munki 6 contains some changes to the handling of Apple software updates. Specifically, on Intel, Munki no longer attempts to download updates that require a restart on macOS Mojave and above (this is generally minor OS updates or security updates). Due to bugs in `/usr/sbin/softwareupdate`, softwareupdate seems to sometimes hang (or at least never completes/returns) when downloading these updates. These updates are the ones that Munki does not attempt to install anyway; these are the same updates that cause Managed Software Center to open the System Preferences/Settings Software Updates pane/view so the user can manually install them.

(Behavior on Apple silicon is unchanged: Munki does not attempt to download or install _any_ Apple updates, instead prompting the user to install them using the System Preferences/Settings Software Updates pane/view.)

See https://github.com/munki/munki/issues/1124 for additional details.