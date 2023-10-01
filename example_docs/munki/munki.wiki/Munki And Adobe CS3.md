_Notes on installing/removing Adobe CS3 apps with Munki_

### Details

As of the 0.4.7 release of the munki tools, munki now supports installation and removal of Adobe CS3 applications using disk image copies of the CS3 install media and prepared according to Adobe's documentation here:

http://www.adobe.com/support/deployment/cs3_deployment.pdf

You'll need to follow Adobe's instructions for creating the install.xml, uninstall.xml and application.xml.override files.

One possible variation from the Adobe instructions: the install.xml and uninstall.xml files must be saved at the root of the DMG.

Once you've created a disk image of the install media and added the xml files, test the install and removal -- if they don't work manually, they won't work with munki. Testing the silent install is described as **Perform a silent install or uninstall** in the Adobe CS3 Deployment documentation.

You may optionally create an uninstaller dmg for the product - this is just a copy of the installer dmg minus all of the embedded dmg files in the payloads directory.  Be sure to leave the Bootstrapper.dmg alone! An advantage of creating an uninstaller dmg is that is is much smaller (it can be 10% the size of the installer dmg).

makepkginfo can create the needed pkg info for an Adobe CS3 installer dmg. Be aware that since Adobe installer dmgs don't use the Apple pkg format, there are no receipts. This is important to note since munki needs a way to determine if an item is already installed. With standard Apple packages, munki can just look for the receipts. With Adobe installers, you must add "installs" items to the pkg info, like so:

    <key>installs</key>
    <array>
    	<dict>
    		<key>CFBundleIdentifier</key>
    		<string>com.adobe.Photoshop</string>
    		<key>CFBundleName</key>
    		<string>Photoshop</string>
    		<key>CFBundleShortVersionString</key>
    		<string>10.0</string>
    		<key>path</key>
    		<string>/Applications/Adobe Photoshop CS3/Adobe Photoshop CS3.app</string>
    		<key>type</key>
    		<string>application</string>
    	</dict>
    </array>

These can be generated either when creating the original pkginfo, or later, like so:

`makepkginfo -f /Applications/Adobe\ Photoshop\ CS3/Adobe\ Photoshop\ CS3.app`

munki can then check for the existence of the "installs" items to tell if the item has been installed.

See [[Munki And Adobe CS4]] for related info.