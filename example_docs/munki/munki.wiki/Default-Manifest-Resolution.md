### Introduction
While you can define ClientIdentifier in Munki's preferences to cause Munki to request a specific manifest from the Munki server, it can be more useful and powerful to leave ClientIdentifier undefined (or empty) and let Munki's default manifest resolution take over.

### Details

ClientIdentifier is undefined or empty, Munki asks for a manifest named after the fully-qualified hostname of the machine:

    http://webserver/repo/manifests/hostname.mycompany.com

If that fails, it tries the short hostname:

    http://webserver/repo/manifests/hostname

If that fails, it tries the machine serial number. If the serial number is "AABBCCDDEEFF"; the request looks like:

    http://webserver/repo/manifests/AABBCCDDEEFF

If that fails, it tries to retrieve a manifest named, literally, "site_default":

    http://webserver/repo/manifests/site_default

### Discussion
Relying on this mechanism frees you from having to manage ClientIdentifiers on each machine in your fleet.

If all machines share a single manifest, just create a site_default manifest and leave ClientIdentifier undefined.

If most machines share a single manifest, with a small number of "snowflakes" that are different, leave ClientIdentifier undefined and create a site_default manifest and then individual manifests for the snowflake machines, each named after the hostname or serial number.

If all your machines are different (or have the potential to be), leave ClientIdentifier undefined, and create manifests for each machine named after the hostname or serial number. Use of [included_manifests](Manifests#included_manifests) may greatly aid the management of a large number of machine manifests.

### See Also
[https://groob.io/posts/manifest-guide/](https://groob.io/posts/manifest-guide/)  
[https://technology.siprep.org/another-opinionated-guide-to-munki-manifests/](https://technology.siprep.org/another-opinionated-guide-to-munki-manifests/)