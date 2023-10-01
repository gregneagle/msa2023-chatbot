# Introduction and Background
Munki has four LaunchDaemons which support functions that require root privileges, and three LaunchAgents for all things visible in the GUI. In this document we will break down all seven of those bundled files and describe how they operate. `launchd` jobs are similar to a hybrid bewteen cron jobs and init scripts or scheduled tasks; they wrap processes. More background on launchd itself can be found [here](https://developer.apple.com/library/mac/technotes/tn2083/_index.html) (Apple's canonical overview, somewhat out of date as of Yosemite), in the [man](https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man8/launchd.8.html#//apple_ref/doc/man/8/launchd) [pages](https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man5/launchd.plist.5.html#//apple_ref/doc/man/5/launchd.plist), and on third party websites for utilities like [Lingon](https://www.peterborgapps.com/lingon/) and [LaunchControl](http://launchd.info).

## Stopping Munki from Running
The most common task one may be trying to accomplish when consulting this document is how to disable the (roughly) hourly background checks that Munki makes. [`launchctl`](https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man1/launchctl.1.html) is the tool which manipulates launchd jobs, and since that particular task is in the root context, you can disable it (if you have rights to sudo on the local machine) with `sudo /bin/launchctl unload -w /Library/LaunchDaemons/com.googlecode.munki.managedsoftwareupdate-check.plist`
The -w flag is optional, but including it means Munki won't run in the background even after a reboot.

### Notes Regarding Hosting / Naming
A general thing to note is that the naming of the files and their associated job labels reflect the previous hosting of the Munki project on Google Code, but it is now hosted solely on [GitHub](https://github.com/munki/munki). Likewise, you will see references to a 'managedsoftwareupdate' tool, which is the primary command-line complement of the Managed Software Center application.

---
# LaunchDaemons

##### `/Library/LaunchDaemons/com.googlecode.munki.managedsoftwareupdate-check.plist`
This job controls the ongoing schedule of background checks that Munki makes, and uses the bundled [`supervisor`](https://github.com/munki/munki/blob/master/code/client/supervisor) utility to perform two functions: First, it makes sure that if the Munki check somehow does not exit, or otherwise hangs indefinitely, it will be cleanly killed after 12 hours (43200 seconds). Second, it adds a delay of up to 3600 seconds (or 60 minutes) before actually triggering an 'auto' run of the managedsoftwareupdate tool. 

To explain and describe what that auto run actually performs, it would check for changes to the catalogs for any manifests that the client in question consults, and performs downloads if new actions are deemed necessary. It can also subsequently perform installations if items are designated as unattended (and no [blocking applications](https://github.com/munki/munki/wiki/Blocking-Applications) are encountered), and also could optionally check for Apple updates as well.


The SetCalendarInterval launchd job key is specified to have this job triggered at ten past each hour, at which point the supervisor utility-generated random delay actually dictates when the run is performed.

---
##### `/Library/LaunchDaemons/com.googlecode.munki.managedsoftwareupdate-install.plist`
When the client running Managed Software Center.app has cached updates that require user notification, or the end user has selected an item they wish to install from the offered Optional Installs, the mechanism that allows the app to run as the root user so it may perform system-wide actions is controlled by the managedsoftwareupdate-install launchdaemon. It checks for the existence of a trigger file at `/private/tmp/.com.googlecode.munki.managedinstall.launchd`, at which point the previously described `supervisor` utility runs `managedsoftwareupdate` with the `--installwithnologout` option. This is also 'wired-up' to the 'Install' button found under the Updates tab when there are waiting updates already queued or otherwise actions ready to be performed.

---

##### `/Library/LaunchDaemons/com.googlecode.munki.managedsoftwareupdate-manualcheck.plist`
Similar to the above, a trigger file `/private/tmp/.com.googlecode.munki.updatecheck.launchd` can be placed by the Managed Software Center app to perform an on-demand check in with the configured Munki server for updates to the clients manifest. Installations will not be performed, but otherwise the 'Check Again' button under the Updates tab can initiate this functionality until its state changes to 'Install'.

---
##### `/Library/LaunchDaemons/com.googlecode.munki.logouthelper.plist`
Finally, the last of the LaunchDaemons helps notify users as a `force_install_after_date` approaches by launching Managed Software Center, and could ultimately kill user sessions in the case that notifications were ignored and the countdown is exceeded. This is carried out by launchctl being called to start this job, which in turn calls the `/usr/local/munki/logouthelper` utility. `force_install_after_date` behavior is described in detail [here](https://github.com/munki/munki/wiki/Pkginfo-Files#force-install-after-date).

---
# LaunchAgents

##### `/Library/LaunchAgents/com.googlecode.munki.ManagedSoftwareCenter.plist`
If a background check finds an action requiring user notification should be performed, it needs to open the app in the users context. It uses a trigger file located at `/var/run/com.googlecode.munki.ManagedSoftwareCenter.plist` to perform this action, with specific checks so we're sure who the current user is even if FastUserSwitching might be in use.

---
##### `/Library/LaunchAgents/com.googlecode.munki.managedsoftwareupdate-loginwindow.plist`
In Munki 1, the behavior of making a change was very cautious and always offered the option to logout in order to perform actions. Now that protective nature only kicks in when an install or action will require a restart, for which we need to show a GUI at the loginwindow. Three trigger files activate this job, which leverage the previously-described `supervisor` utility for a 12-hour timeout:


- `/Users/Shared/.com.googlecode.munki.checkandinstallatstartup`,
which performs a check-in and run of any discovered configurations, perfect for [bootstrapping](https://github.com/munki/munki/wiki/Bootstrapping-With-Munki) a bare/thin image
- `/Users/Shared/.com.googlecode.munki.installatstartup`,
which just installs at startup WITHOUT checking in with the server, good for offline or limited-connectivity situations like user-level 802.1x networks,
	and 
- `/private/tmp/com.googlecode.munki.installatlogout`,
which installs at the loginwindow after a user logs out, again without checking in with the server 

---
##### `/Library/LaunchAgents/com.googlecode.munki.MunkiStatus.plist`
And finally, what actually displays status over the loginwindow and provides feedback to users so they know to hold off on logging in is an app that covers the login window while actions are being performed. It is called MunkiStatus, and is nested in Managed Software Center.app in `Contents/Resources`. The job that triggers it uses the same three paths as the previous `com.googlecode.munki.managedsoftwareupdate-loginwindow.plist`, but also with a dedicated 

- `/var/run/com.googlecode.munki.MunkiStatus` trigger file.