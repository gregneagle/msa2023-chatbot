_Details on using Managed Preferences to configure Munki clients._

### Introduction

The Munki tools support configuration profile (or MCX) management of the Munki configuration. 

> Munki 3.1 new feature <p/> `managedsoftwareupdate` has a new `--show-config` option, which will print Munki's current configuration. This can be helpful when troubleshooting the potentially confusing interaction between different preference levels and managed preferences.

### Details

Since Munki preferences are not user-level preferences, it probably makes the most sense to manage these at the Computer or ComputerGroup level with MCX, or as a Device Profile when using Configuration Profiles.

**Do not** manage the following preferences, or you may see unexpected/undesired behavior:
- InstalledApplePackagesChecksum
- LastAppleSoftwareUpdateCheck
- LastCheckDate
- LastCheckResult
- LastNotifiedDate
- OldestUpdateDays
- PendingUpdateCount

(Note this is not guaranteed to be an exhaustive list. The safest approach always is to manage only those preferences you absolutely need to manage.)

ManagedInstalls keys defined as Managed Preferences take precedence over the same key defined in /var/root/Library/Preferences/ManagedInstalls.plist and /Library/Preferences/ManagedInstalls.plist.

Managed Software Update.app (Munki 1 only) contains an MCX manifest ready for import by Workgroup Manager. This is not included in Munki 2 or 3, but the MCX manifest can be downloaded from [ManagedInstalls.manifest](https://github.com/munki/munki/blob/Munki1/code/Managed%20Software%20Update/ManagedInstalls.manifest) on Munki1 branch of the repository.