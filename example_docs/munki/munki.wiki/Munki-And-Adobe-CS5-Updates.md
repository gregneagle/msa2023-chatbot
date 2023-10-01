### Introduction

Information on using munki with Adobe CS5 updates

### Details

Starting with version 0.5.2.553.0 of the munki tools, munki can handle Adobe CS5 updates, which have an application named "AdobePatchInstaller.app" at the root of the disk image.

Dealing with CS5 updates is very similar to dealing with CS3/CS4 updates.

**Important note #1:** Do not repackage CS5 updates using AAMEE. Simply use munkiimport to import the diskimage as downloaded from Adobe.

**Important note #2:** Some CS5 updates might refuse to install when there is no user logged in via the GUI. I have not been able to verify this conclusively, but it appears that if you've installed a CS5 product using a package generated with the pre-release version of Adobe Application Manager, Enterprise Edition (AAMEE) instead of the "final" 1.0 version of AAMEE, that any updates installed for this product will exhibit the issue of not being able to be installed when there is not logged-in user. If the "base" product was installed using a package generated with AAMEE 1.0 (final), updates will install successfully with no logged-in user.

Updates verified to work:

* Flash Professional CS5 Update 11.0.2
* After Effects CS5 10.0.1 Update
* Adobe Player for Embedding 3.1 -- Requires copy_local = "True" in pkginfo. See below.
* Adobe Premiere Pro CS5 5.0.2 Update
* Adobe Dreamweaver CS5 11.0.3 Updater
* Adobe Camera Raw 6.2 Update
* Adobe Community Help 3.3 -- Must be repackaged. See https://managingosx.wordpress.com/2010/09/03/updating-adobe-help-for-cs5/
* Adobe CSXS Infrastructure CS5 2.0.1 Update (CS Live)
* Adobe Pixel Bender Plug-in for Adobe Photoshop CS5: Must be packaged with AAMEE.
* Adobe IllustratorCS5 15.0.1 Update
* Adobe InDesign CS5 7.0.2 Update
* Adobe XMP Panels CS5 update (July 22, 2010) -- Requires copy_local = "True" in pkginfo. See below.
* Adobe DeviceCentral CS5 3.0.1 Update
* Adobe Flash Builder 4 4.0.1 Update
* Adobe Photoshop CS5 12.0.1 update
* Adobe Bridge CS5 4.0.3 update
* Adobe Flash Professional CS5 Update 11.0.1
* Adobe OnLocation CS5 5.0.1

Older updates that work -- these have been superceded by later cumulative updates:

* Adobe Dreamweaver 11.0.2 update
* Adobe Camera Raw 6.1 update

**copy_local workaround:** These updates fail with "Exit Code: 7 - Unable to complete Silent workflow" whether or not a user is logged in:

* Adobe XMP Panel CS5 - Jul 22, 2010
* Adobe Player for Embedding 3.1

    Errors in the log are:

* ERROR: No media information provided for removable source location
* ERROR: Cannot iniliatize payload session

When the contents of the disk image are copied locally, the update succeeds, so this is a variation of the problem with installs from disk images.

Workaround: using munki tools 0.6.0.633.0 or later, add the following key to the pkginfo:

```xml
    <key>copy_local</key>
    <true/>
```

This causes munki to copy the disk image contents to the local disk before installing them. Currently, this key works only with Adobe CS5 updates.

#### makepkginfo and Adobe CS5 updates

Run makepkginfo against an update disk image to generate a basic pkginfo file. munki will generate a (hopefully) functional "installs" key based on the AdobeCodes for the installed payloads. You can manually add additional "installs" items, and must manually add an "update_for" entry. Here's an example:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
        <key>catalogs</key>
        <array>
                <string>testing</string>
        </array>
        <key>description</key>
        <string></string>
        <key>display_name</key>
        <string>Adobe Bridge CS5</string>
        <key>installed_size</key>
        <integer>177358</integer>
        <key>installer_item_location</key>
        <string>AdobeBridge_4.0.2_mul_AdobeUpdate.dmg</string>
        <key>installer_item_size</key>
        <integer>8952</integer>
        <key>installer_type</key>
        <string>AdobeCS5PatchInstaller</string>
        <key>installs</key>
        <array>
                <dict>
                        <key>CFBundleIdentifier</key>
                        <string>com.adobe.bridge4</string>
                        <key>CFBundleName</key>
                        <string>Adobe Bridge CS5</string>
                        <key>CFBundleShortVersionString</key>
                        <string>4.0.2.1</string>
                        <key>path</key>
                        <string>/Applications/Adobe Bridge CS5/Adobe Bridge CS5.app</string>
                        <key>type</key>
                        <string>application</string>
                </dict>
        </array>
        <key>minimum_os_version</key>
        <string>10.4.0</string>
        <key>name</key>
        <string>AdobeBridgeCS5</string>
        <key>payloads</key>
        <array>
                <dict>
                        <key>AdobeCode</key>
                        <string>{2C8FBE83-2D3E-4CE6-A912-4BED85BCAC06}</string>
                        <key>display_name</key>
                        <string>Adobe Bridge CS5</string>
                        <key>installed_size</key>
                        <integer>177358</integer>
                        <key>version</key>
                        <string>4.0.2.0.0</string>
                </dict>
        </array>
        <key>uninstallable</key>
        <false/>
        <key>update_for</key>
        <array>
                <string>AdobeDesignStandardCS5</string>
                <string>AdobeMasterCollectionCS5</string>
                <string>AdobeProductionPremiumCS5</string>
                <string>AdobePhotoshopCS5</string>
        </array>
        <key>version</key>
        <string>4.0.2.0.0</string>
</dict>
</plist>
```