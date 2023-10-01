_Notes on using munki with the Adobe CS4 apps_

### Introduction

Notes and examples on how to use munki to install Adobe CS4 apps without repackaging into Apple installer format.

### Details

Using munki with Adobe installer packages requires release 0.4.3 or later of the munki tools.

This is not meant to be a tutorial on the Adobe CS4 Deployment Toolkit; see Adobe's documentation for more on how to get and use the Toolkit to create deployment 'packages'.

Note that an Adobe deployment 'package' is really closer to an Installer ChoiceChangesXML file, or an !InstallShield "answer file", in that it tells the installer what to do in an unattended install. You still need to provide the actual installation payloads. Adobe suggests hosting these on an AFP server, or pre-copying them to the target machine. But for use with munki, you'll want to wrap up the deployment package/packages and the installation payloads into a single disk image.

#### Installing and Uninstalling Adobe CS4 apps

- Use the CS4 Deployment Toolkit to create your deployment 'package':
  - Output is:
    - AdobeUberInstaller
    - AdobeUberInstaller.xml
    - AdobeUberUninstaller
    - AdobeUberInstaller.xml
- Make note of the total installed size reported by the Toolkit; you'll probably want to add this to the pkginfo file later.

- Bundle the deployment package and installation files into a disk image following a very strict format (this is due to a a bug in Adobe's tools when dealing with disk images).

- Here is an example disk layout:

- Adobe Photoshop CS4/           <- top level of DMG; same name as original install DMG volume.
  - AdobeUberInstaller
  - AdobeUberInstaller.xml        <- four files output from CS4 Deployment Toolkit
  - AdobeUberUninstaller
  - AdobeUberInstaller.xml
  - Adobe Photoshop CS4/         <- Install media folder from original disk image (or maybe DVD)
    - resources/
    - payloads/
    - extensions/
    - Deployment/
    - Setup.app
    - Bootstrapper.dmg

- The key is the path to the Setup.app and the installation payloads must be exactly the same as on the original media (disk or disk image) -- the volume name must match and the folder(s) containing the payloads must be at the same relative paths.

- The four AdobeUber files should be either at the root level of the disk image, or one folder down. This allows you to have a single disk image that supports multiple install combinations. You can have multiple Adobe "packages", each in its own root-level directory.
  
- Test the DMG. If it doesn't do the right thing manually, it's not going to work via munki.
  - Copy to test machine
  - Mount the disk image. It should appear under /Volumes with the same name as original media.
  - ``sudo /Volumes/Adobe\ Product\ Name/AdobeUberInstaller``
  - Make sure the install succeeds.
  - ``sudo /Volumes/Adobe\ Product\ Name/AdobeUberUninstaller``
  - Make sure the uninstall is successful.

- Optionally create an uninstaller disk image.
  - This is not strictly necessary. munki can use the installer disk image to do the uninstall. But consider:
    - munki will need to download the disk image, and may require a GB or several GBs of space to cache the image.
    - You can create a slimmed-down diskimage that supports uninstall only; these can be a fraction of the size of the full disk image needed for install.
  - To create a uninstaller disk image, simply create a read/write copy of the installer disk image and delete all the .dmg files in the payloads and extensions directories. Be sure to leave the Bootstrapper.dmg in place, though. Convert the trimmed-down image back to read-only compressed and you should find it takes up less than 10 percent of the space of the intstaller disk image.

- Upload the installer DMG and uninstaller DMG (if applicable) to munki server.
- Use `/usr/bin/munki/makepkginfo` to create a skeleton pkginfo file; manual post-editing will certainly be required. Specifically, you will need to add "installs" items, which you can generate like so:
  - `makepkginfo -f /Applications/Adobe\ Photoshop\ CS4/Adobe\ Photoshop\ CS4.app`
  - munki needs these "installs" items since Adobe "packages" don't leave receipts like standard Apple packages.
- Treat like any other packages managed with munki.

#### Deploying CS4 updates

- Download the update from Adobe's web site.  This should be a DMG containing a Setup.app that does the actual update install.
- Upload the DMG to your munki server.
- Use `/usr/bin/munki/makepkginfo` to create a skeleton pkginfo file; manual post-editing will certainly be required.  Specifically, you will need to add "installs" items, which you can generate like so:
  - `makepkginfo -f /Applications/Adobe\ Photoshop\ CS4/Adobe\ Photoshop\ CS4.app`
  - munki needs these "installs" items since Adobe "packages" don't leave receipts like standard Apple packages.
  - You'll almost certainly need to add "update_for" items as well so munki knows what items can be updated with this updater.
- Treat like any other packages managed with munki.

#### Other resources

Get the CS4 Deployment Toolkit and related documentation here:

http://www.adobe.com/devnet/creativesuite/

More info on the issues with Adobe installers and disk images:

http://managingosx.wordpress.com/2009/10/06/adobe-enterprise-deployment-toolkit-versus-disk-images/