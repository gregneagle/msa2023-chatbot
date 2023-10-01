_Info about Munki manifest files_

### Introduction

Format of Munki manifest files and supported keys


### Details

Manifests are essentially just a simple list of the items to install or verify their installation or to remove or verify their removal.

A basic manifest would contain a list of one or more catalogs to be searched for packages, and a list of packages to install. Here's an example:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
   <key>catalogs</key>
   <array>
      <string>production</string>
   </array>
   <key>managed_installs</key>
   <array>
      <string>Firefox</string>
      <string>Thunderbird</string>
   </array>
</dict>
</plist>
```

In this example, Munki is told to search the production catalog for Firefox and Thunderbird, and ensure the latest versions of these items are installed. The concept of "catalogs" is an important one. It is possible to have different versions of software available in different catalogs. A very common and powerful configuration is to maintain a "testing" catalog and a "production" catalog. New versions of software are first added to the "testing" catalog. Only a subset of managed machines is configured to use the "testing" catalog, and this subset gets the newer versions of software first. Once you are satisfied there are no major issues with a new version of a piece of software, you can add the new version to the "production" catalog, where the rest of your managed machines will find it and install it.

A useful metaphor to understand how manifests and catalogs interact is that of _a shopping list at a store._ A catalog can be thought of as the products available at the store, while a manifest can be thought of as the shopping list.

#### catalogs

The key 'catalogs' defines which catalogs to search for the given items. The catalogs are searched in order, but any valid match stops the search, so in the below example, a matching item in the testing catalog would stop the search - the production catalog would not be searched.

```xml
    <dict>
        <key>catalogs</key>
        <array>
            <string>testing</string>
            <string>production</string>
        </array>
        <key>managed_installs</key>
        <array>
            <string>ServerAdminTools</string>
            <string>TextWrangler</string>
            <string>Silverlight</string>
        </array>
    </dict>
```

#### included_manifests

Manifests support references to other manifests (nested manifests):

```xml
    <dict>
        <key>catalogs</key>
        <array>
            <string>testing</string>
            <string>production</string>
        </array>
        <key>included_manifests</key>
        <array>
            <string>standard_apps</string>
        </array>
        <key>managed_installs</key>
        <array>
            <string>TextWrangler</string>
        </array>
    </dict>
```

Where there is a manifest "standard_apps" that contains some, well, standard apps for your users:

```xml
    <dict>
        <key>managed_installs</key>
        <array>
            <string>MicrosoftOffice2008</string>
            <string>Firefox</string>
            <string>Thunderbird</string>
        </array>
    </dict>
```

##### included_manifests and catalogs

Included manifests do not need to have a "catalogs" array (**and in most cases, should *not* include a "catalogs" array**) -- if a catalogs array is not present, the catalogs of the parent manifest will be searched. The primary device manifest **must** contain a catalogs array; included manifests **should not**. Note this implies that a single manifest should not do "double-duty" as both a device manifest and an included manifest. For example, if you have a "site_default" device manifest, it should not also be used as an included manifest in other device manifests. Instead, move the common items into an included manifest that both "site_default" and device-specific manifests include.

#### managed_installs

managed_installs contains a list of items you would like to ensure are installed and kept up-to-date:

```xml
    <key>managed_installs</key>
    <array>
        <string>MicrosoftOffice2008</string>
        <string>Firefox</string>
        <string>Thunderbird</string>
    </array>
```

The names here (and for managed_uninstalls, managed_updates, optional_installs, and featured_items) correspond to the values for the "name" key of a pkginfo item. They are case-sensitive.

Think of this list as meaning "These items must be installed and must be kept up-to-date".

#### managed_uninstalls

You may include a "managed_uninstalls" key:

```xml
    <key>managed_uninstalls</key>
    <array>
        <string>ServerAdminTools</string>
        <string>TextWrangler</string>
        <string>Silverlight</string>
    </array>
```

These items will be checked to see if they're installed, and removed if possible.

Think of this list as meaning "These items must not be installed".

#### optional_installs

Manifests may also have an "optional_installs" key:

```xml
    <key>optional_installs</key>
    <array>
        <string>GoogleChrome</string>
        <string>GoogleEarth</string>
        <string>GoogleSketchUp</string>
        <string>TextWrangler</string>
    </array>
```

Optional installs allow administrators to specify packages as available for optional installation, allowing end-users to choose to install and/or remove these items without needing admin privileges themselves.

optional_installs items are checked against the available catalogs and added to the list of optional installs displayed in Managed Software Center.app. Users can then select any of these items for install, or if they are installed, for removal.

managed_installs and managed_uninstalls have higher precedence than optional_installs, so if an item is in either a managed_installs or managed_uninstalls list, it will not be displayed in Managed Software Center.app as an available optional install.

If a user chooses items to install or remove from the list of optional software, the choices are recorded in a locally-generated manifest: "/Library/Managed Installs/manifests/SelfServeManifest". This manifest inherits its catalogs from the primary manifest (the one pointed to by the ClientIdentifier) and is processed like any other manifest after all of the server-provided manifests have been processed. 

To be more explicit, items selected to be installed by an end user become `managed_installs` (or `managed_uninstalls` if subsequently selected to be removed), and any keys set in the pkginfo file for the item are respected. The expected behavior is therefore that any new versions of items previously selected for install by an end user (which share the same 'name' key) will be handled like any other managed install: end users would not need to explicitly launch Managed Software Center to re-select the item, nor should they see prompts if unattended_install was configured (unless blocking apps or other reasons to prompt a user were triggered). 

#### featured_items

Manifests may also have a "featured_items" key:

```xml
    <key>featured_items</key>
    <array>
        <string>Office2016</string>
        <string>Slack</string>
        <string>SuperSolitaire2017</string>
    </array>
```

The list of featured items will replace the "All Items" view in Managed Software Center, if featured_items is present. In order for items to be featured, they must be also included in the optional_installs list.

For more information on featured items, see [[Featured Items in Managed Software Center]].

#### managed_updates

The value for this key is in the same format as managed_installs. Items in managed_updates are each checked to see if **some** version of the item is already installed; if so, the item is processed just as if it was in the managed_installs list. You could use managed_updates to tell Munki to update software that is not in a managed_installs list; for example, if you have machines that may or may not have Adobe Photoshop CS5 and you do not want to add Adobe Photoshop CS5 to a managed_installs list, but would still like Munki to apply any applicable updates, you could add Adobe Photoshop CS5 to the managed_updates list.

An item in a managed_updates list that is scheduled for removal (because it appears in a managed_uninstalls list) will not be processed for updates.

Think of this list as meaning "These items must be kept up-to-date if they happen to be installed".
This is **not** the place to put updates for items that are listed in managed_installs. See the [update_for key in pkginfo files](Pkginfo-Files#update_for) for how to handle update items.

#### default_installs

Munki 6.1 added support for `default_installs`. Read more about them [here](Default-Installs).

#### conditional_items

Items can be added to a manifest conditionally. See [[Conditional Items]] for more information.

#### item names

For managed_installs, managed_uninstalls and optional_installs, items are typically referred to by name only, but  you can append the version number, which causes Munki to look for that specific version:

```xml
    <key>managed_installs</key>
    <array>
        <string>MicrosoftOffice2008</string>
        <string>Firefox-3.0.9</string>
        <string>Thunderbird</string>
    </array>
```

In the above example, the catalog(s) will be searched for the latest version of MicrosoftOffice2008, version 3.0.9 of Firefox, and the latest version of Thunderbird.

If the version contains a dash (-), separate the name and version with two dashes. For example, Firefox version 3.0.9-rc would become Firefox--3.0.9-rc.

Note that Munki generally will not downgrade an existing install from a newer version to an older version, so specifying an older version in the managed_installs list will not downgrade existing installations.

NOTE: this is _not_ Munki's primary method for ensuring a specific version of a specific software is installed. The primary mechanism for that is [catalogs](Using-Munki-Catalogs). Avoid using this mechanism if at all possible as there are many untested/undocumented/undefined edge cases around this mechanism. It _is_ appropriate for "quick-and-dirty" testing, or for defining "update_for" and/or "requires" dependencies that are for specific software versions.

managed_updates should list the item only without a version number.

For managed_installs, managed_uninstalls, optional_installs, and managed_updates, the name used in the manifest will be matched against the "name" field in each item in each catalog listed in the catalogs attribute of the manifest.

#### See Also
[https://groob.io/posts/manifest-guide/](https://groob.io/posts/manifest-guide/)  
[https://technology.siprep.org/another-opinionated-guide-to-munki-manifests/](https://technology.siprep.org/another-opinionated-guide-to-munki-manifests/)