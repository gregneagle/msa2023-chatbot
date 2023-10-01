**The appdmg install type is now deprecated**, having been superseded by [copy_from_dmg](https://github.com/munki/munki/wiki/CopyFromDMG).

copy_from_dmg was released with the 0.6.2 munkitools, and can do everything appdmg can, plus more.  makepkginfo now creates pkginfo items with copy_from_dmg install methods instead of appdmg for "drag-and-drop" disk images. See https://github.com/munki/munki/wiki/CopyFromDMG for more information.

The rest of this document is historical in nature.

# Introduction

As of the 0.4.4 release, you can use disk images that contain a single application as a type of munki package. These are usually "drag-and-drop" disk images, where the user is expected to drag the app to the /Applications folder (or actually anywhere on the local disk).
munki will copy a single application to the /Applications folder on the startup disk.

munki's internal name for this type of installer item is "appdmg".

# Details

This feature is meant as a convenience for systems administrators. Instead of having to repackage a drag-and-drop disk image as an Apple installer, admins can simply use the original disk image.

Using this format directly instead of repackaging is not recommended if you need to make changes to the app bundle itself before deployment (Firefox customizations come to mind), or the app offers to install additional items that require admin authorization on first launch (examples include TextMate, TextWrangler, and BBEdit, which offer to install command-line tools on first launch).

This won't work with disk images that require the user to agree to a Software License Agreement when the disk image is double-clicked in the Finder -- hidutil cannot mount these images without user intervention. You'll either have to create a new disk image minus the Software License Agreement, or just package the app into an Apple package.

If removal is requested, munki uses the path to the app as specified in the "installs" key to do a simple `rm -rf` of the application bundle.

Sample output from `makepkginfo /path/to/Firefox 3.5.3.dmg`:

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