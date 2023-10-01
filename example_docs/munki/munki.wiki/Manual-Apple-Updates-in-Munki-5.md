The handling of Apple software updates that require a restart is the biggest change in Munki 5.

Apple's `softwareupdate` tool, which Munki uses to install Apple software updates, has become increasingly unreliable at the task of installing macOS updates and Security Updates. This mostly affects Macs with T2 chips, though it's not completely clear if the problems are limited to those models. Some of the observed issues include but are not limited to these:

* After an attempted install of a macOS update or Security Update, the Mac boots into "Boot Recovery Utility", requiring manual intervention to get the machine to start up in macOS.

* Installing/preparing the macOS update or Security Update hangs indefinitely.

These issues do not seem to occur if you use the System Preferences Software Update pane to install these updates.

In Munki 5, Munki will no longer attempt to install macOS updates or Security Updates for macOS Mojave or later. Managed Software Center will direct users to use the System Preferences Software Update pane to install these updates.

More specifically, on macOS Mojave and later, Munki will not install Apple software updates that require a restart. Other Apple software updates will be handled as they have been in previous Munki releases.

Here's an example of Managed Software Center displaying a set of updates including a macOS update:

![](https://github.com/munki/munki/wiki/images/munki5-1.png)

If the user clicks "Update All", he or she is presented with this alert, directing the user to install the macOS update using the System Preferences Software Update pane:

![](https://github.com/munki/munki/wiki/images/munki5-2.png)

If he or she clicks "Install now", Managed Software Center attempts to launch System Preferences and display the Software Update pane. It's up to the user to follow through and actually install any pending Apple updates. managedsoftwareupdate is also configured to install the remaining displayed updates after the Mac restarts.

This, of course, requires that the user is actually able to install the updates. By default in recent macOS releases, even non-admins can install Apple updates using the Software Update pane, but this ability can be restricted with configuration profiles. See [softwareupdate and configuration profile notes](softwareupdate-and-configuration-profile-notes) for additional information.

If the user is unable to install the updates (because he or she is not an admin user, and a configuration profile that restrict these installs is present), a different alert is presented:

![](https://github.com/munki/munki/wiki/images/munki5-3.png)

If the user clicks "Skip these updates", any Apple updates that require a restart are removed from the list of pending updates:

![](https://github.com/munki/munki/wiki/images/munki5-4.png)

The user can then use the normal/previous methods of interacting with Managed Software Center to install these remaining updates.