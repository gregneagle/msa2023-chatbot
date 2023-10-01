_Built-in support for the import and use of macOS Installer applications to perform macOS upgrades_

### Introduction

Munki 3 adds "native" support for using the `startosinstall` tool – included inside the macOS installer application since 10.11 – to install macOS upgrades. This allows you to use Munki to upgrade a Mac from one "major" macOS release to a newer one. It is not supported for doing "minor" updates.

Munki's support for `startosinstall` is limited to Intel Macs. To upgrade macOS on Apple silicon, use the [`stage_os_installer` method](Staging-macOS-Installers), introduced in Munki 6.

### Background

Prior to the release of Munki 3, the supported method of performing OS upgrades was to use the [`createOSXinstallPkg` toolset](https://github.com/munki/createOSXinstallPkg) to create an installer package from an "Install macOS Foo.app" application. You'd then import the installer package and manage it like any other package.

10.12.4 dealt a serious blow to the [`createOSXinstallPkg` toolset](https://github.com/munki/createOSXinstallPkg): Apple changes made it now impossible to include additional packages as part of the install. Additionally, Apple changed the location and functionality of `brtool`, a tool used to set up the macOS install boot on CoreStorage volumes. With some effort, basic functionality of `createOSXinstallPkg` is working again under 10.12.4 (and later), but it appears that the ability to add additional packages is lost forever due to new security measures by Apple. (10.13 changes further break `createOSXinstallPkg` and there is no plan to address these changes.)

In addition, if one examines the contents of the `/macOS Install Data` folder after a 10.12 `createOSXinstallPkg` package completes preparation for a macOS install, and compares that to the contents of the `/macOS Install Data` folder after `startosinstall` completes preparation for a macOS install, it's clear that `createOSXinstallPkg` does not set things up the same way -- that over time, Apple has changed details of the set up process, and `createOSXinstallPkg` has not kept pace.

Given the breakage and the pace of change, it seemed prudent to focus efforts on a mechanism that is at least somewhat-Apple supported, even if it provides less flexibility and functionality than `createOSXinstallPkg` did.

#### Importing a macOS installer

`munkiimport`, `makepkginfo`, and `iconimporter` now have support for macOS installers.

Use `munkiimport /Applications/Install macOS Sierra.app` to wrap the installer in a disk image and import it into your Munki repo. You may also import an existing diskimage containing a copy of "Install macOS Sierra.app".

Add the item to a manifest as you would any other Munki item.

#### Avoiding Unsupported Hardware

Munki will gladly offer the OS install on hardware that is not capable of running that particular release, if you add the item to managed_installs or optional_installs. You can use logic like the one found [here for Mojave](https://github.com/hjuutilainen/adminscripts/blob/master/check-10.14-mojave-compatibility.py) to do a [conditional item](https://github.com/munki/munki/wiki/Conditional-Items) and prevent this from looping at the worst, or polluting logs with errors and warnings at the least. An alternative implementation is here: https://github.com/munki/munki-facts/blob/master/facts/mojave_upgrade_supported.py

#### Munki 3.1 changes

`startosinstall` OS upgrade pkginfo items can now contain an additional array of strings, which are added as additional options to the startosinstall binary. For example:

    <key>additional_startosinstall_options</key>
    <array>
        <string>--converttoapfs</string>
        <string>NO</string>
    </array>

No guarantees that these additional options will actually _work_ or be supported by Apple in future releases; testing is your responsibility, bugs are Apple's.

### Implementation notes

You don't need to add installs items or receipts to the pkginfo item for an imported Install macOS Sierra.app. Munki knows how to tell if the target Mac already has the same major.minor (or a higher major.minor) version installed.

In the vein of https://github.com/munki/munki/wiki/How-Munki-Decides-What-Needs-To-Be-Installed -- Munki simply checks the major.minor OS version. If your `startosinstall` item installs 10.12.4, any version of macOS 10.12 is enough to satisfy Munki. This prevents Munki from offering a 45-minute install of 10.12.4 to machines running 10.12-10.12.3 and "masking" a softwareupdate Delta/Combo Update to 10.12.4. (This also matches the behavior you would get when using a package built with `createosxinstallpkg` and this installs array: https://github.com/munki/munki/wiki/Installing-macOS#sierra)

A macOS installer that is a pending update will be installed after all other items in managed_installs. It's automatically considered an apple_item, so Apple software updates will not be checked for or installed in the same  session.

As with other Munki items that require a restart after install, Managed Software Center will trigger a logout before starting the install session. All other pending managed_installs will be installed first; the macOS upgrade will be started last. If `startosinstall` completes successfully, it will trigger a reboot. Munki will exit after doing a subset of the actions it normally does at the end of a Munki run. Currently that includes running a postflight script (if one exists) with a special runtype of "startosinstall".

Before the reboot, however, Munki will create the `/Users/Shared/.com.googlecode.munki.checkandinstallatstartup` file, which will cause Munki to enter "bootstrapping mode" after the OS upgrade is complete. See [[Bootstrapping With Munki]] for more detail on this subject.

#### Marking other items as `update_for` a macOS install
Nothing prevents you from defining other Munki items as 'update_for' a `startosinstall` item, but such items will _not_ be installed during the same session in which the macOS upgrade is started; instead they will be re-evaluated (and possibly installed) during the "bootstrapping mode" after the OS upgrade is complete. (If your item that installs Sierra is conditionally offered only to machines running < 10.12, though, it will no longer be in managed_installs after the OS upgrade is complete, and "update_for" items will not be processed at all.)

#### Supported versions
Sierra through Monterey installers are supported; `startosinstall` was added in El Capitan, but the syntax and behavior is different and testing showed that quite a lot of additional code would need to be written to attempt to get a acceptable experience and success rate with El Capitan installs. Using `createosxinstallpkg` will continue to be the recommendation for El Capitan and earlier OS installs.  

#### preinstall_script and postinstall_script
Preinstall and postinstall script support is present, but currently untested. Note that a postinstall_script will actually run after the macOS upgrade is set up, but before the OS is actually installed/upgraded. If you need a script to run after the the OS is upgraded, you'll need to use "requires" to install the script as something that runs at boot (one time only perhaps) _before_ you start the macOS update. The "outset" tool or a similar mechanism might be a good choice for this task.

### More questions and answers

- Can I use this feature to upgrade Apple silicon Macs from Big Sur to Monterey?
  - No. On Apple silicon, `startosinstall` requires credentials of a local "volume owner" user. Munki currently has no way to collect and provide those credentials. (Munki 6 provides a [different way](Staging-macOS-Installers) for Munki to assist in macOS upgrades that does work on Apple silicon.)

- What OS versions are supported for running `startosinstall`?  
   - Sierra (10.12.x) - Monterey (12.x). Not all combinations of older OS and OS-to-upgrade-to work: you might not be able to upgrade directly from say, 10.10 to Big Sur. Consult Apple documentation on supported upgrade paths.

- Which "Install macOS/OS X" applications actually work with this implementation, especially at the loginwindow (with no active user session)?  
  - The Sierra (10.12.4-10.12.6), High Sierra (10.13+), Mojave (10.14+), Catalina (10.15+), and Big Sur (11.x) installers are known to work. Use the [`createOSXinstallPkg` tool](https://github.com/munki/createOSXinstallPkg) to create installer packages for older versions of macOS/OS X.

- Is there an easier way to get the Install macOS application than using the App Store? I keep getting the "stub" or "shell" application that doesn't contain all the needed resources.
  - You might find this tool useful to get High Sierra and later installers: https://github.com/munki/macadmin-scripts/blob/master/installinstallmacos.py 