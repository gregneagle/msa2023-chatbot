![](https://github.com/munki/munki/wiki/images/managed_software_center.png)
### What Munki Does

Munki consists of client-side tools written largely in Python, and is available as open-source under the Apache 2 license. Munki currently supports macOS 10.13 and later. (The OS requirements for earlier versions of Munki are [listed on the Getting Started page](https://github.com/munki/munki/wiki#munki-versions).)

On the server side, Munki can use any web server. You can use any available modern web server on any platform. (I say "modern" because some software packages can be over 2GB in size and older web servers have problems serving files of that size.) You do not need to install any Munki-specific software on the web server, but you must be able to create directories and files on the web server.

Munki can install software delivered as standard Apple packages - the same kind of packages, that when double-clicked, open in Apple's Installer.app. Munki can also install software from disk images - for example, an application delivered on a disk image that is supposed to be dragged to the Applications folder. These "drag-n-drop disk images" are easily installed by Munki. Munki also knows how to install many Adobe products. In many cases, Munki can also remove the software it has installed.

Munki also supports "Optional Software". These are items that are made available to the users of machines you manage, who can decide for themselves whether or not they'd like any of these items installed. If they choose to install an optional software item, they can also later remove it. This feature does not require admin rights for the user, and is similar in concept to "Self Service" installs offered by the commercial product Jamf Pro.

Additionally, Munki can update software it did not install itself. You can specify that certain software should be updated only if some version is found already installed on a user's machine.

Finally, Munki can be configured to install Apple Software Updates. This allows users without admin rights to be able to install available Apple updates. See [here](Apple-Software-Updates-With-Munki) for more information.

### What Munki Doesn't Do

Many of the commercial solutions for software deployment also provide solutions for other facets of Mac management. Munki does not. Munki focuses only on software deployment. You'll need to turn to other tools for imaging, inventory, remote assistance, and preference management.

See [here](https://github.com/munki/munki/wiki/More-Links-And-Tools#reportingweb-consoles) for some Web consoles that do inventory and reporting and integrate nicely with Munki.

### Munki Pieces

Most of the data munki needs to function is stored on a web server. Munki uses three types of data:

**Installer items**: these are packages or disk images containing the software to be installed. In many cases, you can use a package or disk image provided by the software vendor without having to repackage or convert the installer package in any way. For example, munki can install Firefox from the disk image that you download from http://www.mozilla.com. Sometimes these are just referred to as "packages", but in actuality Munki can install from things that aren't strictly Apple Installer packages.

**Catalogs**: these are lists of available software, containing metadata about the installer items. You, as the Munki administrator, build these catalogs using tools provided with Munki. Catalogs are usually built from individual files, called "pkginfo" files, that describe the metadata for a single installer item. Learn more about pkginfo files [here](Pkginfo-Files). The `makecatalogs` tool is used to build catalogs from pkginfo files. Learn more about makecatalogs [here](Makecatalogs).

**Manifests**: A manifest is essentially a list of what software should be installed on or removed from a given machine. You could have a different manifest for every machine, or one manifest for all of your machines. Manifests can include the contents of other manifests, allowing you to group software for easy addition to client manifests. For example, you could create a manifest listing all of the software every machine in your organization must have. The manifest for a client could then include the common-software manifest, and additionally have software unique to that client. Learn more about manifests [here](Manifests).

Manifests and catalogs are stored on the web server as standard Apple plist files in text format. pkginfo files are also plist-formatted files. If you've administered Mac OS X machines, you've almost certainly encountered plist files. They are a well-understood way to store structured data in a text format.

### Munki Behaviors

Since a Munki server is just a web server serving static files, all of the "smarts" of Munki reside in the client software on each machine.

By default, when installed and configured, the `managedsoftwareupdate` process runs in the background approximately once an hour. It looks for changes on the server, downloading new or changed manifests and catalogs. It then uses the manifests and catalogs to determine what is supposed to be installed or removed from the user's machine. If anything needs to be installed, it is downloaded in the background. All of this is done in the background without involving the user. If there are any changes that need to be made, what Munki does next depends on whether or not there is a user logged in.

If there is no user logged in, by default, Munki proceeds to install or remove the required software without asking. It displays a status window over the loginwindow, effectively preventing users from logging in until the updates are complete. If any of the updates require a restart, Munki will restart the machine at the end of its session.

If there is a user logged in, Munki will launch Managed Software Center to notify the user of available updates. (Munki won't notify the user of the same updates more than once a day, however.) The user is then in control - he or she can elect to perform the updates right away, or defer them until later.

If the user chooses to perform the updates, there are a couple of possibilities. If any of the updates require a logout or restart, the only choice available will be to logout and update. If none of the updates require a logout or restart, the user can install the updates immediately.

Administrators can customize these behaviors, configuring Munki to never bother the user with available updates (therefore waiting to install all updates when no user is logged in), or the inverse - telling Munki to never automatically install software when at the loginwindow, and instead always requiring user consent for all updates.

Administrators can also mark some updates as safe to install without user confirmation; these usually include a list of "blocking_applications" so that Munki won't try to automatically update software that is in use. See [here](https://github.com/munki/munki/wiki/Pkginfo-Files#unattended-installs-and-uninstalls) for additional information on Munki's support for unattended installs and removals.

It's sometimes necessary for Munki to be more aggressive: there may be reasons that a given piece of software or an update must be installed by some deadline. See [here](https://github.com/munki/munki/wiki/Pkginfo-Files#force-install-after-date) for more information about Munki's ability to "force" some installs.