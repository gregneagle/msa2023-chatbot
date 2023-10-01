### Introduction

Munki can be configured to install available Apple Software Updates, with the benefit that users don't need to be administrators to install updates.

### Recent developments

Due to changes in Apple's softwareupdate, Munki can currently only install a subset of Apple updates on Intel, and no updates at all on Apple silicon. See https://github.com/munki/munki/wiki/manual-apple-updates-in-Munki-5 for some of the changes that affect Mojave+ on Intel.

### Details

To install Apple Software Updates with Munki, set InstallAppleSoftwareUpdates to True in [[Munki's preferences|Preferences]]:

```xml
<key>InstallAppleSoftwareUpdates</key>
<true/>
```

Or using defaults:

```bash
defaults write /Library/Preferences/ManagedInstalls InstallAppleSoftwareUpdates -bool True
```

or via equivalent configuration profile.

To set a custom CatalogURL for Apple Software Updates, you can use `defaults` or a configuration profile to manage `com.apple.SoftwareUpdate`:

```bash
defaults write /Library/Preferences/com.apple.SoftwareUpdate CatalogURL "http://applesus.myorg.org:8088/index-leopard-snowleopard.merged-1.sucatalog"
```

#### Apple items in the Munki repo

Munki updates and Apple Software updates can appear and be installed in the same Munki session. To prevent possible conflicts, if any item to be installed or removed from the Munki server is identified as an "Apple item", Apple software updates will not be processed in the same Munki session. 

This behavior prevents Munki from displaying a pending upgrade to macOS Catalina that you've imported into Munki _and_ a macOS 10.14.6 Supplemental Update in the same list of pending updates.

An item from the Munki repo is identified as an Apple item if it has the optional `apple_item` key set to `True` in its pkginfo file. Additionally, an item will be treated as an `apple_item` during an update check if the `apple_item` key is not present and the item contains either a `receipts` array with a `packageid` key that starts with `com.apple` or an `installs` array with a `CFBundleIdentifier` key that starts with `com.apple`.

It is important to note that any Apple application scheduled for install without an `apple_item` key explicitly set to `False` will cause the item to be treated as an `apple_item` during an update check. The implication of this is that if a user has an update waiting to be installed for Pages, as an example, and the Pages update has no `apple_item` key set _no Apple software update checks will be performed_ for as long as the user postpones the Pages update.

In this scenario, this means that if any important Apple software updates (Security Update, macOS update) became available after the user first received the Pages update they will not be available for install until after Pages is installed. If an important macOS update has also been given a `force_install_date` by the admin via the `apple_update_metadata` method and the user doesn't install the waiting Pages until after the forced date expires, before long Managed Software Center will initiate the final one hour grace period countdown and logout to install the waiting Apple update. This may be a problem from a UX point of view and makes directly managing the `apple_item` key very important in order to prevent long periods of Apple software update "blackout" for users who tend to postpone waiting updates for long periods on end, or any surprises arising from passed forced install deadlines.

In order to prevent such a blackout the admin has two options:
- Mark all Apple updates in Munki as unattended where possible
- Set the `apple_item` key to `<false/>` in any Apple item's pkginfo file

For additional notes on the `apple_item` key see [this section](https://github.com/munki/munki/wiki/Installing-macOS#pkginfo-notes) of the Munki wiki.

#### Apple Update Metadata

Munki supports admin-provided additional metadata for Apple updates, which allows admins to better control the timing and conditions of Apple updates.  **Adding metadata information for an Apple update cannot cause Munki to offer any update Apple Software Update will not offer.** It can only change *how* the update, if available from Apple Software Update, is installed. It can allow Munki to install an Apple update in an unattended manner; it can require a logout or restart even if the update normally would not require these, or it can be force installed after a certain date. Again, if Software Update is not offering the item to the client, Apple Update Metadata cannot force it to do so.

More info on Apple Update Metadata is [[Pkginfo For Apple Software Updates|Pkginfo-For-Apple-Software-Updates]].

#### Unattended Apple Updates

The most common use for Apple Update Metadata has been to mark updates as unattended so that Munki will install them in the background.

With the 2.5.0 release of the Munki tools (and on OS X Yosemite or later), setting UnattendedAppleUpdates to true in Munki's preferences will cause Munki to automatically install all possible Apple updates in the background without notifying the user, such as iTunes, Safari, and Command Line Tools updates.  Updates requiring a reboot will be ignored by this setting, and blocking applications are automatically extracted from the update's distribution file.  This generally alleviates the need to create the metadata specified above unless there is a need for using `force_install_by_date`

```xml
<key>UnattendedAppleUpdates</key>
<true/>
```

#### Using the Munki tools only to install Apple Software Updates

You can use the Munki tools without any Munki repository to install Apple updates. In /Library/Preferences/ManagedPreferences.plist, set `AppleSoftwareUpdatesOnly` to True. 

```bash
defaults write /Library/Preferences/ManagedInstalls AppleSoftwareUpdatesOnly -bool True
```

managedsoftwareupdate will then not request a manifest and catalog(s) from a Munki server, but will proceed directly to checking for (and possibly installing) Apple Software Updates.

Apple Update Metadata functionality is not available with this configuration, since the additional metadata is stored in a Munki repo.

### OS-specific notes

#### Pre-10.11 notes (10.10 and below)

For OS X versions prior to 10.11, you may also direct Munki to use a different Apple Software Update server (for example, one you host internally) by setting the SoftwareUpdateServerURL key in Munki's preferences to the appropriate CatalogURL:

```xml
<key>SoftwareUpdateServerURL</key>
<string>http://applesus.myorg.org:8088/index-leopard-snowleopard.merged-1.sucatalog</string>
```

or again with the defaults command:

```bash
defaults write /Library/Preferences/ManagedInstalls SoftwareUpdateServerURL "http://applesus.myorg.org:8088/index-leopard-snowleopard.merged-1.sucatalog"
```

(Beginning with OS X 10.11, setting this value is not currently recommended)

#### Mavericks (macOS 10.9) and Yosemite (macOS 10.10) notes

Due to changes in how the `/usr/sbin/softwareupdate` tool works in OS X 10.9 and 10.10, you may have unexpected/undesirable results if you use MCX or configuration profiles to manage the `CatalogURL` in `com.apple.SoftwareUpdate`. See this discussion: https://groups.google.com/d/topic/munki-dev/fxnOkoweSIo/discussion

As an alternative to managing this preference with MCX or configuration profiles, consider just directly setting your desired `CatalogURL` in `/Library/Preferences/com.apple.SoftwareUpdate.plist`.

#### macOS 10.11 (El Capitan) and later notes

Due to changes in how the `/usr/sbin/softwareupdate` tool works in OS X 10.11 and later, it is no longer recommended to set SoftwareUpdateServerURL in Munki's preferences. Instead you should just allow Munki to use whatever Apple Software Update is using "normally" -- either the system defaults, or a CatalogURL value set in the com.apple.SoftwareUpdate preferences domain.

With the 2.8.0 release of the Munki tools, the SoftwareUpdateServerURL, if set, will be _ignored_ under 10.11+.

Unlike with earlier versions of macOS/OS X, under macOS 10.11+, due to the changed implementation, it's fine to manage com.apple.SoftwareUpdate's CatalogURL using a configuration profile (or MCX!).

#### macOS 10.14 and later notes

See [Manual Apple Updates](manual-apple-updates-in-Munki-5).