## Frequently Asked Questions
***
### General questions
***

#### Q: How do you pronounce Munki?

**A**: Same as "monkey."

#### Q:  Does Munki stand for something?

**A**: Nope.  Just a fun name that evokes "helper monkeys."

***
### Munki Installation
***
#### Q: Where do I get the latest release of the Munki tools?

**A**: Official releases (and release candidates) are here: [Munki Releases](https://github.com/munki/munki/releases)

#### Q: How do I deploy the Munki tools to the Macs I want to manage?

**A**: There are many approaches to this. See [Deploying Munki](Munki-packages-and-restarts#deploying-munki) for some ideas.

#### Q: Why does the munkitools.mpkg/launchd.pkg require a restart? This prevents an unattended upgrade of the Munki tools!

**A**: It is non-trivial to load launchd jobs, especially user-level LaunchAgents, in the correct Mach context from a package postinstall script in all possible execution contexts in which a package can be installed. But more importantly, the launchd jobs control Munki itself, and so Munki could not unload and reload these jobs without killing itself during the unload. So for maximum reliability, we require a restart so we ensure the jobs are loaded in the correct context and that Munki can actually complete the task! See [[Munki packages and restarts]] for even more information about this.  
As for unattended updates of the Munki tools, in most cases it *is* possible to upgrade them without requiring a logout or restart. See [[Updating Munki Tools|Updating-Munki-Tools]] for additional information.

#### Q: Can I skip the installation of the Munki admin tools on my managed clients?

**A**: Yes, but it's probably not worth the effort. In order to make changes to the Munki repo, your clients/users need write access to it. Having the repo editing tools installed is no more "dangerous" than having a text editor, `vi`, or `PlistBuddy` installed. On the other hand, having the admin tools installed means you don't have to track which machines belong to people who are Munki admins in your org. If you really, really want to not install the admin tools, take a look here: [[ChoiceChangesXML|ChoiceChangesXML]] and here [[Updating Munki Tools|Updating-Munki-Tools]] for info on how you could skip the install of the admin tools. (No, it's not spelled out explicitly -- because it's recommended to just install the entire set of tools.)

***
### Munki Capabilities
***
#### Q: What installer formats does Munki support?

**A**: Munki supports the following formats:
- Apple Installer packages (.pkg/.mpkg)
- Drag-and-drop Application disk images (Disk images that contain an application at the root of the mounted disk)
- Adobe CS3/CS4/CS5/CS6/CC Deployment "packages" created with Adobe's Enterprise Deployment tools - [CS3 info](http://www.adobe.com/support/deployment/cs3_deployment.pdf),  [CS4/CS5/CS6 info](http://www.adobe.com/devnet/creativesuite/enterprisedeployment.html), [CC info](https://github.com/munki/munki/wiki/Munki%20And%20Adobe%20CC)
- Many Adobe CS3/CS4/CS5/CS6/CC product updaters
- Adobe Acrobat Pro 9.x updater disk images as [downloaded from Adobe](http://www.adobe.com/support/downloads/product.jsp?product=1&platform=Macintosh)

Munki does _not_ directly support other third-party installer formats like InstallerVISE, InstallAnywhere, BitRock Installer, etc, or "installers" that are actually applications that just copy stuff onto the disk.

#### Q:  Can Munki install Apple Software Updates?

**A**: In some cases, but the trend is towards no. See [[Apple Software Updates With Munki|Apple-Software-Updates-With-Munki]] for more information. Managed Software Center can prompt users to manually install pending Apple updates.

#### Q: Can I deploy Mac App Store apps using Munki?

**A**: In many cases, yes. See [App Store Apps](https://github.com/munki/munki/wiki/App-Store-Apps)

#### Q: Can I deploy Configuration Profiles using Munki?

**A**: Not with recent versions of macOS, no. Apple has restricted automated configuration profile install to MDM. With macOS versions prior to Big Sur (macOS 11), Munki can install Device profiles (but not User profiles or Enrollment profiles). See [[Managing Configuration Profiles|Managing-Configuration-Profiles]]

#### Q: Can I manage printers using Munki?

**A**: Yes. While not a core feature of Munki, it is possible. See [[Managing Printers With Munki|Managing-Printers-With-Munki]]

#### Q: Can I install/manage (insert some other random thing) with Munki?

**A**: If you can put it into an Apple package or write a script to do it as the root user, probably! If it's something that must be done at the user level, you may need to look at other tools.

#### Q: Can Munki upgrade itself? Can I use Munki to install an updated version of Munki?

**A**: Yes. See [[Updating Munki Tools|Updating-Munki-Tools]].

#### Q: Can I use Munki to install major macOS upgrades (like upgrade machines to Big Sur)?

**A**: Yes. See  [[macOS Installer Application support|macOS-Installer-Application-support]] and [[Installing macOS|Installing-macOS]] (for older releases of macOS).

#### Q: Can Munki install a certain package for "FooSoftware" on Intel Macs and a different package for the same software on Apple silicon Macs?

**A**: Yes. See [[Supported Architectures|https://github.com/munki/munki/wiki/Pkginfo-Files#supported_architectures]]. Import the package for Intel and set its supported_architectures to an array containing "x86_64". Import the package for Apple Silicon under the same product name and set its supported_architectures to an array containing "arm64". `munkiimport`'s `--arch` option is useful here. (If the vendor offers a package/disk image containing a Universal2 version of the software that is arguably a better approach.)

#### Q: Can Munki install a certain package for "FooSoftware" on Macs running Catalina and below and a different package for the same software on Macs running Big Sur and higher?

**A**: Yes. See the previous question and answer. In this case, you'd set `minimum_os_version` and/or `maximum_os_version` to indicate which item should be installed on which OS version. You can use the `--minimum-os-version` and `--maximum-os-version` options with `munkiimport` and `makepkginfo` to set these.

***
### Munki Behaviors
***
#### Q: How often do Munki clients check for updates?

**A**: On average, once an hour. The exact time between checks is randomized somewhat to prevent every client from hitting the Munki server all at once. A launchd job defined at [/Library/LaunchDaemons/com.googlecode.munki.managedsoftwareupdate-check.plist](https://github.com/munki/munki/blob/master/launchd/LaunchDaemons/com.googlecode.munki.managedsoftwareupdate-check.plist) runs at every 10 past the hour (e.g. 9:10). It, in turn, calls [/usr/local/munki/supervisor](https://github.com/munki/munki/blob/master/code/client/supervisor), which sleeps a random time between 0 and 60 minutes (3600 seconds, to be exact) before performing an 'auto' run. This means that the time between any two Munki runs can vary from a few minutes to almost two hours. (See [[Launchd Jobs and Changing When Munki Runs]] for more info.)

#### Q:  How is a user notified of available updates?

**A**: Munki uses Notification Center notifications to notify users of pending updates. If a user ignores pending updates for too long (default 3 days), an application named "Managed Software Center", which looks very much like Apple's App Store application, will open and display available updates. Like with Apple's App Store, the user can then choose to install the updates now, or wait until later. Unlike with Apple's App Store, the user cannot pick and choose among the updates. Those are managed by the Munki administrator. If any update requires a logout or restart, Managed Software Center triggers a logout before proceeding. Otherwise, the user can choose to update immediately.

#### Q: Does Munki support Notification Center notifications?

**A**: Munki 3 added support for Notification Center. See [[Notification Center Support]]. Earlier versions of Munki do not support Notification Center notifications.

#### Q: Will Munki pop up notifications if a user is doing a presentation in front of an audience?

**A**: Yes, it might.  
There is no reliable way to detect that a user is "doing a presentation", so Munki can't automagically not notify when a presentation is happening. There are many, many possible presentation applications. Here are a few: Keynote, PowerPoint, Preview, Prezi, Acrobat, Acrobat Reader, Safari, Chrome, Firefox -- even the Finder by using the full-screen slideshow feature. There are multiple ways for an app to display content full-screen, and not all of them are "detectable" by other apps.

Apple provides a mechanism: Notification Center's "Do Not Disturb" setting. It is designed to temporarily suppress all Notification Center notifications. Munki uses Notification Center and respects Do Not Disturb. But your users must remember to activate it.

Do note that if a user ignores pending updates for too long (default: 3 days; admin-configurable), Munki stops posting Notification Center notifications and instead launches Managed Software Center to display the list of available updates, and this could well happen during a "presentation".

#### Q:  What happens if the user chooses to update without logging out, but some of the updates are for applications that are currently open?

**A:** Munki can check for certain applications and notify the user to quit them before proceeding. See [[Blocking Applications|Blocking-Applications]] for more info on this feature.

#### Q:  What if there is no user logged in?

**A**: The check schedule is the same (roughly once an hour). If there are updates available, Munki will install them if there is no user logged in and the machine has been idle for 10 seconds or longer. A status window is displayed over the loginwindow, and the loginwindow is disabled so that no-one can login while updates are occurring.

#### Q: How does Munki determine if the correct version of an application is installed?

**A**: If the path to the application appears in the "installs" array, Munki will first check that path.  If the application is found at the given path, its CFBundleShortVersionString string is checked.  If it matches what's listed in the manifest, Munki knows the correct version is installed.  If the application isn't found at the given path, LaunchServices and Spotlight are consulted to gather a list of all installed applications.  If the application is listed with the correct version number, Munki knows the correct version is installed.  If it's not listed, or it has an earlier version number, Munki knows the application must be installed.

If there is no "installs" list, Munki relies on package receipts listed in the "receipts" array to determine installation status.

See [[How Munki Decides What Needs To Be Installed|How-Munki-Decides-What-Needs-To-Be-Installed]] for even more information on this topic.

***
### Troubleshooting
***
#### Q: How do I get more information about what is happening when Munki runs?

**A**: There are a couple of ways to get more information:
- You can raise the logging level: `sudo defaults write /Library/Preferences/ManagedInstalls LoggingLevel 4`. Then view/monitor the ManagedSoftwareUpdate log (usually found at /Library/Managed Installs/Logs/ManagedSoftwareUpdate.log)
- You can run the tools at the command line with additional verbose flags: `sudo managedsoftwareupdate -vvv`

See also [[Troubleshooting|Troubleshooting]].

#### Q: I keep getting 'Can't install Foo-1.0 because the integrity check failed.'

**A**: "integrity check failed" means the SHA-256 hash of the downloaded item does not match the SHA-256 hash stored in the pkginfo under the "installer_item_hash" key.  
This will happen if you replace or edit the installer item without updating the associated pkginfo (and rebuilding catalogs).  
Another scenario that triggers this is when the disk image containing Foo-1.0 is a read/write disk image. Convert the disk image to read-only and reimport the item.  
Other (not-recommended) methods of suppressing this error include:  
- Deleting the "installer_item_hash" key from the pkginfo for that item. Munki will not verify the integrity hash.
- Configure Munki to not verify package checksums (not recommended). See the PackageVerificationMode key in https://github.com/munki/munki/wiki/Preferences.

#### Q: I made a change to a pkginfo file but my clients aren't seeing the change.

**A**: Did you run `makecatalogs` after modifying the pkginfo file?

#### Q: I keep seeing warnings like _WARNING: Could not process item Office2011_update-14.4.2 for update. No pkginfo found in catalogs: production_, yet there is definitely an item named "Office2011_update-14.4.2" in the production catalog. What is happening?

**A**: A name followed by a hyphen and a version number (or a number!) has special meaning: it means NAME-VERSION. So Munki is actually looking for an item named "Office2011_update" with a version of "14.4.2". It is NOT looking for an item with the name "Office2011_update-14.4.2". To avoid this type of confusion, don't put versions into names. It's rarely good practice to do so. If you must, don't precede the version with a hyphen. (Any number preceded by a hyphen is likely to be interpreted as a version number.)

#### Q: Each time Munki runs, it wants to install the same software again. Why is this?

**A**: The most likely explanation is that the install has failed. On the next run, Munki sees the item is not installed, and tries again. If the item actually *is* installed, see the next question...

#### Q: Munki *successfully* installed some software, but now each time Munki runs, it wants to install the software again. Why is this?

**A**: Munki usually uses one of two arrays in the pkginfo to determine if an item is installed. If the "installs" array exists, each item in the array is checked; if it does not exist or the currently installed version is older than the one described in the pkginfo, Munki will attempt to install the item. If there is no "installs" array, Munki will use the "receipts" array, again installing if any receipt is missing or is an older version that that described in the pkginfo.  
If Munki repeatedly presents an item for install after a successful installation, then one or more items in the "installs" array is not being installed, or one or more items in the "receipts" array is not being recorded in the receipts database. You'll need to determine what is not being installed and remove it from the installs or receipts array. (Or in the case of a receipt, mark it as "optional".) Alternately, if there is no installs array, you can often resolve this issue by *adding* an installs array.  
See [[How Munki Decides What Needs To Be Installed|How-Munki-Decides-What-Needs-To-Be-Installed]] for even more information on this topic.

#### Q:  I just set up Munki and there's nothing available under "Software" or "Categories" and the icons are greyed out. How do I make things available there?

**A**: Add items to optional_installs in the relevant manifests. Items under "Software" or "Categories" can be installed or removed under the user's control: they aren't enforced as installed, updated, or removed. If there are no items in optional_installs, there's nothing for the user to choose to install (or remove.)

#### Q: Managed Software Center is displaying an alert with the text "There is a configuration problem with the managed software installer. Could not start the process. Contact your systems administrator." What is wrong?

**A**: Managed Software Center could not start `managedsoftwareupdate`. This is usually because the required LaunchDaemons are not loaded, which is most commonly caused by installing the Munki tools for the first time, but failing to restart. More information on the LaunchDaemons is [here](https://github.com/munki/munki/wiki/Launchd-Jobs-and-Changing-When-Munki-Runs#launchdaemons).

#### Q: Managed Software Center is displaying an alert with the text "There is a configuration problem with the managed software installer. The process ended unexpectedly. Contact your systems administrator." What is wrong?

**A**: `managedsoftwareupdate` is ending unexpectedly. This could mean it is crashing, or that some other process is killing it. Check the [log](https://github.com/munki/munki/wiki/Troubleshooting#logs) for details, or run `sudo managedsoftwareupdate -vvv` and/or `sudo managedsoftwareupdate --installonly -vvv` to see if you can replicate the issue.

#### Q: Managed Software Center is displaying an alert with the text "Managed Software Center cannot check for updates now. Try again later. If this situation continues, contact your systems administrator." Why can't it check for updates now?

**A**: A Munki preflight script has exited non-zero. This could be intentional on the admin's part: perhaps the preflight is checking for certain conditionals and exiting non-zero to prevent a Munki run. See [here](Preflight-And-Postflight-Scripts) for more information on Munki preflight scripts.

***
### More
***

#### Q: I really like Munki for managing software on macOS. Is there a Windows version?

**A**: No. But check out [Gorilla](https://github.com/1dustindavis/gorilla).

#### Q: I have a question that isn't answered here. Where do I go for help?

**A**: Try these resources:
* The Munki wiki: https://github.com/munki/munki/wiki
* Troubleshooting tips: https://github.com/munki/munki/wiki/Troubleshooting
* Discussion group: http://groups.google.com/group/munki-discuss
* Professional support: https://github.com/munki/munki/wiki/Professional-Support