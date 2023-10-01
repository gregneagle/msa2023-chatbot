_Admin tool plug-in support for different types of Munki repos_

### Introduction
Munki 3 supports repo plugins: adapters that allow the Munki command-line admin tools to work with repos that aren't local file-based repos, or to add extra capabilities to the tools.

### Repo plugins
repo plugins are written in Python and installed to the munkilib/munkirepo directory. Currently Munki ships with these repo plugins:

* **FileRepo** - the default plugin and handles both local file repos and repos hosted on fileshares.

* **GitFileRepo** - a proof-of-concept/demonstration plugin. It inherits the behavior of FileRepo and does git commits for file changes in the repo (which must be already configured/initialized as a git repo)

* **MWA2APIRepo** - a proof-of-concept/demonstration plugin that talks to a remote repo via the [MWA2 API](https://github.com/munki/mwa2/wiki/API-notes). It requires the [latest MWA2 code from GitHub](https://github.com/munki/mwa2).

Additional repo plugins are welcome, however, we currently wish to have those maintained outside of the core Munki code. If you have created a plugin and would like to make it more visible please add it to the following section, [Community Plugins](#community-plugins).

### Command-line tools
These command-line admin tools have been updated to use the new-style repo plugins:

`iconimporter`  
`makecatalogs`  
`manifestutil`  
`munkiimport`  
`repoclean`

Available options for these tools may have changed; use `<toolname> --help` to see the usage.

When using the `--configure` option with `manifestutil` and `munkiimport`, there are three major changes to be aware of:

- You will no longer be prompted for a repo path. The repo_path preference may be deprecated in the future -- I'm not sure it's needed any longer.

- Repo URL can take several forms:
   - a file: url: file:///Users/Shared/munki\_repo will cause these tools to use a local file-based repo located at /Users/Shared/munki_repo
   - a filesharing url: afp://someserver/sharename or smb://someserver/sharename or nfs://someserver/sharename These tools will attempt to mount these URLs and use whatever mountpoint they mount at (typically under /Volumes)
   - An http/https url: Example: `https://mwa2.my.org/api` These sorts of repos require a custom plugin that knows how to talk to the repo at the given URL.

- You will be prompted for a plugin name. For traditional file-based repos (either local or those available via fileshare, the default FileRepo plugin can be used. If plugin is not defined, the FileRepo plugin will be used.)

### Workflow changes
The most noticable change to workflows using the modified tools is around editing pkginfo items in a text editor when using munkiimport.

Since we can't guarantee direct file access to the pkginfo item after it's been uploaded to the Munki repo, we ask _before_ we upload it if you want to edit it.

If you answer 'yes', the pkginfo is opened in your editor of choice. 
- If the editor is command-line based (like vi), once you exit the editor, the munkiimport session will resume and the pkginfo file will be uploded to the repo.
- If the editor is an application (like SublimeText), munkiimport will wait for you to manually indicate you are done editing the file before proceeding.
- The pkginfo is saved to a temp file before it is opened in the text editor, so don't be concerned about the strange path you might see.

### Other notes
`makecatalogs` works with the MWA2APIRepo but is very slow due to all the web calls need to get every icon and pkginfo item. A future version of the code may allow a plugin to tell the repo to makecatalogs itself: so for the MWA2API, it would trigger the MWA2 code to do the catalog rebuild.

`iconimporter` has to download dmgs and pkgs from the repo in order to process them for possible icons. This is slower and uses more disk than the direct file access possible when only file-based repos were supported. Running `iconimporter` against an entire repo should be an infrequent operation, so it's not likely this is worth optimizing in any way.

### Plugin developer notes
The "API" of the new-style repo plugins is greatly simplified over the previous style of repo plugins. It's possible I've over-simplfied it and it might need extension to cover things I haven't thought of. See the munkilib/munkirepo/FileRepo.py, munkilib/munkirepo/GitFileRepo.py and munkilib/munkirepo/MWA2APIRepo.py files for concrete examples of the new-style repo plugins.

Repo subclasses need to implement these methods:

```python

    def __init__(self, baseurl):
        '''Constructor, does initial setup and handles login/mounting'''

    def itemlist(self, kind):
        '''Returns a list of identifiers for each item of kind.
        Kind might be 'catalogs', 'manifests', 'pkgsinfo', 'pkgs', or 'icons'.
        For a file-backed repo this would be a list of pathnames.'''

    def get(self, resource_identifier):
        '''Returns the content of item with given resource_identifier.
        For a file-backed repo, a resource_identifier of
        'pkgsinfo/apps/Firefox-52.0.plist' would return the contents of
        <repo_root>/pkgsinfo/apps/Firefox-52.0.plist.
        Avoid using this method with the 'pkgs' kind as it might return a
        really large blob of data.'''

    def get_to_local_file(self, resource_identifier, local_file_path):
        '''Gets the contents of item with given resource_identifier and saves
        it to local_file_path.
        For a file-backed repo, a resource_identifier
        of 'pkgsinfo/apps/Firefox-52.0.plist' would copy the contents of
        <repo_root>/pkgsinfo/apps/Firefox-52.0.plist to a local file given by
        local_file_path.'''

    def put(self, resource_identifier, content):
        '''Stores content on the repo based on resource_identifier.
        For a file-backed repo, a resource_identifier of
        'pkgsinfo/apps/Firefox-52.0.plist' would result in the content being
        saved to <repo_root>/pkgsinfo/apps/Firefox-52.0.plist.'''

    def put_from_local_file(self, resource_identifier, local_file_path):
        '''Copies the content of local_file_path to the repo based on
        resource_identifier. For a file-backed repo, a resource_identifier
        of 'pkgsinfo/apps/Firefox-52.0.plist' would result in the content
        being saved to <repo_root>/pkgsinfo/apps/Firefox-52.0.plist.'''

    def delete(self, resource_identifier):
        '''Deletes a repo object located by resource_identifier.
        For a file-backed repo, a resource_identifier of
        'pkgsinfo/apps/Firefox-52.0.plist' would result in the deletion of
        <repo_root>/pkgsinfo/apps/Firefox-52.0.plist.'''
```

### Interaction examples
```
bash-3.2$ ./munkiimport --configure
Repo URL (example: afp://munki.example.com/repo): http://localhost:8080/api
pkginfo extension (Example: .plist): .plist
pkginfo editor (examples: /usr/bin/vi or TextMate.app; leave empty to not open an editor after import): /usr/bin/vi
Default catalog to use (example: testing): testing
Repo access plugin (defaults to FileRepo): MWA2APIRepo
```

```
bash-3.2$ ./munkiimport ~/Downloads/AutoDMG-1.7.3.dmg 
Please provide credentials for http://localhost:8080/api:
Username: gneagle
Password: 
This item is similar to an existing item in the repo:
            Item name: AutoDMG
         Display name: AutoDMG
          Description: Create deployable system images from OS X installer.
              Version: 1.7
  Installer item path: apps/AutoDMG-1.7__1.dmg

Use existing item as a template? [y/n] y
Copying unattended_install: True
Copying unattended_uninstall: False
Copying category: Admin Tools
Copying developer: Per Olofsson
Copying featured: False
           Item name: AutoDMG
        Display name: AutoDMG
         Description: Create deployable system images from OS X installer.
             Version: 1.7.3
            Category: Admin Tools
           Developer: Per Olofsson
            Featured: False
  Unattended install: True
Unattended uninstall: False
            Catalogs: testing

Import this item? [y/n] y
No existing product icon found.
Attempt to create a product icon? [y/n] y
Attempting to extract and upload icon...
Created icon: icons/AutoDMG.png
Copying AutoDMG-1.7.3.dmg to pkgs/apps/AutoDMG-1.7.3.dmg...
Edit pkginfo before upload? [y/n]: n
Saving pkginfo to pkgsinfo/apps/AutoDMG-1.7.3.plist...
Rebuild catalogs? [y/n] y
Rebuilding catalogs at http://localhost:8080/api...
```

```
bash-3.2$ ./manifestutil --configure
Repo URL (example: afp://munki.example.com/repo): file:///Users/Shared/munki_repo
Munki repo plugin (defaults to FileRepo): GitFileRepo
bash-3.2$ ./manifestutil 
Entering interactive mode... (type "help" for commands)
> display-manifest site_default
 catalogs:
     testing
     production
 included_manifests:
     groups/StandardApps
     groups/AllOptionalInstalls
 managed_installs:
     Firefox
 managed_uninstalls:
 managed_updates:
 optional_installs:
     GoogleChrome
     AdobeReaderDC
> add-pkg AutoDMG --manifest site_default --section optional_installs
Doing git commit: gneagle modified 'manifests/site_default' via manifestutil
Added AutoDMG to section optional_installs of manifest site_default.
> new-manifest yet_another_manifest
Doing git commit: gneagle created 'manifests/yet_another_manifest' via manifestutil
> exit
```

### Community Plugins
These are Munki repo plugins developed by third parties and are not part of Munki core. (which is one of the _points_ of supporting repo plugins!)  
If you experience issues with a plugin please make sure to send that issue to the correct repo. 

| Name | URL | Description |
| ---- | --- | ----------- |
| s3Repo | https://github.com/clburlison/Munki-s3Repo-Plugin | This plugin allows administrators to interact with their Munki repo hosted in a S3 compatible bucket. |
| SimpleMDMRepo | https://github.com/SimpleMDM/munki-plugin | Upload pkgs, pkginfos, and icons to a SimpleMDM account. |