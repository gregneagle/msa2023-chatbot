### Introduction
An unconfigured Munki client can autodetect a Munki repo if you make it available at a known URL.

### Details
If Munki's SoftwareRepoURL preference is not defined, the Munki client will attempt to detect a Munki repo.

Munki will get the DNS domain name of the current machine, and attempt to connect to the following URLs, in order:

#### Munki 3.3 and later:
```
https://munki.DOMAIN_NAME/repo  
https://munki.DOMAIN_NAME/munki_repo  
http://munki.DOMAIN_NAME/repo  
http://munki.DOMAIN_NAME/munki_repo  
http://munki/repo  
```

#### Versions of Munki prior to 3.3:
```
http://munki/repo  
```

Upon a successful connection (defined by successfully retrieving the contents of catalogs/all), the Munki client will record the detected Munki repo URL in /Library/Preferences/ManagedInstalls.plist under the SoftwareRepoURL key. This allows Munki to autodetect a Munki repo when it runs for the first time, but not be "hijacked" to a potentially hostile repo when connecting to another network later.

### Discussion
This capability is useful for bootstrapping a Munki client. Using this feature along with the [default manifest resolution](Default-Manifest-Resolution) when ClientIdentifier is not defined can allow you to install the Munki tools and make use of them without specific up-front configuration.


