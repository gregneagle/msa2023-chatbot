_Support for authorized restarts of FileVault 2 volumes_

## Introduction

Munki 3 adds the ability to perform FileVault 2 Authorized Restarts. If the needed requirements are met Munki will attempt to perform an authrestart instead of a normal restart. This restarts the system, bypassing the initial unlock. This is especially useful for when doing full OS upgrades, as the actual OS install does not happen until after an initial reboot.

## Requirements 

### Munki

You'll need a version of Munki that supports this feature. The current release of Munki 3 is recommended.

New Munki [[Preferences]] controlling authorized restart behavior:

| Key | Type | Default | Description |
| --- | -------- | ------- | ----------- |
| PerformAuthRestarts | boolean | false | Set this to true to configure Munki to attempt authrestarts. Munki admins must opt into Authorized Restarts since there may be some security implications. |
| RecoveryKeyFile | string | | (Optional) The path of a plist file that contains the credentials used to perform an authrestart. e.g. `/var/root/restart.plist` This plist file should contain a key `RecoveryKey` with the value set to either a personal/individual recovery key or the password of an authorized user enabled in FileVault. An example of the file is below. |

#### Recovery Key File plist example

> NOTE: It appears High Sierra (or APFS volumes) have dropped support for using a Personal Recovery Key to authorize an Authorized Restart.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>RecoveryKey</key>
	<string>super-secret-password-or-recovery-key</string>
</dict>
</plist>
```

If a RecoveryKeyFile is not specified, or is specified and the file does not exist or is in the wrong format, Managed Software Center will prompt for a password if:
- Pending updates require a restart.
- A user is logged in to the GUI.
- The current GUI user is in the list of FileVault authorized users.

If Munki cannot obtain the required password or recovery key (either through the RecoveryKeyFile, or by prompting for a password), no auth restart will be attempted, and it will fall back to a normal restart.

### OS/Hardware Requirements

Not all versions of macOS and not all hardware types are capable of performing authrestarts. Munki uses `fdesetup` to check to make sure the machine meets the necessary criteria as well as for the restart.

##### `fdesetup isactive`

Munki will check to make sure FileVault is active (on). If FileVault isn't on you probably don't need to be performing an authorized restart. This is checked by running `/usr/bin/fdesetup isactive`
 
##### `fdesetup supportsauthrestart`

The authorized restart ability works on 10.8(+) and must also have supported hardware. This is checked by running `/usr/bin/fdesetup supportsauthrestart`.

## WARNING!

If you decide to use a RecoveryKeyFile, note that leaving a recovery key or password on disk may pose an additional security risk. The use of this feature is up to the discretion of the admin.

-----
#### Implementation notes for auth restarts with user-provided password

![](https://github.com/munki/munki/wiki/images/auth_restart_dialog.png)

Munki 3 adds a new `authrestartd` daemon. Managed Software Center.app uses UNIX/POSIX sockets to communicate with the daemon, which can run `fdesetup` commands as root, and allow Managed Software Center.app to tell if FileVault is on, if authrestart is supported, and if the current user is in the list of FileVault users. After asking for and getting a password from the user, Managed Software Center.app communicates again with the `authrestartd` daemon and sends it the password, which the daemon stores in memory. Soon after, Managed Software Center.app triggers a logout.

When the loginwindow loads, a launchd job causes `/usr/local/munki/managedsoftwareupdate` to run and install pending updates. After the install, if a restart is required, `managedsoftwareupdate` uses UNIX/POSIX sockets to communicate with `authrestartd` and asks `authrestartd` to perform the restart.

`authrestartd`, running as root, uses the password it has in memory to perform an authrestart if possible, falling back to a normal restart.

The user password is never written to disk, and is only stored in memory by `authrestartd`. `authrestartd` does not ever communicate the stored password to any process other than `fdesetup`.