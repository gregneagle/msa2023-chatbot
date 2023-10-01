### Introduction

Munki 6 adds support for a new feature to assist in upgrading macOS. This feature copies an "Install macOS" application to /Applications, then notifies the user the upgrade is available in Managed Software Center. When the user clicks "Update", the "Install macOS" application is launched for the user, and admin rights are temporarily added to the user account if needed. This feature allows you to use Munki to assist with an upgrade from one "major" macOS release to a newer one. It is not supported for doing "minor" updates.

### If you are "blocking" macOS upgrades

It's not uncommon for Mac admins to use various tools to block macOS upgrades by blocking the launch of the Install macOS application. Even if they wanted to upgrade their Macs, Mac admins could implement this strategy as way to require users to use Munki/Managed Software Center to perform the upgrade (instead of kicking off the upgrade manually and possibly not having other required updates happen). But since Munki 6's stage_os_installer method relies on launching the actual Install macOS application, you cannot have one of these application blocking mechanisms active -- it would block the launch of the Install macOS application!

### Other macOS upgrade strategies

Munki 3 added support for Apple's `startosinstall` tool to initiate macOS upgrades. This is still supported in Munki 6, but as with Munki 5, it currently works only on Intel Macs. Learn more [here](macOS-Installer-Application-support).

### munkiimport changes

Since an admin could import a macOS installer with the intention of creating a `startosinstall` item or a `stage_os_installer` item, `munkiimport` now has an `--installer-type` option, which is currently supported _only_ for use with macOS installers, and can take a value of one of "startosinstall", "stage_os_installer", or "copy_from_dmg" (the latter would create a pkginfo item that resulted in the "Install macOS" app being copied into /Applications just as it would with, say, Firefox, or Chrome).

### Creating a `stage_os_installer` item

Use  
  `munkiimport --installer-type stage_os_installer /path/to/dmg/containing/Install\ macOS\ Foo.app` or  
  `munkiimport --installer-type stage_os_installer /path/to/Install\ macOS\ Foo.app`  
to generate a pkginfo supporting this new install mechanism (and import the installer). Optionally use `--arch arm64` to limit this to Apple silicon.

### Supporting Intel Macs and Apple silicon Macs

You could use a `stage_os_installer` item on both Intel and Apple silicon, or you could use `supported_architectures` to have two items, both named "InstallVentura" -- one for Intel that uses `startosinstall`, and one for Apple silicon that uses `stage_os_installer`.

It's possible for multiple pkginfos to reference the same installer item, so even if you have a `startosinstall` item and a `stage_os_installer` item for a given macOS installer, the repo needs only a single copy of the macOS installer.

### `stage_os_installer` client-side behavior

There are two "phases" to a `stage_os_installer` installation flow:
  - Download the disk image and copy the app to /Applications (this is nearly identical to the existing copy_from_dmg installer type)
  - Notify the user of a staged OS installer and launch it for the user, temporarily adding admin rights if needed.

The first "phase" can be done as an `unattended_install`. The second phase always requires user interaction and is unaffected by the value of the `unattended_install` field.

The first "phase" can take quite some time. It takes time to download a 12+ gig disk image, to copy the 12+ gig application from the disk image to /Applications, and time to run a "verification" step after the copy. (This verification step shortens the launch time for the initial launch of the app; if we did not do this, the user would have to wait for the verification when they decided to launch the app). This is why I recommend setting "unattended_install" to _True_ for a `stage_os_installer` item. This will allow Munki to do the "staging" phase in the background if possible, so the user is not impacted by the long download/copy/verify tasks.

Once the installer is staged, Managed Software Center will display the pending macOS upgrade for the user to initiate. If they start the install, Munki will add admin rights to the user's account if needed, and launch the installer app (using a wrapper that removes the added admin rights on exit). Munki additionally sets bootstrapping mode so Munki will at least attempt to run on the first boot of the machine under the upgraded OS.

Note: A `stage_os_installer` cannot be forced to install with `force_install_after_date`.  A staged installer needs to launch the OS installer .app in the user space, so the forced install mechanism of Munki to log the user out to force installations counters that method.

### Additional info

As mentioned previously, there are two "phases" to a `stage_os_installer` installation flow:
  - Download the disk image and copy the app to /Applications (this is nearly identical to the existing copy_from_dmg installer type)
  - Notify the user of a staged OS installer and launch it for the user, temporarily adding admin rights if needed.

It's better that the display name and description displayed in Managed Software Center be different for the two phases, and `munkiimport` will help you with that. In addition to the the `display_name` and `description` fields, the pkginfo for `stage_os_installer` items can contain two new fields: `display_name_staged` and `description_staged`. These "take over" for the display_name and description once the item is staged and ready to be launched.

```xml
	<key>description</key>
	<string>Downloads installer for macOS version 13.0 Build 22A5321d</string>
	<key>description_staged</key>
	<string>Installs macOS version 13.0 Build 22A5321d</string>
	<key>display_name</key>
	<string>macOS Ventura beta installer</string>
	<key>display_name_staged</key>
	<string>Install macOS Ventura beta</string>
```

You can modify the display names and descriptions to meet your needs.

### Getting the macOS installer application

Some ways to get the "Install macOS" application:
- App Store
- `softwareupdate --fetch-full-installer` (See `man softwareupdate` for more info on this option)
- https://github.com/munki/macadmin-scripts/blob/main/installinstallmacos.py
- I'm quite sure there are other methods and tools

### More notes

Untested, but these pkginfo keys should work (though maybe not as you might expect):
- `update_for`
- `requires`
- `preinstall_script`
- `postinstall_script`

All of those will be processed as part of the "staging" phase; in other words, a preinstall_script would be run right before the "Install macOS" application is copied to /Applications; similarly, a postinstall_script would be run right _after_ the application is copied to /Applications. None of these items would be processed or executed as part of the launching of the staged "Install macOS" application.

#### Update vs Upgrade

Just as with `startosinstall` there is no support for using this method to do minor OS updates (for example: macOS 12.6.2 to macOS 12.6.3). It is intended and supported for major OS _upgrades_ only (for example: macOS 11.x to macOS 13.x).

#### Uninstalling

By default, a `stage_os_installer` item is marked with `uninstallable` = `True` and `uninstall_method` = `remove_copied_items`. This means only that a staged macOS installer application can be removed before the actual install is triggered -- it does not mean that you can downgrade macOS.

### Alternate optional install workflows

One requested/desired workflow is this: have Munki pre-stage the macOS installer, ready to go. Then an "Install macOS Foo" item can be an optional install that can be triggered quickly, without the user waiting for the download of the installer (and possibly also the lengthy copy and verfication stage.)

With startosinstall items, this can be achieved by adding the item to optional_installs and also marking it with `precache` as True (More info on [precache](Pkginfo-Files#precache)). Munki will precache the disk image containing the installer in its download cache folder. If/when the user selects the item for install from Managed Software Center's optional installs, the user does not have to wait for the download of the item, and the install can commence nearly immediately.

With stage_os_installer items, `precache` also works to avoid the download wait. But there is also a need to copy the installer to /Applications (or at least to local disk) and to run a "verification" step. `precache` alone cannot also perform those additional steps.

The solution here is _two_ Munki items that work together. The first is a copy_from_dmg item with a postinstall_script. The needed script for a Ventura install is:

```sh
#!/bin/sh

"/Applications/Install macOS Ventura.app/Contents/Resources/startosinstall" --usage
```

You'd import the installer as a copy_from_dmg item like so:

```
munkiimport --installer-type copy_from_dmg /path/to/VenturaInstaller.dmg
```

You'd add this item to managed_installs. Munki would then download the disk image, copy the Install macOS Ventura application to /Applications, and trigger the verification. The application would then remain in /Applications, waiting to be launched.

The second item would be the stage_os_installer item. You'd put this item in optional_installs. Once selected for install, if the Install macOS application is already in /Applications, the download, copy, and verify steps would be skipped, and it would proceed directly to launching the Install macOS application. If the Install macOS application has not yet been staged in /Applications, it would be downloaded, copied and verified first.