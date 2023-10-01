## Munki 3

### Munki 3 new features:

* "Native" support for macOS installation applications (Like "Install macOS Sierra.app"). See [[macOS Installer Application support]].

* Support for authorized restarts. 
  This requires some launchd changes that will require a restart when upgrading from Munki 2.x to 3.x. See [[Authorized Restarts]].

* Notification Manager notification support.
  This requires some launchd changes that will require a restart when upgrading from Munki 2.x to 3.x.  
  See [[Notification Center Support]].

* Repo plugin support contributed by Centrify.
  Allows the creation of plugins to enable the Munki command-line tools to work with cloud-based repos, or repos not available via traditional file paths, or to add additional capabilities/actions when working with a file-based repo.
There are a couple of sample/demonstration plugins included: a GitFileRepo plugin for better integration with Git repos, and a MWA2APIPlugin as an example of working with a repo that doesn't have direct filesystem access.  
See [[Repo Plugins]].

* Auto-removal of optionally-installed applications that have not been used in an admin-specified time period.  
  See [[Removal of Unused Software]].

* Support for a new "Featured" psuedo-category to be used with Managed Software Center. Items can be added to a list of "featured\_items" in a manifest. If there are optional installs that are also in the list of "featured\_items", the display of All optional installs in MSC app will be replaced by a display of Featured items.  
  See [Featured Items](Featured-Items-in-Managed-Software-Center).

* Support for allowing the install of packages signed with untrusted or expired certificates.  
  See [[Allowing Untrusted Packages]].

* A major refactoring of the code base, which should make it easier to add additional features in the future, but also risks introducing some regressions.

### Removed in Munki 3:

* Support for macOS 10.6 and 10.7.

### Removed in Munki 3.6 (released March 2019):

* Support for macOS 10.8 and 10.9.

## More information:
* [[macOS Installer Application support]]
* [[Authorized Restarts]]
* [[Notification Center Support]]
* [[Repo Plugins]]
* [[Removal of Unused Software]]
* [[Allowing Untrusted Packages]]
