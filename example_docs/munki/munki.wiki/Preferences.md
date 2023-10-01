_Details on Munki's preferences_

### Introduction

Munki stores its configuration info in the "ManagedInstalls" preferences domain. By default, this info is stored in /Library/Preferences/ManagedInstalls.plist, but you can also use MCX, configuration profiles, or /private/var/root/Library/Preferences/ManagedInstalls.plist, or a combination of these locations with the normal defaults precedence:

- MCX/Configuration profiles
- /private/var/root/Library/Preferences/ByHost/ManagedInstalls.XXXXXX.plist
- /private/var/root/Library/Preferences/ManagedInstalls.plist
- /Library/Preferences/ManagedInstalls.plist

> Munki 3.1 new feature <p/> `managedsoftwareupdate` has a new `--show-config` option, which will print Munki's current configuration. This can be helpful when troubleshooting the potentially confusing interaction between different preference levels and managed preferences.

### Details

Here's a sample /Library/Preferences/ManagedInstalls.plist:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>ClientIdentifier</key>
    <string>arbitrary_name</string>
    <key>SoftwareRepoURL</key>
    <string>http://munkiwebserver/repo</string>
    <key>LoggingLevel</key>
    <integer>1</integer>
    <key>DaysBetweenNotifications</key>
    <integer>1</integer>
</dict>
</plist>
```

#### Supported ManagedInstalls Keys

_(Scroll the table horizontally to see all columns -- GitHub's default view tends to hide the last column, which contains a description of the key.)_

| Key | Type | Default | Description |
| --- | -------- | ------- | ----------- |
| AppleSoftwareUpdatesOnly | boolean | false | If true, only install updates from an Apple Software Update server. No Munki repository is needed or used.|
| AggressiveUpdateNotificationDays| integer | 14 | Munki 5's more aggressive update behaviors begin when one or more updates have been pending for more than 14 days by default. Set it to 0 to never trigger the aggressive behavior.|
| InstallAppleSoftwareUpdates | boolean | false | If true, install updates from an Apple Software Update server, in addition to "regular" Munki updates.|
| UnattendedAppleUpdates | boolean | false | If true, updates that declare no "must-close" applications, or have one or more "must-close" applications, none of which is running, and do not require a logout or restart will be installed as part of a normal periodic background run without notifying the user. (OS X 10.10+, Munki 2.5+)|
| (SoftwareUpdateServerURL) [Deprecated](https://github.com/munki/munki/wiki/Apple-Software-Updates-With-Munki#el-capitan-notes)| string |  | Catalog URL for Apple Software Updates. If undefined or empty, Munki will use the same catalog that the OS uses when you run Apple's Software Update application or call /usr/sbin/softwareupdate. |
| SoftwareRepoURL | string | See [[Default Repo Detection]] | Base URL for Munki repository|
| PackageURL | string | `<SoftwareRepoURL>`/pkgs | Base URL for Munki pkgs. Useful if your packages are served from a different server than your catalogs or manifests.|
| CatalogURL | string | `<SoftwareRepoURL>`/catalogs | Base URL for Munki catalogs. Useful if your catalogs are served from a different server than your packages or manifests.|
| ManifestURL | string | `<SoftwareRepoURL>`/manifests | Base URL for Munki manifests. Useful if your manifests are served from a different server than your catalogs or packages.|
| IconURL | string | `<SoftwareRepoURL>`/icons | Base URL for product icons. Useful if your icons are served from a different server or different directory than the default.|
| ClientResourceURL | string | `<SoftwareRepoURL>`/client_resources | Base URL for custom client resources for Managed Software Center. Useful if your resources are served from a different server or different directory than the default.|
| ClientResourcesFilename | string | manifest name.zip or site_default.zip | Specific filename to use when requesting custom client resources.|
| HelpURL | string | none | If defined, a URL to open/display when the user selects "Managed Software Center Help" from Managed Software Center's Help menu.|
| ClientIdentifier | string | See [[Default Manifest Resolution]] | Identifier for Munki client. Usually is the same as a manifest name on the Munki server. If this is empty or undefined, Munki will attempt the following identifiers, in order: fully-qualified hostname, "short" hostname, serial number and finally, "site_default" |
| ManagedInstallDir | string | /Library/Managed Installs | Folder where Munki keeps its data on the client.|
| LogFile | string | /Library/Managed Installs/Logs/ManagedSoftwareUpdate.log | Primary log is written to this file. Other logs are written into the same directory as this file.|
| LogToSyslog | boolean | false | If true, log to syslog in addition to ManagedSoftwareUpdate.log.|
| LoggingLevel | integer | 1 | Higher values cause more detail to be written to the primary log.|
| DaysBetweenNotifications | integer | 1 | Number of days between user notifications from Managed Software Center. Set to 0 to have Managed Software Center notify every time a background check runs if there are available updates.|
| UseNotificationCenterDays | integer | 3 | (New in Munki 3) Number of days Notification Center notifications should be used before switching to launching Managed Software Center. See [[Notification Center Support]].|
| UseClientCertificate | boolean | false | If true, use an SSL client certificate when communicating with the Munki server. Requires an https:// URL for the Munki repo. See ClientCertificatePath for details.|
| UseClientCertificateCNAsClientIdentifier | boolean | false | If true, use the CN of the client certificate as the Client Identifier.Used in combination with the UseClientCertificate key.|
| SoftwareRepoCAPath | string | (empty) | Path to the directory that stores your CA certificate(s). See the curl man page for more details on this parameter.|
| SoftwareRepoCACertificate | string | /Library/Managed Installs/certs/ca.pem | Absolute path to your CA Certificate.|
| ClientCertificatePath | string | /Library/Managed Installs/certs/[munki.pem\|client.pem\|cert.pem] | Absolute path to a client certificate. There are 3 defaults for this key. Concatenated cert/key PEM file accepted.|
| ClientKeyPath | string | (empty) | Absolute path to a client private key.|
| AdditionalHttpHeaders | array | (empty) | This key provides the ability to specify custom HTTP headers to be sent with all curl() HTTP requests. AdditionalHttpHeaders must be an array of strings with valid HTTP header format.|
| PackageVerificationMode | string | hash | Controls how Munki verifies the integrity of downloaded packages. Possible values are: *none*: No integrity check is performed. *hash*: Integrity check is performed if package info contains checksum information. *hash_strict*: Integrity check is performed, and fails if package info does not contain checksum information.|
| SuppressUserNotification | boolean | false | If true, Managed Software Center will never notify the user of available updates. Managed Software Center can still be manually invoked to discover and install updates.|
| SuppressAutoInstall | boolean | false | If true, Munki will not automatically install or remove items.|
| SuppressLoginwindowInstall | boolean | false | If true, Munki will not install items while idle at the loginwindow except for those marked for unattended_install or unattended_uninstall. |
| SuppressStopButtonOnInstall | boolean | false | If true, Managed Software Center will hide the stop button while installing or removing software, preventing users from interrupting the install.|
| InstallRequiresLogout | boolean | false | If true, Managed Software Center will require a logout for all installs or removals.|
| ShowRemovalDetail | boolean | false | This preference is no longer supported. In versions of Munki prior to 2.0: if true, Managed Software Updates.app will display detail for scheduled removals.|
| MSULogEnabled | boolean | false | Log user actions in the GUI. See [[MSC-Logging]] |
| MSUDebugLogEnabled | boolean | false | Debug logging for Managed Software Center. See [[MSC-Logging]] |
| LocalOnlyManifest | string | (empty) | Defines the name of your LocalOnlyManifest. Setting this activates the feature. Unsetting it means Munki will remove the file on the next run. See [[LocalOnlyManifest]] |
| FollowHTTPRedirects | string | none | Defines whether Munki will follow all, some or no redirects from the web server. See [FollowHTTPRedirects](#followhttpredirects) |
| IgnoreSystemProxies | boolean | false | If true, HTTP and/or HTTPS proxies set system-wide will be ignored, connections will be made directly.|
| PerformAuthRestarts | boolean | false | (New in Munki 3) If true, Munki will attempt to perform a filevault auth restart. See [[Authorized-Restarts]].|
| RecoveryKeyFile | string | none | (New in Munki 3) Absolute path to a plist file containing filevault credentials in key/value format. Used to perform auth restarts. See [[Authorized-Restarts]].|
| ShowOptionalInstallsForHigherOSVersions | boolean | false | (New in Munki 3.1) If true, Managed Software Center.app will show optional installs and updates that apply to macOS versions higher than the currently installed version.|
| EmulateProfileSupport | boolean | false | (New in Munki 5.2) If true, Munki will attempt to emulate the functionality of Managed Preferences from configuration profiles on Big Sur. See [[Configuration-Profile-Emulation]] for more info.|

#### Additional Notes

##### LogFile

Munki normally writes its logs to /Library/Managed Installs/Logs/, with the main log written to ManagedSoftwareUpdate.log in that directory. Other logs are named "Install.log", "errors.log", and "warnings.log".  If you'd like the logs to be written somewhere else (for example /var/log or /Library/Logs), set LogFile to the desired pathname of the main log:

`sudo defaults write /Library/Preferences/ManagedInstalls LogFile "/var/log/munki/managedsoftwareupdate.log"`

The other logs will be written to the same directory.

##### InstallAppleSoftwareUpdates

If this key is present and set to True, Munki will call softwareupdate and attempt to install Apple Software Updates.

##### SoftwareUpdateServerURL

This key can be used to point to an internal Apple Software Update server.

##### SuppressUserNotification

This key (when present and value is set to True) causes Munki to never notify users of available updates. This might be useful in a lab environment, where you'd like updates to be applied only when no-one is logged in and the machine is at the login window.

##### SuppressAutoInstall

Normally, Munki automatically installs and removes software if there are changes needed and that machine is at the loginwindow with no users logged in. If you have a need to do updates always and only with the consent of the user, including packages configured with unattended_install and unattended_uninstall, setting SuppressAutoInstall to True prevents Munki from automatically installing updates and processing removals.

##### SuppressLoginwindowInstall

(Added in version 0.8.4.1696.0) If this preference is set to true, Munki will not install updates when idle at the loginwindow, with the exception of updates marked for unattended_install or unattended_uninstall.

##### ShowRemovalDetail

By default, Managed Software Update.app suppresses detail on what will be removed, instead showing a simple "Software removals" entry in the list. If you'd like Managed Software Update.app to show specific detail about what will be removed, set ShowRemovalDetail to True. This key has no effect on /usr/local/munki/managedsoftwareupdate, which always shows all detail.

##### InstallRequiresLogout

Managed Software Center.app enforces a logout before it installs or removes software only if one or more items to be installed/removed requires a logout or restart. You can force a logout for all updates by setting InstallRequiresLogout to True. This key has no effect on running /usr/local/munki/managedsoftwareupdate from the command-line.

##### AdditionalHttpHeaders

This key provides the ability to specify custom HTTP headers to be sent with all HTTP/HTTPS requests. AdditionalHttpHeaders must be an array of strings with valid HTTP header format. For example:

```xml
<key>AdditionalHttpHeaders</key>
<array>
    <string>Key-With-Optional-Dashes: Foo Value</string>
    <string>another-custom-header: bar value</string>
</array>
```

One could use this to obtain a cookie in a preflight script and update ManagedInstalls.plist with the appropriate header.  However, it is recommended that you use Secure Config for sensitive data (i.e. cookie) since ManagedInstalls.plist is world-readable.

##### FollowHTTPRedirects

By default, Munki will not follow redirects that are returned by the web server. The `FollowHTTPRedirects` preference defines whether Munki should follow all redirects or only redirect to HTTPS URLs. The possible values for `FollowHTTPRedirects` are:

* ``none`` - This is the default and is the same as Munki's original behaviour. No redirects are followed.
* ``https`` - Only redirects to URLs using HTTPS are followed. Redirects to HTTP URLs are not followed.
* ``all`` - Redirects to both HTTP and HTTPS URLs are followed.

#### Secure Configuration

If there are parts of your Munki configuration you consider sensitive information (for example, repo authentication information, special HTTP headers, or even the Munki repo URLs), instead of storing those preferences in the world-readable `/Library/Preferences/ManagedInstalls.plist` file, you can use a more secure location for some Munki preferences: `/var/root/Library/Preferences/ManagedInstalls.plist`.

Use of this alternate preferences location is completely optional. If you do decide to use it, make sure you fully understand the implications.

Munki uses Apple's `defaults` mechanism to store and access its preferences. Since the core Munki tools run as root, they can access preferences from this file: `/private/var/root/Library/Preferences/ManagedInstalls.plist` as well as the "normal" `/Library/Preferences/ManagedInstalls.plist` file.

Non-admin users of machines managed by Munki will not be able to access or read the contents of `/private/var/root/Library/Preferences/ManagedInstalls.plist`, so this provides some additional security for possibly sensitive preference values.

**Note**: preferences defined in `/var/root/Library/Preferences/ManagedInstalls.plist` have a higher precedence than those defined `/Library/Preferences/ManagedInstalls.plist`, so any preferences set here will override preferences defined in `/Library/Preferences/ManagedInstalls.plist`! This might confuse you or other admins who think only to look in `/Library/Preferences/ManagedInstalls.plist` and forget that some preferences are also defined in `/private/var/root/Library/Preferences/ManagedInstalls.plist`.

With Munki 3.1 or later you can use `sudo managedsoftwareupdate --show-config` to show the effective preferences configuration, no matter where the preferences are defined (/Library/Preferences/ManagedPreferences.plist, /private/var/root/Library/Preferences/ManagedInstalls.plist, or managed preferences).

**VERY IMPORTANT NOTE**: the following preferences are **required** to be defined in `/Library/Preferences/ManagedInstalls.plist` (or set via MCX or configuration profile), as the GUI portion of Munki runs as the logged in user, not root. **Do not** place them in `/var/root/Library/Preferences/ManagedInstalls.plist`, or you may encounter unexpected behavior from Managed Software Center.app, since it can't read the contents of `/var/root/Library/Preferences/ManagedInstalls.plist`:

- ManagedInstallDir
- InstallAppleSoftwareUpdates
- AppleSoftwareUpdatesOnly
- ShowRemovalDetail
- InstallRequiresLogout
- HelpURL

### Editing Munki's preferences

Do not use a text editor or plist editor to edit preferences located at /Library/Preferences/ManagedInstalls.plist or the equivalent files in /var/root/Library/Preferences.  Editing macOS preferences in this way is likely to lead to unexpected or unwanted results, as your changes may be ignored by macOS's preference caching. Instead, if you must manually change the values of one or more Munki preference, use the `defaults` command. This is not unique to Munki -- the same recommendations apply to changing any macOS preference.

If you script the setting of Munki preferences, do not use `PlistBuddy` or any tool designed to manipulate plists, for the same reasons as above. Instead use the `defaults` tool or call the CFPreferences methods in CoreFoundation. (https://developer.apple.com/documentation/corefoundation/preferences_utilities?language=objc)

The other supported way to set and manage Munki's preferences is to use configuration profiles. Be aware that Munki preferences managed via configuration profiles do not result in the values stored in /Library/Preferences/ManagedInstalls.plist or the equivalent files in /var/root/Library/Preferences changing. This is normal, expected behavior for macOS managed preferences.

#### Using the `defaults` command

If you use the `/usr/bin/defaults` command to set values for keys in ManagedInstalls.plist, remember that values default to the "string" type. If you are writing a boolean, integer, or array value, be sure to add the appropriate type flag. For example:

`defaults write /Library/Preferences/ManagedInstalls SuppressAutoInstall -bool false`

See `man defaults` for a complete list of type flags.