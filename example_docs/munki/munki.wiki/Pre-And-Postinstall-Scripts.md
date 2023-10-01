_Using pre and postinstall_scripts to avoid repackaging_

### Introduction

A common reason to repackage software is to perform additional configuration tasks or install additional items. You can often avoid repackaging by creating a separate package with your changes or additions and marking that package as an update_for the original package.

Another technique to avoid repackaging is to add a preinstall_script and/or a postinstall_script to the pkginfo for an item. These scripts can take care of some of the tasks you may have previously needed to resort to repackaging to implement.

These scripts can be in nearly any scripting language with an interpreter on the target systems. A "shebang line" to specify the script interpreter is mandatory. (You cannot use AppleScript "as-is", though you may be able to call some AppleScript by using `osascript`)

### Details

TextWrangler, a popular text editor, is distributed as a "drag-n-drop" disk image containing the TextWrangler application. But on first launch of the TextWrangler application, the user is prompted for admin credentials so some command-line tools can be installed. One approach to avoid this prompt is to repackage TextWrangler so that the applications and command-line tools are installed up front. But this can quickly become tedious as newer versions of TextWrangler are released.

An alternative is to implement a postinstall_script that copies the command-line tools from the TextWrangler bundle to their intended locations.  Here's an example of such a postinstall_script embedded into the pkginfo for TextWrangler 3.5.3:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>autoremove</key>
    <false/>
    <key>catalogs</key>
    <array>
        <string>production</string>
    </array>
    <key>description</key>
    <string>Free text editor from the makers of BBEdit</string>
    <key>display_name</key>
    <string>TextWrangler</string>
    <key>installer_item_hash</key>
    <string>4102747e33d6af3bfe19a1d4eaf9792d65bdf98952cefa9afcf1a008e5fda965</string>
    <key>installer_item_location</key>
    <string>apps/TextWrangler_3.5.3.dmg</string>
    <key>installer_item_size</key>
    <integer>12675</integer>
    <key>installer_type</key>
    <string>copy_from_dmg</string>
    <key>installs</key>
    <array>
        <dict>
            <key>CFBundleIdentifier</key>
            <string>com.barebones.textwrangler</string>
            <key>CFBundleName</key>
            <string>TextWrangler</string>
            <key>CFBundleShortVersionString</key>
            <string>3.5.3</string>
            <key>minosversion</key>
            <string>10.5</string>
            <key>path</key>
            <string>/Applications/TextWrangler.app</string>
            <key>type</key>
            <string>application</string>
        </dict>
    </array>
    <key>items_to_copy</key>
    <array>
        <dict>
            <key>destination_path</key>
            <string>/Applications</string>
            <key>source_item</key>
            <string>TextWrangler.app</string>
        </dict>
    </array>
    <key>minimum_os_version</key>
    <string>10.4.0</string>
    <key>name</key>
    <string>TextWrangler</string>
    <key>postinstall_script</key>
    <string>#!/bin/sh

mkdir -p -m 775 /usr/local/bin
cp /Applications/TextWrangler.app/Contents/MacOS/edit /usr/local/bin/
cp /Applications/TextWrangler.app/Contents/MacOS/twdiff /usr/local/bin/
cp /Applications/TextWrangler.app/Contents/MacOS/twfind /usr/local/bin/

mkdir -p -m 775 /usr/local/share/man/man1
cp /Applications/TextWrangler.app/Contents/Resources/edit.1 /usr/local/share/man/man1/
cp /Applications/TextWrangler.app/Contents/Resources/twdiff.1 /usr/local/share/man/man1/
cp /Applications/TextWrangler.app/Contents/Resources/twfind.1 /usr/local/share/man/man1/

exit 0
    </string>
    <key>uninstall_method</key>
    <string>remove_copied_items</string>
    <key>uninstallable</key>
    <true/>
    <key>version</key>
    <string>3.5.3</string>
</dict>
</plist>
```

Since these scripts are embedded in XML, you must escape certain characters that are special to the XML parser.
Specifically, the following characters and their corresponding XML entities:

* `&` is replaced with `&amp;`
* `<` is replaced with `&lt;`
* `>` is replaced with `&gt;`

You may want to use `makepkginfo` to do the escaping for you.

If your pre- or postinstall_script is in a file, you can generate the embedded version of the script, complete with proper escaping, with `makepkginfo` like so:

```bash
makepkginfo --postinstall_script /path/to/a/script
makepkginfo --preinstall_script /path/to/a/script
```

Additionally, GUI editing tools like MunkiAdmin, MunkiWebAdmin, and the like don't require this escaping if you aren't editing raw plists, as they do the escaping when converting a string into XML.

Failure of the preinstall_script will abort the installation attempt. 
Failure of the postinstall_script will log errors, but the install will be considered complete.

### Logging

```echo``` statements (or anything else that outputs to stdout) will be logged to ```/Library/Managed Installs/Logs/ManagedSoftwareUpdate.log```