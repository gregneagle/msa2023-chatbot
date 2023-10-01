_Basic info on product icons for Munki 2+_

### Introduction

The Managed Software Center application displays "icons" (or more accurately, *artwork*) for software items. If you don't want a boring interface full of generic package icons, you should provide artwork for Managed Software Center to display.

![](https://github.com/munki/munki/wiki/images/managed_software_center.png)

### Details

Product artwork is typically stored in a new "icons" directory in your Munki repo. The preferred format is PNG. The preferred resolution is 350x350 or higher. (Though higher will use more disk space without an improvement in appearance.)

>**Note**:  Some web servers are configured to redirect requests for items in a top-level "icons" directory to some other directory. Configure your web server appropriately, or use the IconURL preference in Munki's preferences to direct the client to use a different URL. See  [[here|Preferences#supported-managedinstalls-keys]] for more information on Munki's preferences. See your web server's documentation for configuration information for your web server.

`managedsoftwareupdate` attempts to download product artwork for all optional items and any managed_installs or removals that are currently applicable.

When looking for product artwork, `managedsoftwareupdate` checks for an 'icon_name" key in the item's pkginfo. If this exists and has a file extension, the filename is requested. Otherwise, ".png" is appended to the name to be requested. If the pkginfo does *not* have an  'icon_name" key, the pkginfo "name" key plus ".png" will be requested.

**Example:**

For a pkginfo item with the name "Firefox" that has no "icon_name" defined, `managedsoftwareupdate` might request "http://munki/repo/icons/Firefox.png" (Exact URL depends on Munki's SoftwareRepoURL and **IconURL** preferences.)

If for some reason you wish to store your icons under an alternative URL, you can set Munki's **IconURL** to your desired base URL. This follows the pattern of ManifestURL, CatalogURL and PackageURL as alternate base URLs.

#### Making icons

#### iconimporter

There is a tool available to assist with the process of generating product icons for an existing repo. 

`/usr/local/munki/iconimporter /path/to/repo_root`

...will find the latest versions of every item in your Munki repo and attempt to extract application icons from each item, convert the icons to png files and save them under `repo_root/icons` as `name.png`, where 'name' is the value of the name key in the relevant pkginfo.

Some packages will contain multiple application icons. In this case, `iconimporter` extracts them all, saving them as `name_1.png`, `name_2.png`, `name_3.png`. It's up to you to look at the icons, rename the one you want to use, and delete the remainder.

`iconimporter` only attempts to extract icons from `copy_from_dmg` installers and Apple pkg installers.

`iconimporter --help` for a full usage message.

#### munkiimport

`munkiimport` will now offer to attempt to extract an icon for items that don't already have an icon in the repo:

    % munkiimport GoogleChrome.dmg
    This item is similar to an existing item in the repo:
                Item name: GoogleChrome
             Display name: Google Chrome
              Description: Google's web browser.
                  Version: 34.0.1847.137
      Installer item path: apps/GoogleChrome-34.0.1847.137.dmg
    
    Use existing item as a template? [y/n] y
    
    <...snip...>
    
    Import this item? [y/n] y
    Attempt to create a product icon? [y/n] y
    Attempting to extract and upload icon...
    Created icon: /Users/Shared/munki_repo/icons/GoogleChrome.png
    Copying GoogleChrome.dmg to /Users/Shared/munki_repo/pkgs/apps/GoogleChrome-35.0.1916.114.dmg...
    Saving pkginfo to /Users/Shared/munki_repo/pkgsinfo/apps/GoogleChrome-35.0.1916.114.plist...
    Rebuild catalogs? [y/n] y
    Rebuilding catalogs at /Users/Shared/munki_repo...

#### Behind the scenes

`managedsoftwareupdate` downloads any available product icons into the Munki data directory (typically `/Library/Managed Installs`) inside an `icons` subdirectory. On launch, Managed Software Center.app creates a symlink to that directory in its html directory: `~/Library/Caches/com.googlecode.munki.ManagedSoftwareCenter/html/icons`