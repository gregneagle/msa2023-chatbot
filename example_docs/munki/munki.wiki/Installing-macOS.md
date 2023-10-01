_Packaging the OS X installer for use with Munki_

### Munki 3+ note
Munki 3 and later provide a "native" option: see [[macOS Installer Application support]]. Use this native support for upgrading to Sierra or later with Munki 3 or later. The remainder of this document is for historical record, or for those still running Munki 2 and/or "upgrading" to a release of macOS older than 10.12.

### Introduction

It is possible to package up OS X installers in order to install (or more accurately, upgrade to) Lion, Mountain Lion, Mavericks, Yosemite, El Capitan or Sierra using Munki. Once you've packaged the OS X installer in this way, you may use Munki to install Lion, Mountain Lion, Mavericks, Yosemite, El Capitan, or Sierra in the same way you install, say, Microsoft Office. And you would likely want to name each major macOS upgrade installer item differently, the same way you would name Office2011 and Office2016 differently.

### Details

#### Getting Started

You'll need some tools to package up the OS X installer.

You can download a zip archive here:

https://github.com/munki/createOSXinstallPkg/archive/master.zip

Or you may clone the Git repo:

```bash
git clone https://github.com/munki/createOSXinstallPkg.git
```
See https://github.com/munki/createOSXinstallPkg/blob/master/README.md for more info on the use of the tools.

### pkginfo notes

To prevent Apple softwareupdates from being offered in the same Munki install session as one with a package you built with createOSXInstallPkg (for example, to prevent a 10.10.5 update or Apple Security update from being applied at the same time Munki is applying an upgrade to El Capitan), make sure to add

```xml
<key>apple_item</key>
<true/>
```

to the pkginfo for your OS X upgrade package.
 
#### receipts
The receipt left behind by a `createOSXinstallPkg`-generated package may not be useful if you also want to detect that the OS has been upgraded/installed by other means.

(In other words: if you were to add an "InstallMountainLion" package to the managed_installs for a certain machine, but that machine already had Mountain Lion, installed some other way, Munki would fail to find the receipt and attempt to install Mountain Lion anyway.)

So instead we should look for receipts that will be there no matter how OS X is installed.

To find the exact packagid version string run pkgutil on a Mac with the current version of OS X you want to install.

```bash
pkgutil --pkg-info com.apple.pkg.BaseSystemBinaries
```

Here are examples of what I've been using successfully:

#### Lion:

```xml    
<key>receipts</key>
<array>
    <dict>
        <key>packageid</key>
    	<string>com.apple.pkg.BaseSystemBinaries</string>
    	<key>version</key>
    	<string>10.7.0.1.1.1306847324</string>
    </dict>
</array>
```

#### Mountain Lion:

```xml    
<key>receipts</key>
<array>
    <dict>
        <key>packageid</key>
        <string>com.apple.pkg.BaseSystemBinaries</string>
        <key>version</key>
        <string>10.8.0.1.1.1306847324</string>
    </dict>
</array>
```

#### Mavericks:

```xml    
<key>receipts</key> 
<array>
    <dict>
        <key>packageid</key> 
        <string>com.apple.pkg.BaseSystemBinaries</string>
        <key>version</key>
        <string>10.9.0.1.1.1306847324</string>
    </dict>
</array>
```

#### Yosemite:

```xml
<key>receipts</key>
<array>
    <dict>
        <key>packageid</key>
        <string>com.apple.pkg.BaseSystemBinaries</string>
        <key>version</key>
        <string>10.10.0.1.1.1412852630</string>
    </dict>
</array>
```

#### El Capitan

Beginning with El Capitan, `com.apple.pkg.BaseSystemBinaries` is not part of the install. Instead of modifying the receipts array, I recommend adding an installs array instead. (You could also do this with older versions of OS X.)
```xml
	<key>installs</key>
	<array>
		<dict>
			<key>ProductVersion</key>
			<string>10.11</string>
			<key>path</key>
			<string>/System/Library/CoreServices/SystemVersion.plist</string>
			<key>type</key>
			<string>plist</string>
			<key>version_comparison_key</key>
			<string>ProductVersion</string>
		</dict>
	</array>
```

#### Sierra

Sierra would have a similar installs array to El Capitan.
```xml
	<key>installs</key>
	<array>
		<dict>
			<key>ProductVersion</key>
			<string>10.12</string>
			<key>path</key>
			<string>/System/Library/CoreServices/SystemVersion.plist</string>
			<key>type</key>
			<string>plist</string>
			<key>version_comparison_key</key>
			<string>ProductVersion</string>
		</dict>
	</array>
```

#### Avoiding Unsupported Hardware

Munki will gladly offer (and allow the built-in checks to make it fail) the OS install on hardware that is not capable of running that particular release. You can use logic like the one found [here for Mojave](https://github.com/hjuutilainen/adminscripts/blob/master/check-10.14-mojave-compatibility.py) to do a [conditional item](https://github.com/munki/munki/wiki/Conditional-Items) and prevent this from looping at the worst, or polluting logs with errors and warnings at the least.