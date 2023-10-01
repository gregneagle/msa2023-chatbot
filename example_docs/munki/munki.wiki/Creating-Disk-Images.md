### Introduction

At times, an install requires several source items to be wrapped in a single container for proper installation. In addition, if an installer is old enough to be a bundle-style package, munki requires it to be encapsulated in a disk image. This has the effect of converting a bundle-style package, which is actually a special type of folder containing additional folders and files, into a single compressed file. This makes uploading and downloading such a package from a web server much more convenient and compatible with a wider range of web servers. This document explains how to create a disk image in a way that works more optimally with munki.

### Summary

`munkiimport` will wrap bundle-style packages, metapackages and drag-drop applications in disk images for you. You generally need not do anything other than:

`munkiimport /path/to/the/item`

If you need to create a disk image because scripts in installers expect source files to be found at relative paths, see the 'Manually creating a disk image' section below.

#### What is a bundle package?

Since the release of Mac OS X 10.5 (Leopard), there have been two major formats for Apple Installer packages. Leopard introduced a new "flat" style of package, where the package is a single file. But prior to Leopard, all packages were "bundle-style" packages, consisting of a directory of files and folders. This style of package still works in Leopard and Snow Leopard, and is required for use with Tiger and earlier OSes, so it is still the most common style of package to be found.

#### Identifying a bundle package

**How can you tell if a given package is a "bundle-style" package?**

- From the Finder, control-click on the package to get a contextual menu. If "Show Package Contents" appears in the menu, the package is a bundle-style package. Otherwise, the package is a "flat" package.

- From the command-line, either attempt to `cd` into the package, or perform an `ls -al` on the directory containing the package. If you can `cd` into the package or it displays as a directory in an extended listing, it is a bundle-style package

**I still can't tell for some reason...**

- Then wrap it in a disk image anyway. Bundle-style packages must be wrapped in a disk image file. Flat packages are not required to be encapsulated in a disk image, but will work fine if they are in a disk image.

#### Manually creating a disk image

- From the Finder: drag the package onto the Disk Utility application located in /Applications/Utilities. Disk Utility will launch and prompt you for a location and name to save the disk image. Be certain to create a read-only disk image, or you will get checksum hash errors when Munki tries to download your disk image.

- From the command-line: `sudo hdiutil create -fs HFS+ -srcfolder /path/to/some_folder_of_stuff /path/to/some.dmg` -- this ensures that it creates an image readable on older macOS versions and will unmount cleanly.