> **NOTE:** As of the Munki 5.7 release, the Munki tools package does not require a restart unless you are upgrading from a very old release of Munki (3.x or earlier). This page remains here for historical documentation.


A point of pain for some Munki admins is that the munkitools package requires a restart. Any package that requires a restart can be more difficult to install, as it is more disruptive and often requires end-user cooperation.

#### Why a restart?
The need for a restart was originally driven by the need for several LaunchDaemons and LaunchAgents for Munki to be able to do its job. On a restart, all previously existing LaunchDameons and LaunchAgents are stopped and unloaded, and all currently existing LaunchDameons and LaunchAgents are loaded and started. This is a clean and robust way to ensure the correct versions of the correct jobs are running, and works across all supported versions of macOS without the need for scripting.

#### Avoiding a restart(?)
It is possible via package scripting (preinstall and postinstall scripts) to unload and load LaunchDaemons, and with very careful scripting, also unload and load user-level LaunchAgents, but there are some challenges here.

* First: various versions of Munki contain different sets of LaunchDaemons and LaunchAgents. A script that wants to ensure the correct LaunchDaemons and LaunchAgents are running after install needs to know Munki's entire history of LaunchDaemons and LaunchAgents to ensure any of these items that might have been installed in the past are stopped and unloaded before install of the current version.  
* Second, and more significant: Since these LaunchDaemons and LaunchAgents control Munki itself, a package script that stops or removes out-of-date LaunchDaemons and LaunchAgents will kill the Munki session attempting to install the updated Munki tools. This means that Munki cannot update its own LaunchDaemons without requiring a restart.

#### Updating Munkitools
Fortunately the Munki LaunchDaemons do not change often, and so it is usually possible to update the Munki tools by installing all the subpackages _except_ for the launchd package, avoiding the need for a restart.

This led to the common strategy used by Munki admins to upgrade Munki on their fleet: decompose the Munki distribution (meta)package into its component packages and import _those_ into Munki. Since only the munkitools_launchd component package requires a restart, and since Munki can determine whether or not it needs to be installed, a Munki tools update that does not include an updated launchd component package can be installed without needing a restart. See [[Updating Munki Tools]] for more information.

#### Deploying Munki
Traditional deployment workflows that utilized NetBoot or booting from an alternate volume, like using NetRestore, NetInstall, DeployStudio or Imagr, or even newer alternatives like Bootstrappr and Installr are not negatively impacted by the need to reboot, since the packages are being installed to volume other than the current boot volume as part of the initial setup process (Installr does have issues with the High Sierra Installer not honoring RestartRequired key in packages). When the machine eventually boots into the newly configured OS volume, the Munki components are already in place and the launchd jobs load and run without need for yet another restart.

#### Deployment changes
But many organizations have moved or are moving to deployment workflows utilizing DEP and MDM. In these workflows, the Munki tools may be installed during or shortly after the Setup Assistant that appears on first boot of a new machine. These workflows don't really have a UI/UX for installed packages that need a reboot for full functionality. So you either have a partially-broken Munki install until the machine is eventually rebooted, or some script/tool created by the admin has to do the reboot. Neither is an appealing prospect.

#### DEP-triggered workflow
Erik Gomez created an alternate Munki package building script for this workflow, which has been incorporated into the [make_munki_mpkg.sh](https://github.com/munki/munki/blob/main/code/tools/make_munki_mpkg.sh) script. It contains scripts to load the Munki LaunchDaemons. Once the GUI user logs in, the appropriate LaunchAgents are loaded as well. This is a better UX for DEP-triggered Munki enrollments. For more information about the `make_munki_mpkg.sh` script, see [[Building Munki packages]].

#### Munki 5.7+
Starting with the Munki 5.7 release, the provided package should install and activate Munki's launch daemons and launch agents without requiring a restart _on a fresh install_. It should be suitable for most initial deployment scenarios, including those driven by DEP/ADE. A restart is still required if a Munki update changes the launchd pkg (and therefore the launchd jobs themselves).
