## Why Repo Plugins?

Munki [repo plugins](https://github.com/munki/munki/wiki/Repo-Plugins) allow Munki to interact with a variety of different Munki repository types. For instance, There is a `FileRepo` plugin, which is used in most instances and allows Munki to work with a local (or locally mounted) file-folder repository. There are other plugins, such as `GitFileRepo` that allow Munki to interact with a Git-based Munki repo. Others exist as well, included with the Munki project and also available on a [third-party "community plugin" basis](https://github.com/munki/munki/wiki/Repo-Plugins#community-plugins). Munki administrators may configure the Munki admin tools to use any one of these plugins, depending upon their needs.

Some AutoPkg recipes utilize the `MunkiImporter` processor step, instructing AutoPkg to deliver recipe output to a Munki repository. By default, `MunkiImporter` expects this to be a `FileRepo` type repository, however `MunkiImporter` may be customized to use other repository types, too.  

## Requirements

- If using a plugin other than `FileRepo`, Munki (and its libraries) must be installed on the machine local to AutoPkg for `MunkiImporter` to function.

## Usage

Below is an example of specifying a plugin for usage. In this example, we're using the `MWA2APIRepo` plugin and we're setting the `MUNKI_REPO` value per the directions of the plugin. The plugin also requires authentication information (for the MWA web api, in this case) so we're providing that in advance so that AutoPkg can run without user interaction.

```
MUNKIREPO_AUTHTOKEN="Basic XXXXXXXYYYYYYYZZZZZZZZ=="
export MUNKIREPO_AUTHTOKEN

autopkg run -v GoogleChrome.munki -k MUNKI_REPO="https://example.org/api" \
                                  -k MUNKI_REPO_PLUGIN="MWA2APIRepo"
```

## Under The Hood

### Two Different Libraries

`MunkiImporter` uses one of two different libraries when interacting with a Munki repository:

1. **autopkglib**: By default, when the repo type is `FileRepo`, `MunkiImporter` will utilize the (this) built-in library. While this library only supports `FileRepo` repositories, it has the benefit of being available in all AutoPkg installs.
2. **munkilibadapter**: This library is used whenever the repo plugin is not `FileRepo`, or when `force_munki_lib=True` is specified. 

Worth noting is that the logic in these two libraries (when looking for existing pkgs/dmgs, for instance) does vary and should be tested if you plan on switching your workflow from using one library to the other (likely `autopkglib` to `munkilibadapter`).

### Icon Extraction

AutoPkg supports extracting and uploading pkg/dmg icons. This functionality is _only_ available with the `munkilibadapter` library. 

When `MunkiImporter` gets to the icon extraction stage, it will check to see which library is in use. If `munkilibadapter` is being used, it will continue. If `autopkglib` is in use, it will create a separate instance of `munkilibadapter` for use only with the icon aspect of work.
