### Introduction

In order to more easily integrate Munki with other management systems, Munki supports a "LocalOnlyManifest". This is simply a manifest file stored locally on the client. It is created/managed/installed by some other management tool, perhaps Puppet, or Chef, or even Jamf Pro.

This feature can be safely ignored by most Munki admins.

### Implementation

A Munki preference, `LocalOnlyManifest`, defines the name of a locally-installed manifest, typically managed/created/installed by some external management system.

Creating a `LocalOnlyManifest` enables administrators to specify additional `managed_installs`,  `managed_uninstalls` or `optional_installs` in a local file that augments those defined on the Munki server. 

For example, if your Munki client is inheriting the `site_default` manifest and you wanted to add a managed_install without editing that server-side manifest, you could define a `LocalOnlyManifest` and populate it with the selected package ...

Define a LocalOnlyManifest:

    sudo defaults write /Library/Preferences/ManagedInstalls LocalOnlyManifest extra_packages

Contents of `/Library/Managed Installs/manifests/extra_packages`:

```XML
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>managed_installs</key>
    <array>
        <string>Firefox</string>
    </array>
    <key>managed_uninstalls</key>
    <array>
        <string>GoogleChrome</string>
    </array>
</dict>
</plist>
```

This example ensures Firefox remains added to the list of managed_installs, and GoogleChrome remains added to the list of managed_uninstalls. As with any manifests, the admin must be careful not to create contradictions.

**NOTE**: Adding additional `catalogs` to your LocalOnlyManifest will have _no effect_. Packages managed using a LocalOnlyManifest must already be present in the available catalogs.
