_How to deploy Microsoft Office 2008 using Munki._

#### Fix invalid values in original  Office 2008 installer

Microsoft used a non-integer value for some integer-only keys, which the built-in python plist parser can't handle.  Before Munki can work with this installer, these values must be corrected.

1. Create a read-write disk image of the Office 2008 Installer media called "Office2008.dmg"
1. Mount disk image
1. Replace all instances of:

    ```
    <key>IFMajorVersion</key>
    <integer>071201.1</integer>
    ```

    found in any plist on the disk image with

    ```
    <key>IFMajorVersion</key>
    <integer>071201</integer>
    ```

    I dragged the "Office Installer" from the disk image to TextMate, and used "Find in Project" to change all of the files at once.

#### Create pkginfo file

1. Copy disk image to your munki pkgs folder
1. Run `makepkginfo` to create a pkginfo file called Office2008-12.0.0.pkginfo
1. Set the "name" key to "Office2008"
1. Add this installs key to the Office2008-12.0.0.pkginfo:

    ```
    <key>installs</key>
    <array>
        <dict>
            <key>type</key>
            <string>plist</string>
            <key>path</key>
            <string>/Applications/Microsoft Office 2008/Office/MicrosoftComponentPlugin.framework/Resources/Info.plist</string>
            <key>CFBundleShortVersionString</key>
            <string>12.0.0</string>
        </dict>
    </array>
    ```

    This Info.plist file contains the most accurate version information for Office 2008, and allows munki to quickly determine what version of Office is installed.  You should now be able to add "Office2008" to a manifest, update your catalogs and deploy Office 2008 via Munki.

#### Deploy Office 2008 12.1.0 update

1. Download the Office 2008 12.1.0 update from Microsoft (Office2008-1210UpdateEN.dmg)
1. Copy the dmg to your munki pkgs folder
1. Run `makepkginfo` to create a pkginfo file called Office2008-12.1.0.pkginfo
1. Set the "name" key to "Office2008_update"
1. Add the "installs" key from above to the Office2008-12.1.0.pkginfo file and set the "CFBundleShortVersionString" key to "12.1.0".  This tells Munki what version the update installs.  (If a previous version exists on the machine, the update will be applied, while if 12.1.0 or later is found, the update will not be run.)
1. Add these keys to the Office2008-12.1.0.pkginfo file

    ```
    <key>update_for</key>
    <array>
        <string>Office2008</string>
    </array>
    <key>requires</key>
    <array>
        <string>Office2008-12.0.0.0.0</string>
    </array>
    ```

    The "update_for" key tells Munki that this installer is for Office 2008, which cause it to be automatically installed on any client that has "Office2008" listed in its manifest.  The "requires" key tells Munki that this installer requires Office2008-12.0.0.0.0 to be already installed, which will cause Munki to make sure that Office2008-12.0.0.0.0 is installed before this update is applied.

#### Deploy other Office 2008 Updates

1. Download the other Office 2008 updates from Microsoft (12.2.0. 12.2.3, 12.2.4, etc.)
1. Copy the installers to your munki pkgs folder
1. Run `makepkginfo` to create a pkginfo file for each update (Office2008-12.2.0.pkginfo, Office2008-12.2.3.pkginfo, etc.)
1. Set the "name" keys to "Office2008_update"
1. Add the "installs" key from above to each pkginfo file and set the "CFBundleShortVersionString" key to the correct version (12.2.0, 12.2.3, 12.2.4, etc.)
1. Add the same "update_for" key from above to each pkginfo file
1. Add a "requires" key for to each pkginfo file, but set it to list the previous update.  (12.2.0 requires "Office2008_Update-12.1.0.0.0", 12.2.3 requires "Office2008_Update-12.2.0.0.0", etc.  That way, Munki will know what order to install the updates.)

Once everything is working, Munki will be able to install a fully patched version of Microsoft Office.  For a new install, it will first run the original Office 2008 installer, followed by each update, in the order defined by the "require" keys.

### Addendum

Microsoft has an updated Office 2008 installer available, which installs Office 2008 SP2 (The version I was able to obtain installed Office 12.2.2).  The updated installer disk image doesn't need any special tricks to work with `makepkginfo`. You'll still need to deploy the subsequent updates.

Will Polley also pointed out that the Office 2008 12.2.5 update contains all the updates after 12.1.0.  So if you can get the updated installer from Microsoft that includes Office 2008 SP2, that plus the 12.2.5 update is all you need.
