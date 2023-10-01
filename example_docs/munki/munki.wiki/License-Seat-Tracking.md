_Information on Munki's support for querying for available license seats for uninstalled optional_installs_

### Introduction

Beginning with the 0.9.1 builds of the munki tools, Munki can query a webserver to determine if there are available seats for licensed software (or any software you wish to make available via optional_installs, yet control the number of deployed copies).


### Details

#### What's needed

- Client running munkitools 0.9.1.x or later
- Web service that is tracking available seats and that provides information in a specific format in response to queries. One such server is Sal (or the deprecated original MunkiWebAdmin *not* mwa2)

#### Using Sal

Follow the instructions to install Sal: https://github.com/salopensource/sal/wiki/Getting-Started

Once you have Sal functioning with license seat tracking, and you've updated one or more munki clients to 0.9.1.x, you'll need to tell the client(s) where to ask for license info. This is stored in Munki's preferences in LicenseInfoURL:

For Sal this includes the long key string assigned to the machine group:

```bash
% defaults read /Library/Preferences/ManagedInstalls LicenseInfoURL
https://sal.example.com/licenses/available/yourreallyreallyreallyreallylongkey
```
#### Using MunkiWebAdmin

If you have a running instance of MunkiWebAdmin, make sure you've updated to the latest code.
See this post: https://groups.google.com/d/msg/munki-web-admin/rofv6CiYNto/MzwvP3CGEFIJ for basic info on entering license seat info in MunkiWebAdmin.

Once you have MWA functioning with license seat tracking, and you'd updated one or more clients to 0.9.1.x, you'll need to tell the client(s) where to ask for license info. This is stored in Munki's preferences in LicenseInfoURL:

```bash
% defaults read /Library/Preferences/ManagedInstalls LicenseInfoURL
http://mwa.example.com:8444/licenses/available/
```

### Editing pkginfo

You must mark the pkginfo for any licensed item to say "this one has licensed seat info on the server". Only uninstalled optional installs with this key will be checked for available licensed seats; if there is no response from the server, we act as though the number of available seats is zero. 

```xml
<key>licensed_seat_info_available</key>
<true/>
```

#### How does this work?

During a managedsoftwareupdate run that includes checking with the server for updates, if there are any uninstalled optional_installs that have `licensed_seat_info_available=true` Munki crafts one or more queries of the form:

`LicenseInfoURL?name=ItemOne&name=ItemTwo&name=ItemThree`

where LicenseInfoURL is the license info URL (for MunkiWebAdmin, that's something like http://mwaserver/licenses/available/) and ItemOne, ItemTwo and ItemThree are names of pkginfo items.

The server then looks up license seat info for ItemOne, ItemTwo and ItemThree and responds with a plist:

```bash
% curl "http://mwa.example.com:8444/licenses/available/?name=MicrosoftOffice2008&name=MicrosoftOffice2011&name=FooBarBaz"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>MicrosoftOffice2008</key>
    <false/>
    <key>MicrosoftOffice2011</key>
    <true/>
</dict>
</plist>
```

The returned plist should contain key/value pairs, where the key is the item name and the value is a boolean: true if there are available seats, false otherwise. If the server has no information for an item (as is the case for item "FooBarBaz") it is acceptable to return nothing. A request and response for only "FooBarBaz" looks like this:

```bash
% curl "http://mwa.example.com:8444/licenses/available/?name=FooBarBaz"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
</dict>
</plist>
```

The returned results are recorded in `/Library/Managed Installs/InstallInfo.plist`. Any optional_installs item with license seat info gets a new key -- **`licensed_seats_available`**:

```xml
<dict>
    <key>description</key>
    <string>Installs Adobe Photoshop CS5 and related components.</string>
    <key>display_name</key>
    <string>Adobe Photoshop CS5</string>
    <key>installed</key>
    <false/>
    <key>installed_size</key>
    <integer>1028875</integer>
    <key>installer_item_size</key>
    <integer>1028875</integer>
    <key>licensed_seats_available</key>
    <true/>
    <key>name</key>
    <string>AdobePhotoshopCS5</string>
    <key>uninstallable</key>
    <true/>
    <key>version_to_install</key>
    <string>12.0.0.0.0</string>
</dict>
```

When Managed Software Center is displaying Optional Software, any item with a `licensed_seats_available` key equal to `false` will have its Install button disabled and the text will say "Unavailable", preventing a user from selecting it for install. Additionally, the Status text will read "No licenses available".

Note that there is no explicit mechanism for a client to notify the server that it has installed an item (or will install an item). Instead, the client submits an updated ApplicationInventory.plist to the server. The server uses this information to determine the number of installed seats. (A server other than MunkiWebAdmin is free to use some other method to determine the number of installed seats.)
