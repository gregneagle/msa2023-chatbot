### Introduction

Munki has support for a boolean 'autoremove' key, to specify items that should be automatically removed if they are not listed in 'managed_installs' in the client's manifest (or included manifests).

If an 'autoremove' item is listed in 'managed_updates' or in 'optional_installs' but not in 'managed_installs', that item will be removed.

### Details

An example:

```xml
    <key>autoremove</key>
    <true/>
    <key>name</key>
    <string>FinalCutPro7</string>
```

This means that if FinalCutPro7 is not listed in the "managed_installs" for a given client, it will be automatically removed. Think of it as a virtual entry in the "removals" list.

#### Issues:

- If you added this key to every package, the installcheck phase might take a very long time as it checked the installation status of everything in your repo. So you probably want to add this only to items in which you need to tightly control the installed base - like items with limited numbers of available license seats.

- There's a problem when you have overlapping items. For example, let's say you have these two items:
  - AdobePhotoshopCS4
  - AdobeCS4DesignStandard
  - If you mark these both for autoremoval (a logical thing to do), on a client that has AdobeCS4DesignStandard installed, installcheck will see that Photoshop CS4 is installed, note that AdobePhotoshopCS4 is NOT in the managed_installs list, and schedule AdobePhotoshopCS4 for removal -- which is not what you want.  So for now you'll need to NOT mark these sorts of items for autoremoval.

- munki 0.5.0 has an attempt to work around the above issue. If an item has an "installs" key, listing items that are installed, the code that considers an item for possible removal will not consider the item installed unless ALL items in the "installs" array are installed.
  - So - in the case of overlapping installable items like PhotoshopCS4 and AdobeCS4DesignStandard, you must ensure the "installs" list is unique for each item in an overlapping group. This allows the code that considers items for removal to distinquish between an install of just PhotoshopCS4 and one of a CS4 Suite, for example.
  - The flipside is that if something is installed and then partially deleted, munki won't be able to confirm that the item is actually installed, and will not attempt to remove it.