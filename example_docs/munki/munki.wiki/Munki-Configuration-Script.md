_An example script to configure Munki_

### Overview

Below you will find a script to configure Munki. While this script can be used in a "thin imaging" environment, pay attention to the context in which the script is running or it will fail.

```
#!/bin/bash
 
# Munki Configuration Script
# Last Date Modified:
# November 25th, 2014
# Uncomment what you need.
 
##################################################   Munki 1/2   ##################################################
 
# AppleSoftwareUpdatesOnly
## boolean
## default = false
### If true, only install updates from an Apple Software Update server.
### No munki repository is needed or used.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls AppleSoftwareUpdatesOnly -bool false
 
# InstallAppleSoftwareUpdates
## boolean
## default - false
### If true, install updates from an Apple Software Update server, in addition to "regular" munki updates.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls InstallAppleSoftwareUpdates -bool false
 
# SoftwareUpdateServerURL - WARNING! NOT RECOMMENDED
## string
## default - NONE
### Catalog URL for Apple Software Updates.
### If undefined or empty, Munki will use the same catalog that the OS uses when you run Apple's Software Update application or call /usr/sbin/softwareupdate. THIS IS NOT RECOMMENDED as of 10.11+, see https://github.com/munki/munki/issues/511
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls SoftwareUpdateServerURL -string "http(s)://FDDQN"
 
# SoftwareRepoURL
## string
## default - "http://munki/repo"
### Base URL for munki repository
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls SoftwareRepoURL -string "http://munki/repo"
 
# PackageURL
## string
## default - "<SoftwareRepoURL>/pkgs"
### Base URL for munki pkgs.
### Useful if your packages are served from a different server than your catalogs or manifests.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls PackageURL -string "http(s)://FDDQN/pkgs"
 
# CatalogURL
## string
## default - "<SoftwareRepoURL>/catalogs"
### Base URL for munki catalogs.
### Useful if your catalogs are served from a different server than your packages or manifests.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls CatalogURL -string "http(s)://FDDQN/catalogs"
 
# ManifestURL
## string
## default - "<SoftwareRepoURL>/manifests"
### Base URL for munki manifests.
### Useful if your manifests are served from a different server than your catalogs or manifests.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls ManifestURL -string "http(s)://FDDQN/manifests"
 
# ClientIdentifier
## string
## default - NONE
### Identifier for munki client.
### Usually is the same as a manifest name on the munki server.
### If this is empty or undefined, Munki will attempt the following identifiers, in order: fully-qualified hostname, "short" hostname, serial number and finally, "site_default"
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls ClientIdentifier -string "MachineName"
 
# ManagedInstallDir
## string
## default - "/Library/Managed Installs"
### Folder where munki keeps its data on the client.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls ManagedInstallDir -string "/Library/Managed Installs"
 
# LogFile
## string
## default - "/Library/Managed Installs/Logs/ManagedSoftwareUpdate.log"
### Primary log is written to this file.
### Other logs are written into the same directory as this file.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls LogFile -string "/Library/Managed Installs/Logs/ManagedSoftwareUpdate.log"
 
# LogToSyslog
## boolean
## default - false
### If true, log to /var/log/system.log in addition to ManagedSoftwareUpdate.log.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls LogToSyslog -bool false
 
# LoggingLevel
## integer
## default - 1
### Higher values cause more detail to be written to the primary log.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls LoggingLevel -int 1
 
# DaysBetweenNotifications
## integer
## default - 1
### Number of days between user notifications from Managed Software Update.
### Set to 0 to have Managed Software Update notify every time a background check runs if there are available updates.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls DaysBetweenNotifications -int 1
 
# UseClientCertificate
## boolean
## default - false
### If true, use an SSL client certificate when communicating with the munki server.
### Requires an https:// URL for the munki repo.
### See ClientCertificatePath for details.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls UseClientCertificate -bool false
 
# UseClientCertificateCNAsClientIdentifier
## boolean
## default - false
### If true, use the CN of the client certificate as the Client Identifier.
### Used in combination with the UseClientCertificate key.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls UseClientCertificateCNAsClientIdentifier -bool false
 
# SoftwareRepoCAPath
## string
## default - (empty)
### Path to the directory that stores your CA certificate(s).
### See the curl man page for more details on this parameter.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls SoftwareRepoCAPath -string "http(s)://FQDN"
 
# SoftwareRepoCACertificate
## string
## default - "/Library/Managed Installs/certs/ca.pem"
### Absolute path to your CA Certificate.
####  /usr/bin/defaults write /Library/Preferences/ManagedInstalls SoftwareRepoCACertificate -string "/Library/Managed Installs/certs/ca.pem"
 
# ClientCertificatePath
## string
## default - "/Library/Managed Installs/certs/[munki.pem|client.pem|cert.pem]"
### Absolute path to a client certificate.
### There are 3 defaults for this key. Concatenated cert/key PEM file accepted.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls ClientCertificatePath -string "/Library/Managed Installs/certs/[munki.pem|client.pem|cert.pem]"
 
# ClientKeyPath
## string
## default - (empty)
### Absolute path to a client private key.
### /usr/bin/defaults write /Library/Preferences/ManagedInstalls ClientKeyPath -string "/Library/Managed Installs/certs/private/munki.key"
 
# AdditionalHttpHeaders
## array
## default - (empty)
### This key provides the ability to specify custom HTTP headers to be sent with all curl() HTTP requests.
### AdditionalHttpHeaders must be an array of strings with valid HTTP header format.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls AdditionalHttpHeaders -array-add '{"http";}'
 
# PackageVerificationMode
## string
## default - "hash"
### Controls how munki verifies the integrity of downloaded packages.
### Possible values are:
###     none: No integrity check is performed.
###     hash: Integrity check is performed if package info contains checksum information.
###     hash_strict: Integrity check is performed, and fails if package info does not contain checksum information.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls PackageVerificationMode -string "hash"
 
# SuppressUserNotification
## boolean
## default - false
### If true, Managed Software Update will never notify the user of available updates.
### Managed Software Update can still be manually invoked to discover and install updates.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls SuppressUserNotification -bool false
 
# SuppressAutoInstall
## boolean
## default - false
### If true, munki will not automatically install or remove items.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls SuppressAutoInstall -bool false
 
# SuppressLoginwindowInstall
## boolean
## default - false
### Added in version 0.8.4.1696.0.
### If true, Munki will not install items while idle at the loginwindow except for those marked for unattended_install or unattended_uninstall.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls SuppressLoginwindowInstall -bool false
 
# SuppressStopButtonOnInstall
## boolean
## default - false
### If true, Managed Software Update will hide the stop button while installing or removing software, preventing users from interrupting the install.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls SuppressStopButtonOnInstall -bool false
 
# InstallRequiresLogout
## boolean
## default - false
### If true, Managed Software Update will require a logout for all installs or removals.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls InstallRequiresLogout -bool false
 
# ShowRemovalDetail
## boolean
## default - false
### If true, Managed Software Update will display detail for scheduled removals.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls ShowRemovalDetail -bool false
 
 
################################################## Munki 2 Only ##################################################
 
# IconURL
## string
## default - "<SoftwareRepoURL>/icons"
### Base URL for product icons.
### Useful if your icons are served from a different server or different directory than the default.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls IconURL -string "http(s)://FDDQN/icons"
 
# ClientResourceURL
## string
## default - "<SoftwareRepoURL>/client_resources"
### Base URL for custom client resources for Managed Software Update.
### Useful if your resources are served from a different server or different directory than the default.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls ClientResourceURL -string "http(s)://FDDQN/client_resources"
 
# ClientResourcesFilename
## string
## default - "manifest name.zip or site_default.zip"
### Specific filename to use when requesting custom client resources.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls ClientResourcesFilename -string "site_default.zip"
 
# HelpURL
## string
## default - "none"
### If defined, a URL to open/display when the user selects "Managed Software Center Help" from Managed Software Center's Help menu.
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls HelpURL -string "http(s)://FQDN"

# LocalOnlyManifest
## string
## default - "none"
### Specific manifest placed in /Library/Managed\ Installs/manifests/
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls LocalOnlyManifest -string "extra_packages"

# FollowHTTPRedirects
## string
## default - "none"
### Allows Munki to follow HTTP/S redirects
### none - This is the default and is the same as the present behaviour. No redirects are followed. https - Only redirects to URLs using HTTPS are followed. Redirects to HTTP URLs are not followed. all - Redirects to both HTTP and HTTPS URLs are followed
#### /usr/bin/defaults write /Library/Preferences/ManagedInstalls FollowHTTPRedirects -string "none"

```