_Troubleshooting tips_

### Introduction

Where to start troubleshooting when things aren't working as you expect.

See also the [[FAQ]], and especially the section on [[troubleshooting|FAQ#troubleshooting]].


### Details

#### Command line

Run `/usr/local/munki/managedsoftwareupdate -vvv` to get more verbose output.

#### Logs

By default, logs are written to `/Library/Managed Installs/Logs/`

ManagedSoftwareUpdate.log is the main log; errors and warnings from the most recent run are in errors.log and warnings.log, respectively. 

You can increase the amount of detail in ManagedSoftwareUpdate.log with `sudo defaults write /Library/Preferences/ManagedInstalls LoggingLevel -int 2` (higher integers for even more detail).

The Managed Software Center application runs as the user, and uses a different path, described here:
https://github.com/munki/munki/wiki/MSC-Logging


When installing Apple Installer packages, Munki calls the command-line `/usr/sbin/installer` tool. That tool logs to /var/log/install.log.

Munki can be configured to check for and install Apple software updates; in that case it calls `/usr/sbin/softwareupdate`. Apple's `softwareupdate` tool also logs to /var/log/install.log.

#### Server troubleshooting

The Munki client talks to the Munki server via normal web protocols -- you may be able to troubleshoot by using a web browser to download the same info from the relevant URLs:

```
http://(yourmunkiserver)/repo/manifests/name_of_client_manifest

http://(yourmunkiserver)/repo/catalogs/production

http://(yourmunkiserver)/repo/catalogs/testing
```

#### Still stuck?
Ask for help here: http://groups.google.com/group/munki-discuss