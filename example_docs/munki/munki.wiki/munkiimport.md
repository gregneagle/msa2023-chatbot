_Tool for importing packages into your Munki repository_

### Introduction

`munkiimport` is a command-line-based assistant for importing pkgs, disk images and apps into your Munki repo. It creates a pkginfo file for the installer item, wraps the pkg or app into a disk image if needed, and uploads the disk image or flat package to the repo, optionally under a subdirectory of your choosing. If the pkg/dmg upload is successful, `munkiimport` then uploads the pkginfo and opens it in your preferred editor.

### Details

Basic usage:

Run `munkiimport --configure` to tell the utility about your repo and preferred editor:

```bash
munkiimport --configure
Repo URL (example: afp://munki.pretendco.com/repo): [This is normally a afp: or smb: URL for a repo on a remote server, or a file: URL for a local file path]
pkginfo extension (Example: .plist):
pkginfo editor (examples: /usr/bin/vi or TextMate.app):
```
Now import a pkg, or disk image:

```bash
$ munkiimport /Users/n8felton/Downloads/googlechrome.dmg
           Item name: Chrome
        Display name: Google Chrome
         Description: Google Chrome is a fast, free web browser.
             Version: 70.0.3538.67
            Category: Productivity
           Developer: Google
  Unattended install: True
Unattended uninstall: True
            Catalogs: production

Import this item? [y/n] y
Upload item to subdirectory path []: apps/Google
Path pkgsinfo/apps/Google doesnt exist. Create it? [y/n] y
No existing product icon found.
Attempt to create a product icon? [y/n] y
Attempting to extract and upload icon...
Imported icons/Chrome.png.
Copying googlechrome.dmg to repo...
Copied googlechrome.dmg to pkgs/apps/Google/googlechrome-70.0.3538.67.dmg.
Edit pkginfo before upload? [y/n]: n
Saved pkginfo to pkgsinfo/apps/Google/Chrome-70.0.3538.67.plist.
Rebuild catalogs? [y/n] y
Rebuilding catalogs at file:///Users/Shared/munki_repo...
Created icons/_icon_hashes.plist...
```

Most of the time you'll answer 'y' to rebuild the catalogs after you've made changes. You might answer 'n' if you are going to be importing more items and want to wait until all new items are imported before rebuilding the catalogs.

### Version numbers in filenames

`munkiimport` will append the provided version number to the end of the filename for the imported package and the generated pkginfo. You will notice that `googlechrome.dmg` is imported as `googlechrome-70.0.3538.67.dmg`.

```bash
munkiimport /Users/n8felton/Downloads/googlechrome.dmg
[...]
Copied googlechrome.dmg to pkgs/apps/Google/googlechrome-70.0.3538.67.dmg.
[...]
Saved pkginfo to pkgsinfo/apps/Google/Chrome-70.0.3538.67.plist.
```

If there is a naming conflict, the package can be imported again, however, `__n` will be further appended to the filename.

```bash
munkiimport /Users/n8felton/Downloads/googlechrome.dmg
[...]
Copied googlechrome.dmg to pkgs/apps/Google/googlechrome__1.dmg.
[...]
Saved pkginfo to pkgsinfo/apps/Google/Chrome-70.0.3538.67__1.plist.
```

#### Packages with version number in filename

Some packages will download with their version number already in the filename. If the version number matches the value entered to `munkiimport`, the filename will essentially be imported unchanged.

```bash
munkiimport /Users/n8felton/Downloads/Skype-8.33.0.41.dmg
[...]
Version: 8.33.0.41
[...]
Copied Skype-8.33.0.41.dmg to pkgs/apps/Skype/Skype-8.33.0.41.dmg.
```

However, if the version numbers are not identical, `munkiimport` will still append the version number provided, regardless if version information is already in the filename.

```bash
munkiimport /Users/n8felton/Downloads/Skype-8.33.0.41.dmg
[...]
Version: 8.33
[...]
Copied Skype-8.33.0.41.dmg to pkgs/apps/Skype/Skype-8.33.0.41-8.33.dmg.
```

Notice that because `8.33` was provided to `munkiimport`, the filename becomes `Skype-8.33.0.41-8.33.dmg` with `8.33` appended.

### Importing with Drag-n-Drop Options
By default, if you run `munkiimport` on a .dmg that contains a single .app bundle that should be dragged and dropped to the /Applications folder or a single .pkg that should be installed, `munkiimport` will create a pkginfo for, respectively, copying the .app to the /Applications folder and creating an appropriate installs array for the bundle, or installing the .pkg.

But there may be other special cases, which you can address with some additional command options.

#### Import a .dmg that has a folder inside
If, instead of a single .app bundle or a single .pkg, you have a .dmg with a single folder you want copied to the /Applications folder (or even another folder), you can add the `--itemname` and `--destinationpath` options.

```
munkiimport --itemname ArKaos\ GrandVJ\ 2.6.2 --destinationpath /Applications Downloads/ArKaos_GrandVJ_2_6_2.dmg
```

### Importing without Interactive Prompts
`munkiimport` by default prompts you with options to fill in our questions to answer.

Sometimes, you may just want to do a `munkiimport` without any prompting, because you know the options you want ahead of time (or you want to automate `munkiimport` in a script).

Here's an example of how you could do that:
```
munkiimport MAContent10_AssetPack_0025_AlchemyDrumsBeatBoxVelocity-2.0.0.0.1.1452033143.pkg --nointeractive --unattended_install --category=Multimedia --developer=Apple
```
Since it's non interactive, you won't get a prompt to run `makecatalogs` at the end, so you'll want to run it manually afterwards (or include it at the end of your script, if you're using `--nointeractive` in a script).
```
makecatalogs
```

### Additional notes

#### pkginfo Editor
By default the pkginfo file is opened with the defined pkginfo editor. If you wish to avoid this you can set the pkginfo editor to an empty string (or delete the preference from com.googlecode.munki.munkiimport). If this preference is empty or undefined the pkginfo is not opened in an editor.

#### Preferences
Preferences set by `--configure` are stored in the OS X preferences domain "com.googlecode.munki.munkiimport", which is has file storage for the current user account in `~/Library/Preferences/com.googlecode.munki.munkiimport.plist`

#### Example Repo URLs:

| URL Scheme | Example |
|---|---|
| SMB | smb://server.domain.org/ShareNamePath/Share |
| AFP | afp://server.domain.org/ShareNamePath/Share |
| File (Local Repo)  | file:///Library/Server/Web/Data/Sites/Default/munki_repo  |

#### Other Options
Apart from the ones mentioned in this page, there are other options for `munkiimport` that you might find helpful. You can find those by running
```
munkiimport --help
```