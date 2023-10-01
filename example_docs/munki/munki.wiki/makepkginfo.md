_Tool for making pkginfo files_

### Introduction

Well-crafted pkginfo files are the key to munki's functionality. Creating these by hand is tedious and error-prone. The makepkginfo tool can help.


### Details

Tool: makepkginfo

Creates a managed install pkginfo plist given an Installer item:
a .pkg, a .mpkg, a .mobileconfig profile, or a .dmg containing a .pkg or .mpkg at the root of the mounted disk image.

makepkginfo now also supports a few other dmg types:
  1. Drag-and-drop application dmgs
  1. Adobe CS4 Update installer dmgs
  1. DMGs containing Adobe CS4 Deployment Toolkit packages and install files
  1. (Adobe CS5/CS6/CC products are also supported, but generally must be repackaged with AAMEE or CCP. See [[Munki And Adobe CS5]], [[Munki And Adobe CS6]] and other wiki documentation for more info.)

You may also pass items that are installed by the package using the '-f' flag. 
These are added to the 'installs' key of the catalog item plist and are used when 
processing the catalog to check if the package needs to be installed or 
reinstalled.

You can leave off the installer item, and just pass "-f" items to build a list of items to add to an existing pkginfo file.

The generated plist is printed to STDOUT.

Usage: `makepkginfo [/path/to/package_or_dmg] [-f /path/to/item/it/installs ...]`

A simple example:

```bash
> ./makepkginfo /path/to/ServerAdminToold1055.dmg
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>description</key>
    <string></string>
    <key>installer_item_location</key>
    <string>ServerAdminToold1055.dmg</string>
    <key>minimum_os_version</key>
    <string>10.4.0</string>
    <key>name</key>
    <string>ServerAdministrationSoftware</string>
    <key>receipts</key>
    <array>
    	<dict>
    	    <key>packageid</key>
    	    <string>com.apple.pkg.ServerAdminTools</string>
    	    <key>version</key>
    	    <string>10.5.3.0</string>
    	</dict>
    	<dict>
    	    <key>packageid</key>
    	    <string>com.apple.pkg.ServerSetup</string>
    	    <key>version</key>
    	    <string>10.5.3.0</string>
        </dict>
    </array>
    <key>version</key>
    <string>10.5.3.0</string>
</dict>
</plist>
```

Another example:

```bash
> makepkginfo --file /Applications/iWork\ \'08/Keynote.app --file /Applications/iWork\ \'08/Pages.app --file /Applications/iWork\ \'08/Numbers.app /Volumes/iWork08/iWork08.pkg
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>description</key>
    <string></string>
    <key>installer_item_location</key>
    <string>iWork08.pkg</string>
    <key>installs</key>
    <array>
        <dict>
            <key>CFBundleIdentifier</key>
            <string>com.apple.iWork.Keynote</string>
            <key>CFBundleName</key>
            <string>Keynote</string>
            <key>CFBundleShortVersionString</key>
            <string>4.0.3</string>
            <key>type</key>
            <string>application</string>
        </dict>
        <dict>
            <key>CFBundleIdentifier</key>
            <string>com.apple.iWork.Pages</string>
            <key>CFBundleName</key>
            <string>Pages</string>
            <key>CFBundleShortVersionString</key>
            <string>3.0.2</string>
            <key>type</key>
            <string>application</string>
        </dict>
        <dict>
            <key>CFBundleIdentifier</key>
            <string>com.apple.iWork.Numbers</string>
            <key>CFBundleShortVersionString</key>
            <string>1.0.2</string>
            <key>type</key>
            <string>application</string>
        </dict>
    </array>
    <key>minimum_os_version</key>
    <string>10.4.0</string>
    <key>name</key>
    <string>iWork</string>
    <key>receipts</key>
    <array>
        <dict>
            <key>packageid</key>
            <string>com.apple.pkg.iWork08</string>
            <key>version</key>
            <string>3.0.0.1352</string>
        </dict>
    </array>
    <key>version</key>
    <string>08</string>
</dict>
</plist>
```

Note that in both of these examples the required key installer_item_location will almost certainly be wrong unless you store all of your installer items at the root of the pkgs directory in the repo.

Here's makepkginfo run against a Firefox dmg:

```bash
> makepkginfo /Volumes/repo/pkgs/apps/Firefox\ 3.5.3.dmg
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>catalogs</key>
    <array>
        <string>testing</string>
    </array>
    <key>installer_item_location</key>
    <string>apps/Firefox 3.5.3.dmg</string>
    <key>installer_item_size</key>
    <integer>18002</integer>
    <key>installer_type</key>
    <string>appdmg</string>
    <key>installs</key>
    <array>
        <dict>
            <key>CFBundleIdentifier</key>
            <string>org.mozilla.firefox</string>
            <key>CFBundleName</key>
            <string>Firefox</string>
            <key>CFBundleShortVersionString</key>
            <string>3.5.3</string>
            <key>path</key>
            <string>/Applications/Firefox.app</string>
            <key>type</key>
            <string>application</string>
        </dict>
    </array>
    <key>minimum_os_version</key>
    <string>10.4.0</string>
    <key>name</key>
    <string>Firefox</string>
    <key>uninstall_method</key>
    <string>remove_app</string>
    <key>uninstallable</key>
    <true/>
    <key>version</key>
    <string>3.5.3.0.0</string>
</dict>
</plist>
```

### Options

`makepkginfo` supports a lot of options:

<table>
  <tr><td>-h</td><td>--help</td><td>Show a help message and exit</td></tr>
  <tr><td>-f FILE</td><td>--file=FILE</td><td>Path to a filesystem item installed by this package, typically an application. This generates an "installs" item for the pkginfo, an item munki can use to determine if this software has been installed. Can be specified multiple times.</td></tr>
  <tr><td>-p PKGNAME</td><td>--pkgname=PKGNAME</td><td>Optional flag.<br>-If the installer item is a disk image containing multiple packages, or the package to be installed is not at the root of the mounted disk image, PKGNAME is a relative path from the root of the mounted disk image to the specific package to be installed.<br>-If the installer item is a disk image containing an Adobe CS4 Deployment Toolkit installation, PKGNAME is the name of an Adobe CS4 Deployment Toolkit installer package folder at the top level of the mounted dmg. If this flag is missing, the AdobeUber`*` files should be at the top level of the mounted dmg.</td></tr>
  <tr><td>-i ITEM<br>-a ITEM</td><td>--itemname=ITEM<br>--appname=ITEM</td><td>Optional flag.<br>-If the installer item is a disk image with a drag-and-drop item, ITEMNAME is the name or relative path of the item to be installed.<br>Useful if there is more than one item at the root of the dmg.</td></tr>
  <tr><td></td><td>--displayname=DISPLAYNAME</td><td>Optional flag.<br>String display name of the package. <br>Note: overrides any display_name in the package itself.</td></tr>
  <tr><td></td><td>--description=DESCRIPTION</td><td>Optional flag.<br>String description of the package.<br>Note: overrides any description in the package itself</td></tr>
  <tr><td>-d DESTINATIONPATH</td><td>--destinationpath=DESTINATIONPATH</td><td>Optional flag.<br>If the installer item is a disk image with a drag-and-drop item, this is the path to which the item should be copied. Defaults to "/Applications".</td></tr>
  <tr><td>-u UNINSTALLERDMG</td><td>--uninstallerdmg=UNINSTALLERDMG</td><td>Optional flag.<br>If the installer item is a disk image containing an Adobe CS4 Deployment Toolkit installation package or Adobe CS3 deployment package, UNINSTALLERDMG is a path to a disk image containing an AdobeUberUninstaller for this item.</td></tr>
  <tr><td></td><td>--postinstall_script=SCRIPT_PATH</td><td>Optional flag.<br>Path to an optional postinstall script to be run after installation of the item. The script will be read and embedded into the pkginfo.</td></tr>
  <tr><td></td><td>--preinstall_script=SCRIPT_PATH</td><td>Optional flag.<br>Path to an optional preinstall script to be run before installation of the item. The script will be read and embedded into the pkginfo.</td></tr>
  <tr><td></td><td>--postuninstall_script=SCRIPT_PATH</td><td>Optional flag.<br>Path to an optional postuninstall script to be run after removal of the item. The script will be read and embedded into the pkginfo.</td></tr>
  <tr><td></td><td>--preuninstall_script=SCRIPT_PATH</td><td>Optional flag.<br>Path to an optional preuninstall script to be run before removal of the item. The script will be read and embedded into the pkginfo.</td></tr>
  <tr><td></td><td>--uninstall_script=SCRIPT_PATH</td><td>Optional flag.<br> Path to an uninstall script to be run in order to uninstall this item. The script will be read and embedded into the pkginfo.</td></tr>
  <tr><td>-c CATALOG</td><td>--catalog=CATALOG</td><td>Optional flag.<br>Specifies in which catalog the item should appear. The default is 'testing'. Can be specified multiple times to add the item to multiple catalogs.</td></tr>
  <tr><td>-o USER</td><td>--owner=USER</td><td>Optional flag.<br>If the installer item is a disk image used with the copy_from_dmg installer type, this sets the owner of the item specified by the --item flag. The owner may be either a UID or a symbolic name. The owner will be set recursively on the item.</td></tr>
  <tr><td>-g GROUP</td><td>--group=GROUP</td><td>Optional flag.<br>If the installer item is a disk image used with the copy_from_dmg installer type, this sets the group of the item specified by the --item flag. The group may be either a GID or a symbolic name. The group will be set recursively on the item.</td></tr>
  <tr><td>-m MODE</td><td>--mode=MODE</td><td>Optional flag.<br>If the installer item is a disk used with the copy_from_dmg installer type, this sets the mode of the item specified by the --item flag. The specified mode must be in symbolic form. See the manpage for chmod(1) for more information. The mode is applied recursively.</td></tr>
  <tr><td>-V</td><td>--version</td><td>Print the version of the munki tools and exit.</td></tr>
</table>