### Introduction

The copy_from_dmg installer type is typically used for "drag-n-drop" disk images; where the vendor has supplied their software on a disk image and expects the user to drag the software from the mounted disk image to some place on the the startup disk (typically, but not always, `/Applications/`).

copy_from_dmg supports copying arbitrary items from a disk image to arbitrary locations on the startup disk. You can also specify owner, group, and mode for the copied items.


### Details

The `munkiimport` tool will automatically generate a pkginfo file using copy_from_dmg if the item to be imported is a disk image that contains an application at the root of the mounted filesystem.

You can manually create a pkginfo file using the copy_from_dmg method. Use `makepkginfo` to create a pkginfo item like so:

```bash
makepkginfo /Volumes/repo/pkgs/apps/GoogleEarthMacNoUpdate-Intel-5.2.dmg --owner=root --group=admin --mode=go-w --item="Google Earth Web Plug-in.plugin" --destinationpath="/Library/Internet Plug-ins"
```

This creates a pkginfo item instructing Munki to copy "Google Earth Web Plug-in.plugin" from the root of the mounted disk image to "/Library/Internet Plug-ins"; to set its owner to "root," group to "admin," and to remove the write bit for "other". The resulting plist looks like this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>autoremove</key>
    <false/>
    <key>catalogs</key>
    <array>
        <string>testing</string>
    </array>
    <key>installer_item_location</key>
    <string>apps/GoogleEarthMacNoUpdate-Intel-5.2.dmg</string>
    <key>installer_item_size</key>
    <integer>23168</integer>
    <key>installer_type</key>
    <string>copy_from_dmg</string>
    <key>installs</key>
    <array>
        <dict>
            <key>CFBundleShortVersionString</key>
            <string>5.2</string>
            <key>path</key>
            <string>/Library/Internet Plug-ins/Google Earth Web Plug-in.plugin</string>
            <key>type</key>
            <string>bundle</string>
        </dict>
    </array>
    <key>items_to_copy</key>
    <array>
        <dict>
            <key>destination_path</key>
            <string>/Library/Internet Plug-ins</string>
            <key>group</key>
            <string>admin</string>
            <key>mode</key>
            <string>go-w</string>
            <key>source_item</key>
            <string>Google Earth Web Plug-in.plugin</string>
            <key>user</key>
            <string>root</string>
        </dict>
    </array>
    <key>minimum_os_version</key>
    <string>10.4.0</string>
    <key>name</key>
    <string>Google Earth Web Plug-in</string>
    <key>uninstall_method</key>
    <string>remove_copied_items</string>
    <key>uninstallable</key>
    <true/>
    <key>version</key>
    <string>5.2.0.0.0</string>
</dict>
</plist>
```

The Google Earth disk image actually contains two items you might want to install -- the Google Earth application itself, and the Google Earth Web Plug-in. You have two options here:

1. Create two separate pkginfo items, one for Google Earth.app and one for Google Earth Web Plug-in.plugin. You could then add an "update_for" key to the Google Earth Web Plug-in item, marking it as an update for Google Earth. When munki is instructed to install Google Earth, it will install the Google Earth Web Plug-in as well.<br><br>
1. Combine the "installs" and "items_to_copy" sections from the two pkginfo items into a single pkginfo item.  makepkginfo currently only supports a single installation item when creating a copy_from_dmg pkginfo item, but the plist itself can support multiple items. Such a combined pkginfo item would look like this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>autoremove</key>
    <false/>
    <key>catalogs</key>
    <array>
        <string>testing</string>
    </array>
    <key>installer_item_location</key>
    <string>apps/GoogleEarthMacNoUpdate-Intel-5.2.dmg</string>
    <key>installer_item_size</key>
    <integer>23168</integer>
    <key>installer_type</key>
    <string>copy_from_dmg</string>
    <key>installs</key>
    <array>
        <dict>
            <key>CFBundleIdentifier</key>
            <string>com.Google.GoogleEarthPlus</string>
            <key>CFBundleName</key>
            <string>Google Earth</string>
            <key>CFBundleShortVersionString</key>
            <string>5.2</string>
            <key>path</key>
            <string>/Applications/Google Earth.app</string>
            <key>type</key>
            <string>application</string>
        </dict>
        <dict>
            <key>CFBundleShortVersionString</key>
            <string>5.2</string>
            <key>path</key>
            <string>/Library/Internet Plug-ins/Google Earth Web Plug-in.plugin</string>
            <key>type</key>
            <string>bundle</string>
        </dict>
    </array>
    <key>items_to_copy</key>
    <array>
        <dict>
            <key>destination_path</key>
            <string>/Applications</string>
            <key>source_item</key>
            <string>Google Earth.app</string>
        </dict>
        <dict>
            <key>destination_path</key>
            <string>/Library/Internet Plug-ins</string>
            <key>group</key>
            <string>admin</string>
            <key>mode</key>
            <string>go-w</string>
            <key>source_item</key>
            <string>Google Earth Web Plug-in.plugin</string>
            <key>user</key>
            <string>root</string>
        </dict>
    </array>
    <key>minimum_os_version</key>
    <string>10.4.0</string>
    <key>name</key>
    <string>Google Earth</string>
    <key>uninstall_method</key>
    <string>remove_copied_items</string>
    <key>uninstallable</key>
    <true/>
    <key>version</key>
    <string>5.2.0.0.0</string>
</dict>
</plist>
```