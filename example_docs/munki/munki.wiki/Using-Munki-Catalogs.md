_Using catalogs to implement development/testing/production stages_

### Munki Catalog Concepts

Munki catalogs are the main mechanism by which a macOS systems administrator can deploy certain software installations and updates to one group of users, while denying those same installs and updates to another group.

Additionally, Munki catalogs allow for filtering which versions of installer items are "visible" to a specific groups of Macintosh machines.  The main intention behind catalogs is to provide a method for implementing a development, testing, and production software package deployment workflow.

This multiple catalog model allows the sysadmin to test updates with a small group of
test machines before making software updates available to all production macOS client machines in the computing environment. As the macOS systems administrator makes changes to the development and testing catalogs and then finally pushes them out to the production catalog, minimal changes are made to the macOS client manifests.

Munki catalogs are searched in the same order as they are specified in the client
manifest; if a software item is available in more than one catalog, the version in the earliest listed catalog will be used. Please be aware that development and testing catalog key entries should be placed before the production entry. As such, the earlier catalog entries will take precedence over the later entries in the manifest. Also, if there are no catalog entries in a particular client munki manifest, then the catalog listed in the parent manifest will be used.

As a caveat, munki catalogs are not recommended for making arbitrary or logical software groupings like "AdobeApps" or "Utilities", but rather for unstable/stable or development/test/production staging, or similar deployment workflow purposes. 

### Catalog naming

You may name catalogs anything you like, with a single exception: the catalog name "all" is reserved for use internally by Munki. You should not create a catalog named "all". You should also not point any client to the "all" catalog.

Catalog names take on the case-sensitivity of the underlying filesystem on which they are stored. This can have unexpected consequences. In general, it is best to avoid catalog names that differ only by case.

On a case-insensitive filesystem (like HFS+ or APFS, the default filesystems on macOS, or NTFS, the most commonly used filesystem on Windows), you will have undesired behavior if you have catalog names that differ by case. A catalog named "testing" and one named "Testing" cannot exist at the same time in the same directory of a case-insensitive filesystem. Depending on the Munki version, this can result in one catalog overwriting the other, or may cause `makecatalogs` to display a warning message.

### Practical Munki catalog examples

Currently, munki catalogs are created by the macOS systems administrator with a command line tool (written as a Python script) named "makecatalogs" (usually installed
in /usr/local/munki/makecatalogs). This tool can be run directly on the munki web server (if it is running macOS) or on any machine that has mounted the munki repo storage as a file share. makecatalogs recursively walks the munki repo/pkgsinfo directory and then builds a XML catalog file based on the pkginfo files it finds, complete with relative paths to the appropriate installer items.

Munki manifests usually have one or more catalog key entries such as "testing" or "production" which point the client manifest to munki catalogs to search for installation packages. This allows you to have a munki manifest named "A-mac" that searches both the "testing" and "production" catalogs, and another munki manifest named "B-mac" that searches only the "production" catalog.  

In this scenario, a new version of a software package is added to the "testing" catalog first. macOS client machines with "testing" catalog entries in their manifests can see and download the new package immediately and can install it via the "Managed Software Updates" interface. Client machines with manifest "B-mac" won't see the new package until it is added to the "production" catalog.

The underlying idea here is that most of the macOS client machines in a given computing environment are configured to use the production catalog only. Here is a simplified example of a production client machine manifest:

```xml
<key>catalogs</key>
<array>
    <string>production</string>
</array>
```

In another example, a group of test machines are configured to also search the testing catalog:

```xml
<key>catalogs</key>
<array>
    <string>testing</string>
    <string>production</string>
</array>
```

Finally, a much smaller group (maybe just a single systems administrator) may have a development catalog entry in their manifest as well. Take special note of the order of the catalog key entries, as this is important. Earlier catalog entries will take priority over later entries. Be careful not to reverse the order of these catalog entries or there will be unexpected results such as development and testing Mac client machines not installing the newest versions of software available.

```xml
<key>catalogs</key>
<array>
    <string>development</string>
    <string>testing</string>
    <string>production</string>
</array>
```

Continuing on with this example, let's say the "in production", supported version of Firefox is 3.6.3. This version is in the production catalog, so all client machines that have an entry in their manifest like this:

```xml
<key>managed_installs</key>
<array>
    <string>Firefox</string>
</array>
```

and are looking only at the production catalog will get Firefox 3.6.3. Mozilla then releases Firefox 3.7.  The macOS systems administrator doesn't want every production client machine to get the new version right away; the update should first go to a subset of test machines and users. So the sysadmin makes a pkginfo file and assigns it only to the testing catalog, and then runs the "makecatalogs" script to update the catalog.

The client machines that have "Firefox" in the managed_installs section of their manifests and have "testing" in their catalogs entry can now "see" Firefox 3.7, so  
they automatically download and have this new version available for install.  The 
vast majority of client machines, though, don't have "testing" in their list of catalog entries. As a result, these production client machines do not see the listing for Firefox 3.7 and stay with Firefox 3.6.3.

Later, the sysadmin decides Firefox 3.7 is stable and solid in the computing environment
and wants to install it on all production client computers. So then the sysadmin edits the pkginfo file for Firefox 3.7, changes its catalog assignment to "production", and rebuilds the catalogs.

Now all production client machines in your organization can "see" Firefox 3.7 and automatically download it. Additionally, all of the machines that didn't install it while it was in testing can install it now via the "Managed Software Updates" interface.

### Catalogs and included_manifests

Munki manifests can contain other manifests. These are listed under "included_manifests" in a given manifest. If an included manifest contains a list of catalogs, these are the only catalogs that will be used for managed_installs/managed_updates/managed_uninstalls items within that manifest.

This is often *not* what is wanted, especially when included manifests are used to group commonly used software packages. Often what is wanted is for Munki to use the catalogs defined in the "primary" manifest; that is, the main manifest used by the machine running Munki. In this case, your included manifest(s) would have **no** catalog list. If an included manifest has no catalog list, the catalog list of the parent manifest is used. This enables the Munki administrator to create groups of packages or application installs by defining them in an included manifest, while controlling the development/testing/production version for a given client in the client's primary manifest.

### Conclusion

In summary, using the multiple munki catalog model is an efficient way for the macOS
systems administrator to manage a complete enterprise wide systems and applications software deployment workflow. This method minimizes the need to manually edit client manifest files and allows for a large number of software packages to be tested and brought into production on client Mac machines in a short amount of time.