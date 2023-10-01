### Deploying Xcode with Munki

#### Xcode 10

Nothing appears to have changed between Xcode 9 and 10 for deployment. As before, strongly recommended you download the package from the developer site and not use the AppStore version. The previous install script that was used for Xcode 5 still works fine. Use `munkiimport` to import the Xcode.app you have downloaded from the developer site and then for postinstall scripts use the [script](#postinstall_script) detailed in the Xcode 5 section. 

This has been tested on Xcode 10.2 and 10.2.1 and no issues found as yet with repeated requests to install packages or accept EULA.

#### Xcode 9

Nothing appears to have changed between Xcode 8 and 9 for deployment. As before, strongly recommended you download the package from the developer site and not use the AppStore version. The previous install script that was used for Xcode 5 still works fine. Use `munkiimport` to import the Xcode.app you have downloaded from the developer site and then for postinstall scripts use the [script](#postinstall_script) detailed in the Xcode 5 section. 

This has been tested on Xcode 9.3 and no issues found as yet with repeated requests to install packages or accept EULA.

#### Xcode 8
Nothing seems to have changed between Xcode 7 and 8 for deployment. The previous postinstall scripts continue to work as expected.

#### Xcode 7
The postinstall_script that worked on previous versions of Xcode continues to work for Xcode 7. There is an issue, however, specifically with Xcode 7.2.1 that requires additional attention. While the postinstall_script successfully installs the packages in the /Applications/Xcode.app/Contents/Resources/Packages/ directory, on first launch, Xcode prompts for admin credentials and then proceeds to install those same packages again. The current work around is to add the following lines to the end of the existing postinstall_script to tell Xcode not to check for these packages at launch:
```xml
# disable version check for MobileDeviceDevelopment
/usr/bin/defaults write /Library/Preferences/com.apple.dt.Xcode DVTSkipMobileDeviceFrameworkVersionChecking -bool true
```
A possibly bad side-effect of this approach would be if someone later manually installed a newer version of Xcode that came with a newer version of the MobileDeviceDevelopment pkg, Xcode would not attempt to install it.

#### Xcode 6

The same directions below used to deploy Xcode 5 continue to work for Xcode 6, verified with Xcode 6.1.1. Additionally, the Xcode Command Line Tools can be installed by either downloading them from the Apple Developer site and importing them into Munki, or by following the method described by Rich Trouton on his [blog](https://derflounder.wordpress.com/2015/02/02/installing-the-xcode-command-line-tools-on-10-7-x-and-later/).

#### Xcode 5

I recommend you get a Mac Developer membership and use the version of Xcode available on the Developer site; this avoids having to deal with the App Store challenges. If you use the App Store version, see [[App Store Apps]] for some advice.

I've had good success with using `munkiimport` to import the Xcode 5 disk image, and then adding the following postinstall_script to the pkginfo:

##### postinstall_script
```xml
<key>postinstall_script</key>
<string>#!/bin/sh

# make sure all users on this machine are members of the _developer group
/usr/sbin/dseditgroup -o edit -a everyone -t group _developer

# enable developer mode
/usr/sbin/DevToolsSecurity -enable

# accept Xcode license
/Applications/Xcode.app/Contents/Developer/usr/bin/xcodebuild -license accept

# install embedded packages
for PKG in /Applications/Xcode.app/Contents/Resources/Packages/*.pkg; do
    /usr/sbin/installer -pkg "$PKG" -target /
done
</string>
```

Depending on your exact needs, you may need to modify this script and/or perform additional tasks.

#### Xcode 4.5

There are two extra installers that need to be installed after installing Xcode 4.5.2: Xcode.app/Contents/Resources/Packages/MobileDevice.pkg and Xcode.app/Contents/Resources/Packages/MobileDeviceDevelopment.pkg

You should mark them as update_for Xcode 4.5.2 so they can be uninstalled as well when Xcode is uninstalled. You can import the packages using munkiimport:

```bash
munkiimport /Applications/Xcode.app/Contents/Resources/Packages/MobileDevice.pkg --update_for=Xcode-4.5.2
munkiimport /Applications/Xcode.app/Contents/Resources/Packages/MobileDeviceDevelopment.pkg --update_for=Xcode-4.5.2
```

Xcode also needs a postinstall_script to enable developer mode and add users to the developer group:

```bash
    #!/bin/sh
    
    # Enable developer mode policies
    /usr/sbin/DevToolsSecurity -enable
    
    # Add a group to developer group
    /usr/sbin/dseditgroup -o edit -a <your_group_name> -t group _developer
    
    exit 0
```

And postuninstall_script to revert the changes:

```bash
    #!/bin/sh
    
    # Disable developer mode policies
    /usr/sbin/DevToolsSecurity -disable
    
    # Remove a group from developer group
    /usr/sbin/dseditgroup -o edit -d <your_group_name> -t group _developer
    
    exit 0
```

#### Xcode 4.3/4.3.1/4.3.2 for Lion

Xcode is now distributed as a self-contained Xcode.app via the Mac App Store (MAS) as well as Apple's Developer Center.  The applications are identical, though the MAS version will take a very long time to import to a DMG using munkiimport as it contains a high number of files and is very large.  The version from Apple's Developer Center is already a DMG, so it is recommended to use.  This does require a developer account to access, but the free Safari developer program does provide access to Xcode. http://developer.apple.com/downloads

Xcode requires a !MobileDevice package to be installed on first launch, but we can install this easily with Munki.  This can be done with a post-install script, but it is safer to import that package to your repo and set Xcode to require it.  It is contained inside Xcode.app, at Xcode.app/Contents/Resources/Packages/MobileDevice.pkg

You may also want to download and import the Command Line tools and Auxiliary Tools for Xcode from the Developer site.

In order to properly remove the Command Line Xcode tools, you should be using version 0.8.2 of the Munki tools when importing the Command Line Xcode tools package.

#### Pre-Xcode 4.3

The receipts left on disk after installing versions of Xcode prior to 4.3 do not match the receipt info declared within the Xcode metapackage distribution file, so you will need to add an "installs" key to prevent Munki from attempting to reinstall Xcode repeatedly. You may also want to add minimum_os_version and/or maximum_os_version keys to prevent attempted installs on the wrong OS versions. Some examples:

#### Xcode 4.2.1 for Lion

```xml
    	<key>installs</key>
    	<array>
    		<dict>
    			<key>CFBundleIdentifier</key>
    			<string>com.apple.dt.Xcode</string>
    			<key>CFBundleName</key>
    			<string>Xcode</string>
    			<key>CFBundleShortVersionString</key>
    			<string>4.2.1</string>
    			<key>path</key>
    			<string>/Developer/Applications/Xcode.app</string>
    			<key>type</key>
    			<string>application</string>
    		</dict>
    	</array>
    	<key>minimum_os_version</key>
    	<string>10.7.2</string>
```

#### Xcode 4.2 for Snow Leopard

```xml
    	<key>installs</key>
    	<array>
    		<dict>
    			<key>CFBundleIdentifier</key>
    			<string>com.apple.dt.Xcode</string>
    			<key>CFBundleName</key>
    			<string>Xcode</string>
    			<key>CFBundleShortVersionString</key>
    			<string>4.2</string>
    			<key>path</key>
    			<string>/Developer/Applications/Xcode.app</string>
    			<key>type</key>
    			<string>application</string>
    		</dict>
    	</array>
            <key>maximum_os_version</key>
    	<string>10.6.9</string>
    	<key>minimum_os_version</key>
    	<string>10.6.8</string>
```

#### Xcode 3.2.6

```xml
    	<key>installs</key>
    	<array>
    		<dict>
    			<key>CFBundleIdentifier</key>
    			<string>com.apple.Xcode</string>
    			<key>CFBundleName</key>
    			<string>Xcode</string>
    			<key>CFBundleShortVersionString</key>
    			<string>3.2.6</string>
    			<key>path</key>
    			<string>/Developer/Applications/Xcode.app</string>
    			<key>type</key>
    			<string>application</string>
    		</dict>
            </array>
    	<key>maximum_os_version</key>
    	<string>10.6.9</string>
    	<key>minimum_os_version</key>
    	<string>10.6.6</string>
```    

### Uninstalling Xcode (pre-App Store versions of Xcode)

Since the package receipt info for Xcode is not useful, it can't be used for uninstalls, either. Fortunately, Apple has provided an uninstall script that Munki can use:

```xml
    	<key>uninstall_method</key>
    	<string>/Developer/Library/uninstall-devtools</string>
```

#### More XCode 4 for Lion notes

Now that Xcode 4 is a free download from the Mac App Store, I wanted to be able to use munki to distribute it (as an optional install) to Lion machines. Here's what I did:

1. "Purchased" and downloaded Xcode 4.2.1 from the Mac App Store.
1. Control-clicked the "Install Xcode.app" and chose "Show Package Contents".
1. Navigated to the Resources directory, in which I found an Xcode.mpkg and a Packages subdirectory.
1. Copied the Xcode.mpkg and a Packages subdirectory to a new directory named Xcode4.2.1.
1. Used DiskUtility to make a disk image of the Xcode4.2.1 directory. (Be sure when making a disk image that you choose to make a read-only or compressed disk image. Read-write disk images will cause "Hash value integrity check" errors unless Munki's PackageVerificationMode is set to 'none' or the installer_item_hash is removed from the pkginfo (neither change is recommended).
1. Used munkiimport to import it into my munki repo.
1. Changed minimum_os_version to `<string>10.7.2</string>`.
1. Added an "installs" item for /Developer/Applications/Xcode.app as described above.
1. Changed the uninstall_method to `<string>/Developer/Library/uninstall-devtools</string>` as described above.