_Automatic removal of unused/underused optional\_installs_

### Introduction

New for Munki 3: Munki can track application usage and can use this information to automatically remove optional_installs items that have not been used for a period of time.

This can be used to automatically remove expensive software from machines where it is not being actively used.


### Overview

To use this feature, you can add a new key and dictionary to a pkginfo item. An example:

```xml
<key>unused_software_removal_info</key>
<dict>
    <key>bundle_ids</key>
    <array>
        <string>com.foo.app1</string>
        <string>com.foo.app2</string>
    </array>
    <key>removal_days</key>
    <integer>90</integer>
</dict>
```

The `unused_software_removal_info` dictionary can contain two keys:

* `bundle_ids` This is optional, and must contain a list of strings. Each string is the bundle id of an application that will be checked to see if it was activated in the past `removal_days` days. If it doesn't exist, bundle_ids will be extracted from applications in the `installs` array if it exists.
* `removal_days` This is required, and is an integer. If no application in the list of bundle_ids has been activated in the past `removal_days` days, and the item has not been installed in the past `removal_days` days, the item will be added to the list of things to be removed, and if the item is in the SelfServeManifest list of managed_installs, it will be removed from that list.


### How it works

The new version of Munki introduces a new background process (`app_usage_monitor`) that registers for some notifications.

It registers for the NSWorkspace notifications for app launch, quit and activate, and records these events in a database named "application_usage.sqlite" in Munki's local data directory (typically /Library/Managed Installs).

The same process also registers for a 'com.googlecode.munki.managedsoftwareupdate.installrequest' notification, which is posted by Managed Software Center 4.3.x or later when a user chooses to install an item from optional installs.

During a managedsoftwareupdate run, Munki processes optional\_installs from the available manifests. For each optional\_installs item, if the item is determined to be currently installed, Munki then checks to see if the item has unused\_software\_removal_info. If so, it then:

* Is there application usage data at least as far back as `removal_days`?
* If so, was there an install request for this item in the past `removal_days`?
* If not, get a list of bundle_ids of applications to check.
* Loop through each bundle_id; if no application is currently running and has not been activated in the past `removal_days`, then add this item to the removal list and remove it from the SelfServeManifest's managed_installs (if it's there)


### Considerations

This functionality works _only_ with optional\_installs. Items listed as managed\_installs will not be considered for removal due to non-use.

Since this feature works by checking the usage of _applications_, it cannot be used to remove unused software that does not have an application component: for example, you could not use this mechanism to reliably remove unused fonts, or the Adobe Flash Player plugin due to non-use.

Items must have a functional uninstall method.

Items need not be in the current SelfServeManifest managed\_installs to be considered for removal; they need only be in optional_installs in any applicable manifest (and not in managed_installs in any server-based manifest that is applied to the current machine).

`unused_software_removal_info` is stored in pkginfo items. If you add this information to ExpensiveSoftware-1.0 and later import ExpensiveSoftware-1.1, be sure to copy the `unused_software_removal_info` to the new pkginfo.


### Database schema

The database contains two tables. Here are the SQL statements that create them:
``` 
CREATE TABLE application_usage (
    event TEXT,
    bundle_id TEXT,
    app_version TEXT,
    app_path TEXT,
    last_time INTEGER DEFAULT 0,
    number_times INTEGER DEFAULT 0,
    PRIMARY KEY (event, bundle_id)
)

CREATE TABLE install_requests (
    event TEXT,
    item_name TEXT,
    item_version TEXT,
    last_time INTEGER DEFAULT 0,
    number_times INTEGER DEFAULT 0,
    PRIMARY KEY (event, item_name)
)
```