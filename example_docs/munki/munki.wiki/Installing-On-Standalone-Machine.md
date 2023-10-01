**NOTE: These instructions are no longer current and are considered deprecated. This document remains for historical reasons only. For instructions on setting up a demonstration Munki server and client, see [[DemonstrationSetup|Demonstration-Setup]]**

These instructions describe how to install and configure Munki to work on a single machine (tested with Mac OS X 10.6.2 Client). For demonstration purposes, we'll be deploying Firefox. This is useful for testing, but is not recommended for production use.

# Server Setup

1. Turn on Web Sharing
1. Check System Preferences -> Sharing -> Web Sharing
1. Download and install Munki Package
1. Create server directory structure
1. Open Terminal.app
1. `cd`
1. `mkdir Sites/munki Sites/munki/catalogs Sites/munki/manifests Sites/munki/pkgs Sites/munki/pkgsinfo`
1. Copy Firefox disk image to Sites/munki/pkgs
1. Give webserver permission to read disk image
1. `chmod 644 Sites/munki/pkgs/[1. Create pkginfo file for package
1. `/usr/local/munki/makepkginfo Sites/munki/pkgs/[NAME_OF_DISK_IMAGE](NAME_OF_DISK_IMAGE]`) > Sites/munki/pkgsinfo/[1. Create catalog
1. `/usr/local/munki/makecatalogs Sites/munki`
1. Create a testing manifest at Sites/munki/manifests/testing. (Be careful about the name of the manifest file -- for this example we're naming it "testing" with no filename extension.)
3a18f66e57c114e5d5346e2ff484c45e

# Client Setup

1. Edit /Library/Preferences/!ManagedInstalls.plist
1. Set !ClientIdentifier to testing
1. Set SoftwareRepoURL to http://localhost/~USERNAME/munki where USERNAME is the short name of your user account.

It might be easiest to use the `defaults` command for this:

    defaults write /Library/Preferences/ManagedInstalls ClientIdentifier testing
    defaults write /Library/Preferences/ManagedInstalls SoftwareRepoURL http://localhost/~USERNAME/munki

# Running the Client Tools

1. `sudo /usr/local/munki/managedsoftwareupdate` <br>- or -<br>
1. Launch /Applications/Utilities/Managed Software Update.app

# Updating Software

 ==On the Server==
1. Copy new version of Firefox disk image to Sites/munki/pkgs
1. Create pkginfo file for new package
1. `/usr/local/munki/makepkginfo ~/Sites/munki/pkgs/[NAME_OF_DISK_IMAGE](NAME_OF_DISK_IMAGE].pkginfo`) > ~/Sites/munki/pkgsinfo/[NAME_OF_DISK_IMAGE].pkginfo`
1. Create catalog
1. `/usr/local/munki/makecatalogs ~/Sites/munki`
 ==On the Client==
1. Launch /Applications/Utilities/Managed Software Update.app

# More info

For a more in-depth introduction to Munki, see these !MacTech articles:

http://www.mactech.com/articles/mactech/Vol.26/26.10/2610MacEnterprise-ManagingSoftwareInstallswithMunki/index.html<br>
http://www.mactech.com/articles/mactech/Vol.26/26.11/2611MacEnterprise-ManagingSoftwareInstallswithMunki-Part2/index.html<br>
http://www.mactech.com/articles/mactech/Vol.26/26.12/2612MacEnterprise-ManagingSoftwareInstallswithMunki-Part3/index.html<br>
http://www.mactech.com/articles/mactech/Vol.27/27.01/2701MacEnterprise-ManagingSoftwareInstallswithMunki-Part4/index.html