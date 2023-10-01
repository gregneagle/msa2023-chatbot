### Introduction

Many Mac administrators have adapted a modular approach to imaging using tools like InstaDMG or Apple's System Image Utility. The "modules" of the modular approach are Apple packages, and these tools build installation images using these packages.

If you are using Munki, you might consider making your images very "thin" and using Munki to bootstrap a machine's configuration.


### Details

The concept here is simple. Instead of a lengthy process of building an installation image from a great number of packages, you build a "thin" image that consists of the OS, perhaps an admin account, and the Munki tools. You restore the image to the target machine, and upon reboot, the Munki tools take over and complete the configuration of the machine by installing all the rest of the software your organization needs, including the majority of your configuration packages.

The "thin" image needs to have only enough to allow the target machine to boot and run the Munki tools; Munki installs everything else, including any needed Apple Software Updates.

To cause Munki to check for updates and install at startup, make sure the file **`/Users/Shared/.com.googlecode.munki.checkandinstallatstartup`** exists. You can create a package that installs that file and make it part of your thin image, or you can have a script `touch` that file.

A package that installs the required file is available here: https://github.com/munki/contrib/blob/master/munki_kickstart.pkg?raw=true

When `/Users/Shared/.com.googlecode.munki.checkandinstallatstartup` exists, Munki will check for and install updates. If a reboot is required after installing updates, after the reboot, Munki will check and install again, continuing until there are no updates to be installed. This allows you to bootstrap the configuration of a machine, including installing Apple Software Updates, with no user intervention.

**Pros -** Some advantages of this approach:

1. Less duplication of effort. You don't need to add packages to both Munki and a modular disk image workflow.
1. More packages work. There are a non-insignificant number of packages that fail to install correctly in a modular imaging workflow because scripts within these packages make invalid assumptions. Munki installs packages to the current startup disk, which is more likely to result in success with these problematic packages.
1. Can be used with a "no imaging" approach. Taking the "thin imaging" concept one step further, you may be able to deploy machines without imaging at all. This begins with taking a new Mac out of the box, using the image installed on it at the factory. You install the Munki tools only, and allow Munki to reconfigure the machine to your standard. This approach allows you to rapidly deploy new hardware releases from Apple without needed to take the time and resources to build a new deployment image.

**Cons -** Some disadvantages of this approach:

1. Slower. Configuring a machine this way is much slower than block-copying a "pre-compiled" modular image built with AutoDMG, SIU or similar tools.
1. Timing when integrating with other tools. For example, DeployStudio has post-imaging tasks run on the first reboot after being run on a computer. If Munki was set to run on the first reboot as well, the DeployStudio scripts could reboot the machine in the middle of a Munki run. The solution in this case is to make the creation of the `/Users/Shared/.com.googlecode.munki.checkandinstallatstartup` file one of the tasks DeployStudio performs after the first reboot. When DeployStudio reboots the machine again, Munki will run on the second reboot.
1. Network connectivity, in specific to the configured munki server, is required. In environments where connectivity is not guaranteed at the login window, 'looping' as failed attempts are retried may obstruct end users from logging in. Support personnel should recognize that the app which provides that progress bar, MunkiStatus, can be quit with Cmd-Option-Shift-Escape as a workaround if connection cannot be established.

### Munki 3.1 changes

Munki 3.1 contains changes to improve the bootstrapping experience on machines encrypted with FileVault 2.

`managedsoftwareupdate` has two new options: `--set-bootstrap-mode` and `--clear-bootstrap-mode`.

`managedsoftwareupdate --set-bootstrap-mode` creates the needed `/Users/Shared/.com.googlecode.munki.checkandinstallatstartup` file, and also turns off FileVault auto login (this is the automatic login to the account of the user who unlocks the FV2-encrpyted disk at boot), by setting the com.apple.loginwindow DisableFDEAutoLogin preference to True. (See deprecated [Apple support article HT202842](https://web.archive.org/web/20190408214404/https://support.apple.com/en-us/HT202842).)

`managedsoftwareupdate --clear-bootstrap-mode` removes the `/Users/Shared/.com.googlecode.munki.checkandinstallatstartup` file and resets the com.apple.loginwindow DisableFDEAutoLogin preference to its previous value.

When performing a macOS upgrade (using an Install macOS.app/startosinstall), Munki uses these new mechanisms in order to effectively re-bootstrap after an OS upgrade. 

Previously, on a FileVault 2-encrypted machine, after the upgrade was complete, the user would need to unlock the startup disk in order to boot into the newly-upgraded OS. After unlocking the startup disk with the user's login password, the OS would normally continue logging into the user's account, bypassing the loginwindow. This resulted in the re-bootstrapping (Munki running to check for and install all needed updates for the new OS) not happening properly. With the changes in Munki 3.1, the automatic account login is temporarily suppressed, allowing Munki the opportunity to run over the loginwindow after the macOS upgrade is complete.

You probably won't need to use/care about these changes when bootstrapping a brand-new machine, since it most likely will not have FileVault 2 turned on, but if for some reason you do, you can use `managedsoftwareupdate --set-bootstrap-mode` to set up bootstrapping mode.