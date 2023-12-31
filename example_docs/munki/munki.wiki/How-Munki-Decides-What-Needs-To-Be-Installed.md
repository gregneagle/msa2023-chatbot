_Overview of the check phase and the use of receipts/installs_

### Introduction

When checking to see what needs to be installed, Munki uses information in the pkginfo items to decide whether or not a given item is installed. A Munki admin must understand how this works in order to create functional pkginfo items.

### Details

Each time `managedsoftwareupdate` runs (except when in --installonly mode), it checks the lists of managed_installs, managed_updates, optional_installs, and managed_uninstalls items to see if they are installed.

Listed below, in order of precedence, are the methods used by munki to determine if a given item should be installed. (The check for removals is similar, but not 100% identical.)
The order is as follows:
- OnDemand
- installcheck_script
- Configuration Profiles
- installs items
- receipts

When combining these methods, **only** the highest priority method is used.  For example, if a given pkginfo item has both an "installs" list and a "receipts" list, the receipts will be ignored for purposes of determining installation status. Even in this case, though, receipts may be used when removing an item, as they help Munki determine exactly which files were installed.

#### OnDemand
Pkginfo items with a key of `OnDemand` set to `true` will always be installed:
```
    <key>OnDemand</key>
    <true/>
```

The default value is `false`.

https://github.com/munki/munki/wiki/On-Demand-Items

#### Install Check Script

A pkginfo item may optionally contain an "installcheck_script". Its purpose is to provide a method for determining if an item needs to be installed where providing "installs/receipts" is inadequate or impractical.  Command-line tools typically installed via `port` (macports) or Python modules installed using `easy_install` or `pip` are prime examples as they provide no easy method for determining their installed version.

An "installcheck_script" should be crafted such that an exit code of 0 indicates that the item is currently **not** installed and should therefore be installed.  All non-zero exit codes indicate that the item in question is installed.

Here's an example "installcheck_script" illustrating a check to determine if the current version of the `argparse` Python module is installed:

```sh
#!/bin/sh
    
# Grab current version of installed python module
version="$(python -c 'import argparse;print argparse.__version__' 2>/dev/null)"
    
# Compare with the version we want to install
if [ ${version:-0} < 1.2.1 ]; then
    exit 0
else
    exit 1
fi
```

*Same script, embedded in a pkginfo file...*

```xml
    <key>installcheck_script</key>
    <string>#!/bin/sh

# Grab current version of installed python module
version="$(python -c 'import argparse;print argparse.__version__' 2&gt;/dev/null)"

# Compare with the version we want to install
if [ ${version:-0} &lt; 1.2.1 ]; then
    exit 0
else
    exit 1
fi
    </string>
```

Inversely, if an item that included an "installcheck_script" were to be a "managed_uninstall", this same script would be used to determine if the item is installed so that a removal can be processed.  This is similar to how removals are processed, based on "installs" items.


#### Uninstall Check Script

Optionally, an explicit "uninstallcheck_script" can be provided to determine whether or not an item should be removed.  In this case, the script would provide an exit code of 0 to indicate that the item is currently installed and that removal should occur.  All non-zero exit codes indicate that the item in question is **not** installed.

#### Configuration Profiles
Pkginfo items with the `installer_type` of `profile` will use the following conditions to determine whether to install the profile. They are checked, in order, and if any of these conditions is true, Munki will install the profile. Please see [Managing Configuration Profiles](https://github.com/munki/munki/wiki/Managing-Configuration-Profiles) for more information.

1. _Is the profile's identifier in the output of `profiles -C`?_ 

   Every profile has an identifier, with a recommended value of a reverse-domain name uniquely identifying the profile. (e.g. com.myorganization.SoftwareUpdateSettings). Munki will compare the profile it is considering installing with the results of `profiles -C` to see if there is a match. For this reason, updates to an existing profile must use the same identifier (but a different version) to be considered for installation.
2. _Is there a receipt for this profile identifier?_
   
   Even if a profile has been manually installed, without a profile receipt, Munki will install the profile.
3. _Does the hash of this profile match the receipt's hash_value match?_

   The hash value is generated by feeding the .mobileconfig file through a sha256 hashing algorithm. The hash is _not_ based on the identifier, nor the UUID.
4. _Does the `ProfileInstallDate` from the profile's receipt match the `ProfileInstallDate` specified by `profiles -C`?_

   In the event that these dates differ, even though the identifier and hash match, Munki will install the profile.

#### Installs

This list is generated for you by `makepkginfo` or `munkiimport` for some types of installation items ("drag-n-drop" disk images; Adobe installers), but not for Apple packages. You can generate (or modify) this list yourself.

This is the most flexible mechanism for determining installation status. The "installs" list can contain any number of items. These can be applications, Preference Panes, Frameworks, or other bundle-style items, Info.plists, or simple directories or files. The Munki admin can use any combination of items to help Munki determine if an item is installed or not.

Here's an auto-generated "installs" list for Firefox 64.0.2:

```xml
	<key>installs</key>
	<array>
		<dict>
			<key>CFBundleIdentifier</key>
			<string>org.mozilla.firefox</string>
			<key>CFBundleName</key>
			<string>Firefox</string>
			<key>CFBundleShortVersionString</key>
			<string>64.0.2</string>
			<key>CFBundleVersion</key>
			<string>6419.1.8</string>
			<key>minosversion</key>
			<string>10.9.0</string>
			<key>path</key>
			<string>/Applications/Firefox.app</string>
			<key>type</key>
			<string>application</string>
			<key>version_comparison_key</key>
			<string>CFBundleShortVersionString</string>
		</dict>
	</array>
```

To determine if Firefox 64.0.2 is installed, Munki first looks at the path of `/Applications/Firefox.app`, and then looks for an application with a _CFBundleIdentifier_ of `org.mozilla.firefox`, and, if found, verifies that its version (_CFBundleShortVersionString_) is at least `64.0.2`.

If it can't find the application or if its version is lower than 64.0.2, Munki considers Firefox-64.0.2 as *not* installed.

Installs lists can contain multiple items. If any item is missing or has an older version, the item will be considered not installed.

**Note**: Because the path is checked before the bundle identifier is, you can have two separate items (e.g., _Firefox_ and _FirefoxESR_) have their own respective installs arrays with two separate paths (e.g., _/Applications/Firefox.app_ and _/Applications/FirefoxESR.app_) but share the same bundle identifier (e.g., _org.mozilla.firefox_), and Munki will not try to upgrade one to the other.

You can manually generate items to add to an "installs" list using `makepkginfo`:

```sh
/usr/local/munki/makepkginfo -f /Library/Internet\ Plug-Ins/Flash\ Player.plugin
```
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>installs</key>
    <array>
        <dict>
            <key>CFBundleShortVersionString</key>
            <string>10.3.183.5</string>
            <key>path</key>
            <string>/Library/Internet Plug-Ins/Flash Player.plugin</string>
            <key>type</key>
            <string>bundle</string>
        </dict>
    </array>
</dict>
</plist>
```

You could then copy and paste the entire "installs" key and value, or copy just the dict value and add it to and existing installs list.

In this example, Munki would check for the existence of "/Library/Internet Plug-Ins/Flash Player.plugin" and if found, check its version. If the version was lower than "10.3.183.5", this item would be considered not installed.

You can generate "installs" items for any filesystem item, but Munki only knows how to determine versions for bundle-style items that contain an Info.plist or version.plist with version information. For other filesystem items, Munki can only determine existence (in the case of a non-bundle directory), or can calculate a checksum (for files). For files with checksums, the test will fail (and therefore the item will be considered not installed) if the checksum for the file on disk does not match the checksum in the pkginfo.

```xml
<key>installs</key>
<array>
    <dict>
        <key>md5checksum</key>
        <string>087fe4805b63412ec3ed559b0cd9be71</string>
        <key>path</key>
        <string>/private/var/db/dslocal/nodes/MCX/computergroups/loginwindow.plist</string>
        <key>type</key>
        <string>file</string>
    </dict>
</array>
```

If you'd like Munki to only check for the existence of a file and do not care about its contents, remove the generated md5checksum information in the installs item info. Be sure to leave the path intact!

```xml
<key>installs</key>
<array>
    <dict>
        <key>path</key>
        <string>/private/var/db/dslocal/nodes/MCX/computergroups/loginwindow.plist</string>
        <key>type</key>
        <string>file</string>
    </dict>
</array>
```

https://github.com/munki/munki/wiki/Pkginfo-Files#installs-array

#### Receipts

When an Apple-style package is installed, it leaves a receipt on the machine. Metapackages leave multiple receipts. `makepkginfo` and `munkiimport` add the names and versions of those receipts to a "receipts" array in the pkginfo for a package.

Here's is a receipts array for the Avid LE QuickTime codecs, version 2.3.4:

```xml
<key>receipts</key>
<array>
    <dict>
        <key>filename</key>
        <string>AvidCodecsLE.pkg</string>
        <key>installed_size</key>
        <integer>1188</integer>
        <key>name</key>
        <string>AvidCodecsLE</string>
        <key>packageid</key>
        <string>com.avid.avidcodecsle</string>
        <key>version</key>
        <string>2.3.4</string>
    </dict>
</array>
```

If Munki is using the "receipts" array to determine installation status, it checks for the existence and the version of each receipt in the array. If any receipt is missing or has a lower version number than the version specified for that receipt in the "receipts" array, the item is considered not installed. Only if every receipt is present and all versions are the same as the ones in the pkginfo (or higher) is the item considered installed.

If you are troubleshooting, you can use the `pkgutil` tool to examine the installed receipts:

```sh
# pkgutil --pkg-info com.avid.avidcodecsle
No receipt for 'com.avid.avidcodecsle' found at '/'.
```

In this case, the receipt for the Avid LE QuickTime codecs was not found on this machine.

A common complication with receipts is this: with many metapackages, the installation logic results in only a subset of the subpackages being installed. Generally, the "receipts" list contains a receipt for every subpackage in a metapackage (and needs this info if Munki is asked to remove the software based on package receipts). But if it is normal and expected that not every subpackage will actually be installed, Munki will continually mark the item as not currently installed and offer to install it again and again.

One solution for this issue is to add an "optional" key with the value of "true" to the receipts that are optionally installed. Munki will then not consider these receipts when determining installation status.

```xml
<key>receipts</key>
<array>
    <dict>
        <key>filename</key>
        <string>mandatory.pkg</string>
        <key>installed_size</key>
        <integer>1188</integer>
        <key>name</key>
        <string>Mandatory</string>
        <key>packageid</key>
        <string>com.foo.mandatory</string>
        <key>version</key>
        <string>1.0</string>
    </dict>
    <dict>
        <key>filename</key>
        <string>optional.pkg</string>
        <key>installed_size</key>
        <integer>1188</integer>
        <key>name</key>
        <string>Optional</string>
        <key>optional</key>
        <true/>
        <key>packageid</key>
        <string>com.foo.optional</string>
        <key>version</key>
        <string>1.0</string>
    </dict>
</array>
```

Another solution for this situation is to provide an "installs" array that lists items that are installed by the package. Munki can use that information instead of the receipts to determine installation status.