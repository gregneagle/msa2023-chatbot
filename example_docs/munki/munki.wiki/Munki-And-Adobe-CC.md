# Introduction

Info on installing and removing Adobe Creative Cloud products with Munki.

# Process

Munki can install Adobe CC deployment packages generated with Adobe's Creative Cloud Packager tool. The workflow is similar to that for CS5 and CS6 applications packaged with AAMEE.

## Overview:

1. Use Adobe's [Creative Cloud Packager](https://helpx.adobe.com/creative-cloud/packager.html) to package your Adobe CC product.
2. Import the Creative Cloud Packager's Install package and the Uninstall package for each product.

3. Make specific changes to some pkginfo files to accommodate problematic Adobe package behavior.

## Importing into Munki:

As of March 2015, Adobe Creative Cloud Packager lists 23 separate products.  You can use Creative Cloud Packager to create an installer package for each separate product, or any groups of products. If you plan to include updates in the main packages, you should first read the [note on including updates in the main CCP install packages](https://github.com/munki/munki/wiki/Munki-And-Adobe-CC#note-on-including-updates-in-the-main-ccp-install-packages) in the aamporter section towards the bottom.

You can import a specific package into Munki using `munkiimport`:
```
munkiimport /path/to/Build/AdobeCCProduct_Install.pkg --uninstallpkg /path/to/Build/AdobeCCProduct_Uninstall.pkg
```  
However, this will be quite tedious to do 23 times.  Thankfully, [Tim Sutton](https://github.com/timsutton) wrote a helpful script to automate importing the packages into Munki:
[https://github.com/timsutton/aamporter/blob/master/scripts/munkiimport_cc_installers.py](https://github.com/timsutton/aamporter/blob/master/scripts/munkiimport_cc_installers.py)  

You can make any organization-specific changes by editing [lines 41-44](https://github.com/timsutton/aamporter/blob/master/scripts/munkiimport_cc_installers.py#L41-L44) in the script to set your preferred location, category, and developer.

Execute the script on your CC Packages directory:
```
./munkiimport_cc_installers.py /path/to/CCPackages
```

## Fixing Broken Packages

**note: several of these issues were fixed with the release of Creative Cloud 2015.**

*Test Test Test*

Using `munkiimport` above with the correct `--uninstallpkg` switch will produce a working Munki install (and removal) for most of the products.  However, some of the Creative Cloud packages don't contain useful information inside that can generate a sane version number, and some of them don't generate the typical Adobe installs key, due to the way Creative Cloud Packager packages them.  

Specifically, [Adobe Acrobat Pro DC](https://creative.adobe.com/products/acrobat), [Edge Code](https://creative.adobe.com/products/code), [Edge Reflow](https://creative.adobe.com/products/reflow), [GamingSDK](https://creative.adobe.com/products/gaming-sdk), [Lightroom 5](http://www.adobe.com/products/photoshop-lightroom.html), and [Scout](https://creative.adobe.com/products/scout) do not generate useful data about their install, which will cause Munki to [loop these installs endlessly](https://github.com/munki/munki/wiki/FAQ#q-munki-successfully-installed-some-software-but-now-each-time-munki-runs-it-wants-to-install-the-software-again-why-is-this).  They also don't provide useful version numbers - munkiimport will automatically pick "1.0.0.0 - Please edit me!" because it can't find a better option.

Thus, these products need installs arrays.  These examples below may vary as version numbers are updated, but the process will generally be the same.

**Acrobat Pro DC:**  
Acrobat Pro DC installs two applications, "Adobe Acrobat.app" and "Acrobat Distiller.app" (and a shortcut to its uninstaller, contained inside the "Adobe Acrobat.app").  Use `makepkginfo -f /Applications/Adobe\ Acrobat\ DC/Adobe\ Acrobat.app -f /Applications/Adobe\ Acrobat\ DC/Acrobat\ Distiller.app` to generate an installs array and useful version number:
```
	<key>installs</key>
	<array>
		<dict>
			<key>CFBundleIdentifier</key>
			<string>com.adobe.Acrobat.Pro</string>
			<key>CFBundleName</key>
			<string>Acrobat Pro</string>
			<key>CFBundleShortVersionString</key>
			<string>15.007.20033</string>
			<key>CFBundleVersion</key>
			<string>15.007.20033</string>
			<key>minosversion</key>
			<string>10 . 4 . 3</string>
			<key>path</key>
			<string>/Applications/Adobe Acrobat DC/Adobe Acrobat.app</string>
			<key>type</key>
			<string>application</string>
			<key>version_comparison_key</key>
			<string>CFBundleShortVersionString</string>
		</dict>
```

Notice that Adobe did something stupid, which is to put a series of extraneous spaces inside the minosversion for the app bundle - "10 . 4 . 3."  Same thing happens with Acrobat Distiller.app:
```
		<dict>
			<key>CFBundleIdentifier</key>
			<string>com.adobe.distiller</string>
			<key>CFBundleName</key>
			<string>Distiller</string>
			<key>CFBundleShortVersionString</key>
			<string>15.007.20033</string>
			<key>CFBundleVersion</key>
			<string>15.007.20033</string>
			<key>minosversion</key>
			<string>10 . 4 . 3</string>
			<key>path</key>
			<string>/Applications/Adobe Acrobat DC/Acrobat Distiller.app</string>
			<key>type</key>
			<string>application</string>
			<key>version_comparison_key</key>
			<string>CFBundleShortVersionString</string>
		</dict>
	</array>
```

At least now there's a useful version number (in this case "15.007.20033"), which can replace the "1.0.0.0 - please edit me!" version that munkiimport tried to guess.

**note: Creative Cloud Packager has now fixed Uninstalls for Acrobat DC since v17.0**
Despite Creative Cloud Packager helpfully providing an uninstaller package, it doesn't actually function properly - it won't actually remove Acrobat Acrobat Pro DC.  However, Acrobat DC does install a number of receipts which list all of the files it brings along for the ride (all 10696 of them!).  You can see this using `pkgutil --pkgs | grep -i com.adobe.acrobat`.  These receipts can be put into a receipts array, which can be used for the "removepackages" uninstall method:
```
	<key>receipts</key>
	<array>
		<dict>
			<key>packageid</key>
			<string>com.adobe.acrobat.DC.viewer.app.pkg.MUI</string>
			<key>version</key>
			<string>15.007.20033</string>
		</dict>
		<dict>
			<key>packageid</key>
			<string>com.adobe.acrobat.DC.viewer.appsupport.pkg.MUI</string>
			<key>version</key>
			<string>15.007.20033</string>
		</dict>
		<dict>
			<key>packageid</key>
			<string>com.adobe.acrobat.DC.viewer.browser.pkg.MUI</string>
			<key>version</key>
			<string>15.007.20033</string>
		</dict>
		<dict>
			<key>packageid</key>
			<string>com.adobe.acrobat.DC.viewer.print_automator.pkg.MUI</string>
			<key>version</key>
			<string>15.007.20033</string>
		</dict>
		<dict>
			<key>packageid</key>
			<string>com.adobe.acrobat.DC.viewer.print_pdf_services.pkg.MUI</string>
			<key>version</key>
			<string>15.007.20033</string>
		</dict>
	</array>
	<key>uninstall_method</key>
	<string>removepackages</string>
	<key>uninstallable</key>
	<true/>
```

Since an installs array is present, the receipts won't be used to determine if the program is installed - but can be used to remove it on demand.

Acrobat DC also installs a linkCreation.dotm template into the Office 2011 Startup directory for Word. So Microsoft Word should be in the blocking applications:
```
        <key>blocking_applications</key>
        <array>
            <string>Microsoft Word</string>
        </array>
```

Unfortunately, the last thing left is that it creates an alias to the Uninstaller application, and this is not installed by package.  Thus, despite removing the packages, /Applications/Adobe Acrobat DC/ is still present, and contains a broken alias.  It can be removed, along with the Word template, using a postuninstall_script:
```
	<key>postuninstall_script</key>
	<string>#!/bin/sh
/bin/rm -rf /Applications/Adobe\ Acrobat\ DC/
/bin/rm -f /Applications/Microsoft\ Office\ 2011/Office/Startup/Word/linkCreation.dotm
	</string>
```

*Note about Acrobat DC and Acrobat Pro 11*: Acrobat Pro 11 uses a similar installs key in its pkginfo:
```
	<key>installs</key>
	<array>
		<dict>
			<key>CFBundleIdentifier</key>
			<string>com.adobe.Acrobat.Pro</string>
			<key>CFBundleName</key>
			<string>Acrobat</string>
			...
```
If your pkginfo for Acrobat Pro 11 has an installs array that contains these two elements, Acrobat Pro 11 will also (erroneously) report that it is installed and can be removed if Acrobat Pro DC is installed.  To address this issue (if you offer optional installs of both Acrobat Pro 11 and Acrobat Pro DC), remove the two keys above from the Acrobat Pro 11 installs array, to force Munki to verify based entirely on path.

**Edge Code CC:**  
Edge Code installs only a single application, which makes it easy to generate an installs array.  Use `makepkginfo -f /Applications/Adobe\ Edge\ Code\ CC.app`:
```
	<key>installs</key>
	<array>
		<dict>
			<key>CFBundleIdentifier</key>
			<string>com.adobe.EdgeCode</string>
			<key>CFBundleName</key>
			<string>Edge Code</string>
			<key>CFBundleShortVersionString</key>
			<string>0.98.0-359086275</string>
			<key>CFBundleVersion</key>
			<string>0.98.0-359086275</string>
			<key>path</key>
			<string>/Applications/Adobe Edge Code CC.app</string>
			<key>type</key>
			<string>application</string>
			<key>version_comparison_key</key>
			<string>CFBundleShortVersionString</string>
		</dict>
	</array>
```

Additionally, despite Creative Cloud Packager helpfully providing an uninstaller package, it doesn't actually function properly - running it with Installer.app fails, and removing the package with Munki doesn't remove the installed software.  Instead of relying on it, instead use an **uninstall_script** to delete the folder from /Applications and remove the package receipt:
```
	<key>uninstall_method</key>
	<string>uninstall_script</string>
	<key>uninstall_script</key>
	<string>#!/bin/sh
/bin/rm -rf "/Applications/Adobe Edge Code CC.app"
/usr/sbin/pkgutil --forget com.adobe.EdgeCode
	</string>
	<key>uninstallable</key>
	<true/>
```

**Edge Reflow CC:**  
Edge Reflow has the same problems as Edge Code, but also the same solutions.  Generate the installs array with `makepkginfo -f /Applications/Adobe\ Edge\ Reflow\ CC.app`:
```
	<key>installs</key>
	<array>
		<dict>
			<key>CFBundleIdentifier</key>
			<string>com.adobe.EdgeReflow</string>
			<key>CFBundleName</key>
			<string>Edge Reflow</string>
			<key>CFBundleShortVersionString</key>
			<string>0.51</string>
			<key>CFBundleVersion</key>
			<string>0.51</string>
			<key>path</key>
			<string>/Applications/Adobe Edge Reflow CC.app</string>
			<key>type</key>
			<string>application</string>
			<key>version_comparison_key</key>
			<string>CFBundleShortVersionString</string>
		</dict>
	</array>
```

Similarly, create an **uninstall_script**:
```
	<key>uninstall_method</key>
	<string>uninstall_script</string>
	<key>uninstall_script</key>
	<string>#!/bin/sh
/bin/rm -rf "/Applications/Adobe Edge Reflow CC.app"
/usr/sbin/pkgutil --forget com.adobe.pkg.Reflow
	</string>
	<key>uninstallable</key>
	<true/>	
```

**GamingSDK:**  
This doesn't install an application that you can query for a version, but instead includes a text file called `VersionInfo.txt`, which contains the version number in plain text.  As of writing time, the content of that file is "1.4.394", which gives an easy value to use in our pkginfo.  
Use `makepkginfo -f /Applications/Adobe\ Gaming\ SDK\ 1.4/VersionInfo.txt` to generate a simple md5 hash of it:
```
	<key>installs</key>
	<array>
		<dict>
			<key>md5checksum</key>
			<string>34ef3b5ada1541c9f997835ead3127a5</string>
			<key>path</key>
			<string>/Applications/Adobe Gaming SDK 1.4/VersionInfo.txt</string>
			<key>type</key>
			<string>file</string>
		</dict>
	</array>
```

As with Edge Code & Edge Reflow, use an **uninstall_script** to delete the folder from /Applications and remove the package receipt:  
```
	<key>uninstall_method</key>
	<string>uninstall_script</string>
	<key>uninstall_script</key>
	<string>#!/bin/sh
/bin/rm -rf "/Applications/Adobe Gaming SDK 1.4"
/usr/sbin/pkgutil --forget com.adobe.AdobeGamingSDK1.4.pkg
	</string>
	<key>uninstallable</key>
	<true/>
```

**Scout:**  
Scout requires an installs key as well, but also installs an application with sane version info contained inside the Info.plist, which makes `makepkginfo -f /Applications/Adobe\ Scout\ CC.app` helpful:
```
	<key>installs</key>
	<array>
		<dict>
			<key>CFBundleIdentifier</key>
			<string>com.adobe.Scout.application</string>
			<key>CFBundleName</key>
			<string>Scout</string>
			<key>CFBundleShortVersionString</key>
			<string>1.1.3</string>
			<key>CFBundleVersion</key>
			<string>1.1.3.354121</string>
			<key>path</key>
			<string>/Applications/Adobe Scout CC.app</string>
			<key>type</key>
			<string>application</string>
			<key>version_comparison_key</key>
			<string>CFBundleShortVersionString</string>
		</dict>
	</array>
```

Again, the uninstaller package won't do the right thing, so an **uninstall_script** is necessary:
```
	<key>uninstall_method</key>
	<string>uninstall_script</string>
	<key>uninstall_script</key>
	<string>#!/bin/sh
/bin/rm -rf "/Applications/Adobe Scout CC.app"
/usr/sbin/pkgutil --forget com.adobe.pkg.Scout
	</string>
	<key>uninstallable</key>
	<true/>
```

## Updating Adobe CC Products

Adobe CC is in the middle of transition of their installer tools, and so the methods available to add updates to Munki depend on exactly which applications and versions. [aamporter](https://github.com/timsutton/aamporter) was a convenient additional tool for automatically adding Adobe's "patch" installers but is of little relevance in early 2017, with most applications having been moved over to the newer installer tools. The old aamporter content in this wiki is preserved in the "2015 and earlier" section below, but if one is packaging current (as of 2017) applications, only a few applications still using the legacy "RIBS" installer remain (Lightroom 2015 being one).

### 2015.5 and later

All CC 2017 releases and the 2015 ".5" releases from June 2016 ship using a new installer technology known by Adobe as HyperDrive. This supports completely self-contained "update" installers which, to use Adobe's description, can be ["installed without a base version."](https://helpx.adobe.com/enterprise/kb/apps-deployed-without-base-versions.html)

To add these updates, package new versions using CCP and add them as previous versions were added. Any related updates like Camera Raw may be either included in the new packages or added separately as their own Munki items using `update_for` relationships.

### 2015 and earlier

Creative Cloud Packager is an important tool for creating standard Apple packages for Adobe's Creative Cloud products, and it helpfully bundles in updates with it.  You could use it to deploy updates for Adobe's CC products by repackaging them each time an update comes out, but doing this for each of the 23 separate products quickly becomes tedious.

Thankfully, Tim Sutton has provided a helpful tool to solve this problem - enter [aamporter](https://github.com/timsutton/aamporter).  aamporter is a command line utility that will search for updates for your specified products, download them, and import them into Munki.  It's important to read through the documentation in the [README](https://github.com/timsutton/aamporter/blob/master/README.md) first before continuing.

### Note on including updates in the main CCP install packages

Munki includes built-in support for Adobe patch updaters imported separately from the CCP install package, and so if you plan to use aamporter to automate these updates, it's preferable if the CCP packages include no additional updates, just the "base" product. In the days of AAMEE (CCP's predecessor), there were issues applying the Adobe patch updates to installs where the base installer included additional updates downloaded from AAMEE. With the arrival of Creative Cloud it's no longer possible to obtain these patch updates via Adobe's website to import manually, but aamporter is still able to download these updates from Adobe's feed and Munki still supports installing them "natively."

### Build the product plists

The first step is to create the product plist for each of your CC packages by pointing `aamporter` at each of the .ccp files inside your CC package folders:
```
./aamporter.py --build-product-plist /path/to/CCPackages/AfterEffectsCC/AfterEffectsCC.ccp
```
Doing this to all of your CCP packages will give you a bunch of plists.  That's what `aamporter` needs in order to cache the downloads, but there's some manual editing required in order to import these into Munki.  The Munki-specific features need to be added, either in each individual product plist, or in a generic ["aamporter.plist" file](https://github.com/timsutton/aamporter#aamporterplist-options) (or a combination of both).

Create your "aamporter.plist" file to contain generic information:
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>munkiimport_options</key>
	<array>
		<string>--category=AdobeUpdates</string>
		<string>--developer=Adobe</string>
	</array>
</dict>
</plist>
```
More can be specified (see [the documentation](https://github.com/timsutton/aamporter#aamporterplist-options) for details), but remember that options set in the aamporter.plist file will apply to every update.  If you want to sort your updates by product, you'll want to add the Munki-specific options to each product plist.  

Here's an example product plist for Adobe AfterEffects CC, with the Munki-specific features added:
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>channels</key>
	<array>
		<...snipped...>
	</array>
	<key>munki_update_for</key>
	<array>
		<string>AdobeAfterEffectsCC</string>
	</array>
	<key>munki_repo_destination_path</key>
	<string>updates/adobe/CC/AfterEffectsCC</string>
</dict>
</plist>
```

The `munki_update_for` option specifies that any updates from the channels listed will be imported to Munki with as an **update_for** an item named "AdobeAfterEffectsCC".  `munki_repo_destination_path` specifies where the files will be located in the Munki repo.  If you don't want specific locations for each update, this option can be placed in aamporter.plist instead.

### Importing the updates

With the product plists created and edited with your desired Munki configurations, it's time to begin the import process.  Here's an example command using a few of the CC products:
```
./aamporter.py --munkiimport AfterEffectsCC.ccp.plist AuditionCC.ccp.plist BridgeCC.ccp.plist DreamweaverCC.ccp.plist --make-catalogs
```

If you want to get fancy something like the following will work as well:

```
./aamporter.py --munkiimport /some/path/to/all/my/Adobe/packages/*/*.plist
```

As the documentation explains, the `--munkiimport` switch imports the packages into Munki with the information specified in aamporter.plist and the individual product plists. 

Check the repo to make sure the relationships for **update_for** are as expected.

Please read the [Caveats](https://github.com/timsutton/aamporter#caveats) for aamporter carefully, and test the updates thoroughly.