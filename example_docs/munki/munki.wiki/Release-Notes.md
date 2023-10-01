Please see the Releases page [here](https://github.com/munki/munki/releases) for current release notes. This page will remain as a historical record for releases prior to 2.0.

#### 2.0.0 Build 2212 release notes - 17 Sep 2014

Official 2.0 release of the Munki tools.

- All-new user interface: Managed Software Center. Supports OS X 10.6+. No support for 10.5.

#### 1.0.0 Build 1864 release notes - 10 Jan 2014

Official 1.0.0 release of the Munki tools. No code changes from previous release.

#### 0.9.2 Build 1863 release notes - 17 Dec 2013

- Logging changes

- Yet Another Unicode handling fix

- supported_architectures change: computers that have an arch of i386 but can *run* 64bit apps should now allow packages with x86_64 arch to install. Thanks to Jesse Peterson.

See https://code.google.com/p/munki/source/list for more details on recent changes.

#### 0.9.2 Build 1856 release notes - 26 Nov 2013

**This is a Release Candidate for version 0.9.2 of the Munki tools.**

- bugfix for download speed status messages

#### 0.9.2 Build 1855 release notes - 25 Nov 2013

**This is a Release Candidate for version 0.9.2 of the Munki tools.**

- Fix for unicode values in CFBundleVersion in Info.plists

- Changes to improve verbose messages and logging of download progress and speeds

- Fix for `curl` buffering headers output in Mavericks, causing progress display not
to function.

- Allow changing `curl` path for 10.9 `curl` client-side cert workaround

- Always add catalog info to pkginfo. Fixes issue with --nopkg.

- `makepkginfo` now inserts some user/environment metadata into generated pkginfo
files. It stores the metadata under the `*metadata` key. makecatalogs now strips
any key starting with `"*"` from pkginfo before adding the pkginfo to a catalog.

#### 0.9.2 Build 1846 release notes - 22 Oct 2013

**This is a testing build -- please test throughly before widespread deployment**

- Fix for a bug in the new firmware update warning code.

#### 0.9.2 Build 1842 release notes - 14 Oct 2013

**This is a testing build -- please test throughly before widespread deployment**

- Managed Software Update displays warnings when a firmware update is to be installed.

- Fixes for Optional Software update installs in Managed Software Update.app when item to be installed cannot be removed.

- Workarounds/fixes for handling Apple Software Updates in upcoming OS releases.

- More Unicode handling fixes

- Munki's support for Apple updates now ignores updates that have been marked to ignore (either via the Software Update GUI or /usr/sbin/softwareupdate --ignore

- Changes to munkiimport and makepkginfo to deal with already-mounted disk images.

- Support for licensed_seat_info for Optional installs.

- Adobe CC installer fixes

- Many other bug fixes,

#### 0.9.0 Build 1803 release notes - 20 June 2013

- Addresses an issue with the 10.8.4 update which would cause managedsoftwareupdate to hang for a very long time after installing the update.

- Fixes for Adobe CCP-created packages. Thanks to Pepijn Bruienne.

- munkiimport and makepkginfo now properly parse Adobe AAMEE/CCP packages that also include product updates. Thanks to Pepijn Bruienne for assistance.

- Localization updates and fixes for German, Spanish, and Swedish.

- Many bug fixes.

#### 0.8.4 Build 1770 release notes - 02 April 2013

Changes since the 0.8.3.1679.0 release:

- If installation fails for an item that is required by another item, Munki now properly defers installation of the dependent item(s). Similar behavior for uninstalls/removals.

- Some Unicode/UTF-8 fixes for munkiimport.

- Russian localization for Managed Software Update.app. Thanks to Soldatenko Rostislav.

- Fixes for IPv6 environments.

- Support for 'date' comparisons in conditional_items.  See [here](http://code.google.com/p/munki/wiki/ConditionalItems#Built-in_Conditions) for more info.

- Support for version comparison keys other than CFBundleShortVersion string for installs items.

- Apple updates and Munki updates can now appear and be installed in the same Munki "run". An exception to this is if the Munki updates contain Apple items; in this case, Munki will not display or install any Apple Software Update items to prevent conflicts.

- Support for adding additional metadata for Apple Software Update updates.
Admins can override blocking_applications and RestartAction, and add "unattended_install" and "force_install_after_date" values for Apple software updates. makepkginfo and munkiimport have been extended to create the needed pkginfo. Apple updates are identified by their ProductKey. An example:

    munkiimport --apple-update zzzz041-9792 --unattended_install

Tells Munki to attempt unattended_installs of iTunes 11.0.2.
Thanks to Heig Gregorian for this implementation.
See http://code.google.com/p/munki/wiki/PkginfoForAppleSoftwareUpdates for more info

- Many bug fixes.

See http://code.google.com/p/munki/source/list for detailed change log.

#### 0.8.3 Build 1679 release notes - 30 Nov 2012

Official release of the 0.8.3 version of Munki tools.

- Support for new "installable_condition" in pkginfo. See [here](http://code.google.com/p/munki/wiki/PkginfoFiles#installable_condition) for more info.

#### 0.8.3 Build 1664 release notes - 08 Nov 2012

Preview release for version 0.8.3 of the Munki tools.

This is a development release -- though it is believed stable, do not use in a production capacity without testing.

Some included changes since the 0.8.3.1634.0 release:

- A workaround for problems installing recent Apple software updates under 10.8.x. This issue caused softwareupdate to crash with an NSInvalidArgumentException error.

- Changes to the softwareupdate caching process to work around issues with Apple's updates; some recent updates did not have valid .dist files for some languages listed in the sucatalog.

- Change default Apple Software Update catalogs from .sucatalog.gz versions to .sucatalog versions to work around an issue with Mountain Lion's softwareupdate.

- Added Danish localization. Thanks to ttv@mbkpro-27.hlmn.dk

- In MSU.app, if removal detail is suppressed, and a removal item requires a logout, make sure MSU.app also requires a logout.

- A fix for an issue where Munki would crash if a use clicked "Cancel" in Managed Software Update.app while removals were being processed.

- Other bug fixes. 

#### 0.8.3 Build 1634 release notes - 27 Aug 2012

This is a development release -- though it is believed stable, do not use in a production capacity without testing.

Some included changes since the 0.8.2.1475.0 release:

- Fixes/workarounds for cfprefsd issues on Mountain Lion. This caused issues importing some disk images on Mountain Lion. Thanks to Heig Gregorian and Pepijn Bruienne.

- managedsoftwareupdate now prevents idle sleep while installing/removing items. Thanks to Michael Lynn for the Python bindings to IOKit functions.

- for copy_from_dmg type installs, if a destination directory does not exist, it will be created (along with any needed intermediate directories). Owner, group and mode for all created directories are based on the existing parent directory.

- fix Managed Software Update status display over the loginwindow in Leopard

- New optional "destination_item" key for "items_to_copy" items in "copy_from_dmg" installer_types. Specifies a different name to use for the item when copied; allows you to rename an item on copy. 

- New --destinationitemname option in makepkginfo for copy_from_dmg type installs. Sets the new - "destination_item" key.

- New "nopkg" installer_type. Allows for pkginfo items that do all their work with embedded scripts; no actual package is installed.

- Support for installcheck_script and uninstallcheck_script. If present, these will be used by Munki to determine the need to install or uninstall an item. A return code of 0 from the installcheck_script means install is needed; any other return code causes install to be skipped. For uninstall_check scripts, a return code of 0 means uninstall is needed; any other return code causes uninstall to be skipped.

- New "optional" key for individual receipts. If this key is present and set to "True", the receipt will not be considered when checking for the need to install an item.

- Changes to Managed Software Update.app's behavior and appearance when at the loginwindow in Lion and Mountain Lion.

- Changes to how /usr/sbin/installer is called when installing packages. Works around an issue with scripts in recent Microsoft Office 2011 updates.

- makepkginfo now has many, many new options that can create most available key/values for pkginfo files. Thanks to Heig Gregorian.

- munkiimport now supports all makepkginfo options. Thanks to Heig Gregorian.

- Previously, if ClientIdentifier is empty or undefined, Munki would ask for manifests in the following order:

1) Fully qualified hostname
2) "Short" hostname
3) "site_default"

This is now:

1) Fully qualified hostname
2) "Short" hostname
3) Machine serial number
4) "site_default"

Thanks to Nate Walck.

- New "minimum_munki_version" key in pkginfo; setting this prevents attempted installs of a specific package unless the client's version of munki is equal to or greater than the version defined by this key. Useful if you need an updated version of the Munki tools in place before you attempt to install a certain package.

- Notes in pkginfo files are removed when pkginfo files are compiled into catalogs; that is, catalogs will not contain any pkginfo notes.

- Spanish localization. Thanks to Noel Balonso.

- Dutch localization. Thanks to Pepjin Bruienne.

- French localization. Thanks to Claude Perrin.

- Finnish localization. Thanks to Hannes Juutilainen.


#### 0.8.3 Build 1564 release notes - 04 June 2012

This is a preview release for Munki 0.8.3. Do not use in a production environment without testing first!

- Changes to how /usr/sbin/installer is called when installing packages. Works around an issue with scripts in recent Microsoft Office 2011 updates.

- makepkginfo now has many, many new options that can create most available key/values for pkginfo files. Thanks to Heig Gregorian.

- munkiimport now supports all makepkginfo options. Thanks to Heig Gregorian.

- Previously, if ClientIdentifier is empty or undefined, Munki would ask for manifests in the following order:

1. Fully qualified hostname
1. "Short" hostname
1. "site_default"

This is now:

1. Fully qualified hostname
1. "Short" hostname
1. Machine serial number
1. "site_default"

Thanks to Nate Walck.

- New "minimum_munki_version" key in pkginfo; setting this prevents attempted installs of a specific package unless the client's version of munki is equal to or greater than the version defined by this key. Useful if you need an updated version of the Munki tools in place before you attempt to install a certain package.

- Notes in pkginfo files are removed when pkginfo files are compiled into catalogs; that is, catalogs will not contain any pkginfo notes.

- French and Finnish localizations. Thanks to Claude Perrin and Hannes Juutilainen.

- ApplicationInventory.plist now includes non-bundle applications.

- Miscellaneous bug fixes.

#### 0.8.2 Build 1475 Release notes - 20 April 2012

This is the official release for munki tools 0.8.2.

##### Known issues in this release

- munkiimport will fail to rebuild catalogs if the makecatalogs tool is not in the same directory as munkiimport.

- Munki preferences stored in /var/root/Library/Preferences/ManagedInstalls.plist do not work as expected under Mountain Lion DP.

- A corrupt LaunchServices database may cause managedsoftwareupdate to throw a FileNotFound exception and exit.

##### Change log

- Fix for installing Apple updates that would cause failures to not be reported as such.

- Managed Software Update.app: slow down a busy loop that could consume too much CPU when displaying a restart alert.

#### 0.8.2 Build 1473 Release notes - 12 April 2012

This is a release candidate for munki tools 0.8.2. Please test in your environment before wide deployment.

- Managed Software Update.app: Fix for items marked for forced_install_after_date that also require logout or restart.

- Fix localization issue for Managed Software Update.app on Snow Leopard (and possibly Leopard) when first preferred language is not English and not German.

- installer.py: Refactor of copyFromDMG() and copyAppFromDMG() to fix some logic errors and share code between the two functions

- installer.py: Output a deprecation warning if install_type 'appdmg' is encountered while installing; display an error instead of just logging if we encounter an install_type we don't know how to handle.


#### 0.8.2 Build 1468 Release notes - 03 April 2012

This is a release candidate for munki tools 0.8.2. Please test in your environment before wide deployment.

- Fixed a typo in some Managed Software Update output

- Skip /.MobileBackups directory when scanning for apps

- make sure all Exceptions are converted to strings before sending to munkicommon.display_error() (Fix for "object has no attribute 'rstrip'" errors)


#### 0.8.2 Build 1466 Release notes - 22 March 2012

Note: this is a preview of the 0.8.2 release. Please use in a testing capacity only.

Changes in this release:

- Bug fix: Fix a call to updatecheck.lookForUpdatesForVersion() with the wrong number of parameters.


#### 0.8.2 Build 1465  Release notes - 20 March 2012

Note: this is a preview of the 0.8.2 release. Please use in a testing capacity only.

Changes in this release:

- Support for Apple Software Update items that specify applications that must be closed before an update can be safely installed

- Support for admin-provided scripts to add additional conditions to test against for conditional_items. Contributed by Heig Gregorian. See http://code.google.com/p/munki/wiki/ConditionalItems#Admin_Provided_Conditions for more info.

- Added ipv4_address as an attribute available for conditional_items testing. This attribute contains an array of active IPv4 addresses on the client. See http://code.google.com/p/munki/wiki/ConditionalItems#Built-in_Conditions

- Better support for version numbers in "requires" and "update_for" arrays to control specific versions to apply an a update to.

- munkiimport now accepts --catalogs and --min-os-vers and --max-os-vers options. Useful for scripting munkiimport to avoid interactive specification of these options. Contributed by David Aguilar.

- makecatalogs can now be called without a path to a repo. If you have defined a repo path vi munkiimport --configure or manifestutil --configure, makecatalogs will use that path by default. You may still specify a repo path, which will take precedence.

- makepkginfo can now better parse certain Apple metapackages.

- makecatalogs and manifestutil now ignore all files and subdirectories whose name begins with a period.

- Managed Software Update.app: changes encoding of update descriptions so they will display properly in an unreleased version of Mac OS X.


#### 0.8.2 Build 1430 Release notes - 15 February 2012

Note: this is a **preview** of the 0.8.2 release. Please use in a testing capacity only.

Changes in this release:

- When caching the Apple software update catalog, we now follow redirects for compatibility with Lion's Software Update Service when using a "unified" catalog URL.

#### 0.8.2 Build 1425 Release notes - 13 February 2012

Note: this is a **preview** of the 0.8.2 release. Please use in a testing capacity only.

Changes in this release:

- `managedsoftwareupdate` now uses an HTTP user-agent string compatible with Apple's software update client when requesting software update catalogs. This should allow use of "unified" catalog URLs, which use server-side Apache rewrite rules.

- Support for a new installer_environment dictionary in pkginfo which contains key/value pairs to set environment variables for use by `/usr/sbin/installer` (See http://code.google.com/p/munki/wiki/PkginfoFiles#installer_environment)

- Managed Software Update.app now warns if a user decides to update while on battery power and less than 50% of battery power remains.

- Changes to Adobe CS4 installs -- will attempt to kill stalled Adobe AIR installations at the loginwindow

- `makecatalogs` now warns if it would overwrite an existing catalog. This partially addresses an issue with munki server data on a case-insensitive volume and catalog names that differ only by case.

- `managedsoftwareupdate` now waits to call Managed Software Update.app to notify the user until after the postflight script has finished executing.

- Application inventory now written to /Library/Managed Installs/ApplicationInventory.plist for use by reporting scripts.

- Other miscellaneous tweaks and bug fixes.

#### 0.8.1 Build 1363 Release notes - 02 February 2012

This release adds support for conditional_items in manifests.

See http://code.google.com/p/munki/wiki/ConditionalItems for more information.

#### 0.8.0 Build 1351 Release notes - 08 November 2011

Some of the new features available in this release:

- Support for preuninstall_script/postuninstall_scripts. See http://code.google.com/p/munki/wiki/PkginfoFiles#preuninstall_script/postuninstall_script for details.

- force_install_after_date: See http://code.google.com/p/munki/wiki/PkginfoFiles#force_install_after_date

- Completely rewritten support for checking for, downloading and installing Apple Software Updates that should be compatible with a larger number of Apple updates.  **Note:** If you point Munki to a custom SoftwareUpdateServerURL, or use a custom CatalogURL in com.apple.SoftwareUpdate (either directly or by using MCX), you must point to the actual OS-specific catalog, and not rely on Apache URL rewrites. (In other words, using a CatalogURL of the form 'http://<your server>:8088/index.sucatalog' will not currently work correctly with Munki.)

- And, of course, lots of miscellaneous bug fixes and tweaks. See http://code.google.com/p/munki/source/list for recent changes.

#### 0.7.1 Build 1173 Release notes - 11 May 2011

Some of the new features available in this release:

- Support for preinstall and postinstall script in pkginfo. See PreAndPostinstallScripts

- Now distributed as a metapackage. The munki admin can choose which subpackages to deploy; choosing, for example, to not deploy the munkitools_launchd subpackage in favor of a custom site-specific set of launchd files; or choosing not to deploy the munki admin tools on most machines.

- Managed Software Update.app can now log certain user actions. See [- forced_install/forced_uninstall now are called unattended_install/unattended_uninstall (though the old name will continue to work for at least a while) and are no longer necessarily blocked if they are part of a dependency relationship. This makes unattended_installs more generally useful.

- And, as always, lots of miscellaneous bug fixes and tweaks.


#### 0.7.0 Build 1047 Release notes - 02 March 2011

Some of the new features available in this release:

- The munki tools can now be used without a munki repo if all you are interested in is allowing users to install Apple Software Updates without needing admin rights. See: AppleSoftwareUpdatesWithMunki

- A new secure configuration file option to store sensitive munki settings that might be risky to store in /Library/Preferences/ManagedInstalls.plist, which is world-readable. See: http://code.google.com/p/munki/wiki/configuration#Secure_Config

- Support for "forced" installs and uninstalls.  See:
http://code.google.com/p/munki/wiki/PkginfoFiles#Forced_Installs_and_Uninstalls

- Support for "Blocking Applications" - if any of these applications are running, munki will not immediately install. See BlockingApplications for more info.

- New 'munkiimport' tool for importing installer items into a munki repo. See: http://code.google.com/p/munki/wiki/munkiimport

- munki now uses the LaunchServices database and Spotlight to search for applications that are not in their default location; this is faster than the previous System Profiler implementation and finds more apps on Leopard.

- New method for installing Apple Software Updates that is more reliable than prior methods.

- German language localization of Managed Software Update.app, and readiness for additional localizations. Thanks to Martin R. Hufsky.

- MCX support for the preferences normally specified in ManagedInstalls.plist. Thanks to Dan Roque.

- An MCX manifest in Managed Software Update.app

- Support for embedded uninstall scripts in pkginfo items. An example:

    	<key>uninstall_method</key>
    	<string>uninstall_script</string>
    	<key>uninstall_script</key>
    	<string>#!/bin/sh
    
    rm -rf "/Applications/Adobe Reader.app"
    rm -rf "/Library/Internet Plug-ins/AdobePDFViewer.plugin"
    rm -f "/Library/Application Support/Adobe/HelpCfg/en_US/Reader_10.0.helpcfg"
    
    pkgutil --forget com.adobe.acrobat.reader.10.reader.app.pkg.en_US
    pkgutil --forget com.adobe.acrobat.reader.10.reader.browser.pkg.en_US
    pkgutil --forget com.adobe.acrobat.reader.10.reader.appsupport.pkg.en_US
    	</string>
    	<key>uninstallable</key>
    	<true/>

- Lots of miscellaneous bug fixes and tweaks.


#### 0.6.0 Build 759 Release notes - 27 Sep 2010

- New copy_from_dmg installer type. Supports copying items from a disk image to arbitrary locations on the startup disk. Additionally, supports applying a custom user, group and mode to copied items. See [http://code.google.com/p/munki/wiki/CopyFromDMG CopyFromDMG](MSULogging]) for details. copy_from_dmg can replace appdmg installer types. You can tell makepkginfo to create a pkginfo item using the legacy appdmg installer type by using the --appdmg flag.

- Support for optional installs. See MunkiOptionalInstalls for details.

- Support for managed_updates.  These are items that munki will manage updates for, even if the item is not in any managed_installs list.  Items are listed in a manifest under a "managed_updates" key, using the same format as "managed_installs".

- Removed support for "modifies" dependency type. This was deprecated several months ago.

- Support for SHA-256 checksum to verify downloaded package integrity. makepkginfo now generates this checksum for pkginfo items. The PackageVerificationMode key in ManagedInstalls.plist controls this behavior. Set  PackageVerificationMode to "none" to disable package verification. The default is "hash"; the checksum will be verified if it exists; set the PackageVerificationMode to "hash-strict" to require checksums verification on all downloads. Thanks to Justin McWilliams for this submission.

- preflight and postflight scripts are now checked for security: they must be owned by the user running the managedsoftwareupdate process (this is generally root), the group must match that of the munki process (or be 'wheel') and the scripts must not be world-writable.  Thanks to Justin McWilliams for this submission.

- Support for additional HTTP headers to be sent when communicating with the munki server. These headers are specified in /Library/Preferences/ManagedInstalls.plist in the key "AdditionalHttpHeaders", which is an array of strings, each with an HTTP header:
        <key>AdditionalHttpHeaders</key> 
        <array> 
                <string>Key-With-Optional-Dashes: Foo Value</string> 
                <string>another-custom-header: bar value</string> 
        </array>
One could use this to obtain a cookie in a preflight script and update ManagedInstalls.plist with the appropriate header.  Thanks to Justin McWilliams for this submission. 

- Installation of Adobe CS5 products should now install Adobe Help and Adobe Media Player if they are included in the install.

- Numerous bug fixes and minor enhancements.  Some listed here:
- http://code.google.com/p/munki/issues/detail?id=12
- http://code.google.com/p/munki/issues/detail?id=22
- http://code.google.com/p/munki/issues/detail?id=23

#### 0.5.2 Build 572 Relase notes -16 Jul 2010

- Support for Adobe CS5 installers and updaters.  This support is still subject to the underlying issues with the Adobe installers. See [MunkiAndAdobeCS5](http://code.google.com/p/munki/wiki/MunkiAndAdobeCS5)

- Support for preflight and postflight scripts.  See PreflightAndPostflightScripts

#### 0.5.1 Build 533 Release notes -14 May 2010

Fixed version number returned by managedsoftwareupdate -V

#### 0.5.1 Build 532 Release notes -13 May 2010

- Managed Software Update.app 2.0.2:
- Now bounces icon in the Dock if it's in the background and has updates to install.
- When checking for updates, quits and relaunches before displaying updates to work better with Fast User Switching.

- updatecheck.py:
- Now uses /usr/bin/curl to download info and packages from the munki server. This also enables support for:
- SSL Server verification (https://)
- Partial download resumption
- Using E-Tags instead of modification dates to determine if a file has changed on the server

- Support for using a client certificate CN as the client identifier (defaults write /Library/Preferences/ManagedInstalls UseClientCertificateCNAsClientIdentifier -bool YES)


#### 0.5.0 Release notes - 08 March 2010

- Managed Software Update.app rewritten in Cocoa-Python (PyObjC), replacing the AppleScript Studio application.
- Managed Software Update.app now launched via a LaunchAgent to follow Apple recommendations on not calling LaunchServices from a daemon context.

- MunkiStatus.app moved from /Library/Application Support/Managed Installs to  inside the Managed Software Update.app application bundle (in /Applications/Utilities/Managed Software Update.app/Contents/Resources/)

- Some work done to make munki behave better if Fast User Switching is enabled:
- Managed Software Update.app will warn if there are multiple users logged in and refuse to initiate an update if an update requires a restart.
- MunkiStatus.app should now properly display in front of the loginwindow when Fast User Switching is active and we're switched to the loginwindow with (possibly) a user switched out.
- a new tool (/usr/local/munki/launchapp) is used by the LaunchAgents that launch Managed Software Update.app and MunkiStatus.app to ensure the app is launched only in the context of the current GUI user.
- /usr/bin/munki/managedsoftwareupdate checks for switched-out GUI users before restarting after an update session that requires a restart.

- appleupdates.getSoftwareUpdateInfo() now scans a packages in a downloaded distribution for RestartAction info. This addresses a case where the .dist file has no RestartAction info, but one or more of the subpackages does.

- Running makepkginfo no longer causes a default ManagedInfo.plist file to be written to /Library/Preferences if the file does not already exist.

- Support for suppressing package relocation for bundle-style packages. Add:
    <key>suppress_bundle_relocation</key>
    <true/>
  to a pkginfo item to enable this.

- Applications installed from "drag-n-drop" disk images are now ensured they are owned by root.

- Fix for retrieving main manifest from an https:// URL. Thanks to patrick.mcneal.

#### 0.4.9 Release notes - Jan 06 2010

- Support for Adobe Acrobat Pro 9 updater disk images.
- MunkiStatus now launched indirectly via a LaunchAgent to follow Apple recommendations on not calling LaunchServices from a daemon context.
- Various fixes for Adobe edge cases.

#### 0.4.8 Release notes - Dec 04 2009

- Managed Software Update.app has moved to /Applications/Utilities/.

- Support for CS3 Deployment "packages". See [MunkiAndAdobeCS3] for details.

- Changes to logging:
- Log rolling now implemented so logs do not grow without bounds
- New Installs.log tracks only the results of attempted installs and removals.
- New errors.log and warnings.log contain only the most recent errors and warnings

- Changes to reporting:
- /Library/Managed Installs/InstallInfo.plist now contains ONLY items that need to be installed or removed.
- /Library/Managed Installs/ManagedInstallReport.plist is a comphrensive summary of the most recent managedsoftwareupdate session. It contains info on:
- ManagedInstallVersion
- AvailableDiskSpace
- ConsoleUser
- MachineInfo
- ManifestName
- StartTime/EndTime
- ItemsToInstall/ItemsToRemove
- InstallResults/RemovalResults
- ManagedInstalls
- ManagedRemovals
- ProblemInstalls
- ProblemRemovals
- Errors
- Warnings

- Apple Update changes:
- If munki is configured to handle Apple Software Updates and:
- There are available munki updates -and-
- There are available Apple updates, then:
- munki installs only the munki updates.
- This change was made to eliminate the confusion and undesired behaviors that occurred when available munki updates duplicated Apple Updates, or made them unneeded.  Now the munki updates are done, and a subsequent Apple Software Update check would return more accurate results based on the new configuration.

- Experimental support for an `autoremove` boolean key in pkginfo. This would be used to indicate a software item that should be automatically removed from a client if the item is not in the managed_installs section of the client's manifest (or included manifests).  See [[Munki And Auto Remove]] for more info.

- UI support for packages that recommend restart (instead of require restart) and those that require logout.

- pkginfo now has an optional "package_path" key, which is a string containing a relative path to the package to be installed on a disk image. This allows munki to install items that aren't at the root of the disk image, and to install the "correct" item when there are multiple packages at the disk image root.

- /Library/Preferences/ManagedInstalls.plist now supports explicit URLs for:
- ManifestURL - example - "http://munki/repo/manifests/"
- CatalogURL  - example - "http://munki/repo/catalogs/"
- PackageURL  - example - "http://differentserver/pkgs/"
- These allow you to point munki to one server for the munki-specific data, while pointing it at another server for the actual installation packages/disk images.

- Lots of bug fixes and UI tweaks.


#### 0.4.7 Release notes

0.4.7 was an internal release only, and was not made available publicly.

#### 0.4.6 Release notes - Nov 02 2009

- /usr/local/munki/managedsoftwareupdate -V now prints the release version number.
- Changes to the dependancy model:
- The 'modifies' dependancy type is now deprecated and support will be removed in a future release.
- New pkginfo key: 'update_for'
- This takes an array of strings, each of which refers to another pkginfo item:

An example:
    	<key>name</key>
    	<string>PhotoshopCameraRaw</string>
    	<key>update_for</key>
    	<array>
    	  <string>PhotoshopCS4</string>
    	  <string>AdobeCS4DesignStandard</string>
              <string>AdobeCS4MasterCollection</string>
    	</array>

The PhotoshopCameraRaw item is an update for PhotoshopCS4, AdobeCS4DesignStandard, and the AdobeCS4MasterCollection. 

Whenever munki processes a managed_installs item or removals item, it looks in the currently available catalogs for items that declare they are updates for the current item, and will add them to the list of things to install or remove. You can use the 'requires' key to ensure the updates are installed in the correct order.

With this addition, the 'modifies' key becomes redundant; you can express the same relationship (and more complex relationships) using the 'update_for' and 'requires' keys. See the example pkginfo items in the Source code repo for more examples.

#### 0.4.5 notes

0.4.5 was an internal release only, and was not made available publicly.

#### 0.4.4 Release notes - Oct 22 2009

- Support for Adobe CS4 Deployment Toolkit "packages" encapsulated into disk images.
- Support for Adobe CS4 Update installer dmgs.
- see http://code.google.com/p/munki/wiki/MunkiAndAdobeCS4 for more info.

- Support for disk images containing a single application that is to be copied to /Applications
- See http://code.google.com/p/munki/wiki/AppDmgPackageNotes for more info.

- New version of Managed Software Update.app that fixes some bugs when displaying software removals in the list of available updates.

- makepkginfo can be called with -f arguments and no installer item to make it easier to post-generate lists of items that a given installer item installs.

- Example:
    makepkginfo -f /Applications/Remote\ Desktop\ Connection.app
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
    	<key>installs</key>
    	<array>
    		<dict>
    			<key>CFBundleIdentifier</key>
    			<string>com.microsoft.rdc</string>
    			<key>CFBundleName</key>
    			<string>RDC</string>
    			<key>CFBundleShortVersionString</key>
    			<string>2.0.0</string>
    			<key>path</key>
    			<string>/Applications/Remote Desktop Connection.app</string>
    			<key>type</key>
    			<string>application</string>
    		</dict>
    	</array>
    </dict>
    </plist>

An admin could now copy and paste the 'installs' info into a pkginfo file for Microsoft's RDC install package if they didn't add this info when the pkginfo file was originally created.

- makepkginfo can generate a pkginfo file for disk images containing a single application that is to be copied to /Applications.
- makepkginfo can generate a basic pkginfo file for Adobe CS4 Deployment  disk images and for Adobe CS4 Update installer dmgs.

Note that since the non-Apple installer items types now supported by munki do not have package receipts, it is vital they have entries under the 'installs' key in order for munki to be able to determine whether or not they're already installed.

#### 0.4.3 Release notes

There was no public 0.4.3 release.

#### 0.4.2 Release notes - Oct 14 2009

The 0.4.2 release of the munki tools features experimental support for handling Apple Software Updates.

By default, handling Apple Software Updates is off.

To turn it on, 

   `defaults write /Library/Preferences/ManagedInstalls InstallAppleSoftwareUpdates -bool YES`

Since it's using Apple's tools, it should talk to whichever Software Update Server you have configured (via MCX or in /Library/Preferences/com.apple.SoftwareUpdate.plist).  If none is configured, it talks to Apple's SUS.

If you'd like the munkitools to use an alternate SUS URL:

   `defaults write /Library/Preferences/ManagedInstalls SoftwareUpdateServerURL "<SUS URL>"`

Some notes:

- Most of the code for Apple Updates is in munkilib/appleupdates.py; some is in managedsoftwareupdate.

- On Leopard, when checking for updates, appleupdates.py uses /System/Library/CoreServices/Software Update.app/Contents/Resources/SoftwareUpdateCheck
- On Snow Leopard, /usr/sbin/softwareupdate is used.

- Since I could not get the 'install-and-restart' behavior of Software Update.app working consistently to my satlisfaction, I've gone back to the approach of using /usr/sbin/installer install the items downloaded by softwareupdate (using existing code in munkilib/installer.py).  The last time I tried this, I kept finding downloads /usr/sbin/installer refused to install.  I'm trying a slightly different approach this time and have not yet had an issue, but the sample size is small.

- If munki finds available Apple Updates, and a restart is required for these updates, it installs them, restarts, then installs any available updates from the munki repo, again restarting if needed.  This behavior cannot currently be customized.