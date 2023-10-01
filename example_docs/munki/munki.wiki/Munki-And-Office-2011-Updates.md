_Munki and Office 2011 updates_

### Introduction

Like Office 2008, Office 2011 must be updated by installing additional update packages, some of which require previous updates to be installed. See [[Munki And Office 2008]] to understand how to use update_for and requires to cause the correct updates to be installed in the correct order. The concepts are the same for Office 2011.

### Current Recommendation

Use [AutoPkg](https://autopkg.github.io/autopkg/).

The MSOffice2011Updates.munki recipe finds the latest Office 2011 update, downloads it, extracts the embedded package, and imports it into your Munki repo.

### Additional notes

#### Office 2011 14.1.2 and 14.1.3 Updates

Office 2011 updates typically work with little modification as downloaded from Microsoft.  Unfortunately, the Office 14.1.2 update brought a new issue where it will hang while trying to install at the login window. This same issue affects the Office 2011 14.1.3 update as well; the workaround is the same.

In order to prevent this problem, simply add the following installer_choice_xml entry to your Office 14.1.2 or 14.1.3 update pkginfo file:

```xml
<key>installer_choices_xml</key>
<array>
    <dict>
        <key>attributeSetting</key>
        <integer>0</integer>
        <key>choiceAttribute</key>
        <string>selected</string>
        <key>choiceIdentifier</key>
        <string>quit</string>
    </dict>
</array>
```

This installer_choices_xml section tells the installer to NOT install the "quit" subpackage in the update; this payload-free package attempts to quit open Microsoft applications before doing the update. It's written in a way that hangs when executed while at the login window. We work around the problem by telling the installer to skip the install of this specific subpackage.

You can learn more about Munki's support for installer choice changes XML here: [[ChoiceChangesXML]]

### Office 2011 14.1.4 Update

With prior Office 2011 updates, it was recommended to use an installer_choices_xml file to disable the installation of the package that quit open apps.

The corresponding package in the 14.1.4 update has a new preflight script:

```bash
#!/bin/bash

/usr/bin/w | /usr/bin/grep -e "console" | /usr/bin/grep -v grep > /dev/null
if [ $? == 1 ]
then
    exit 0
fi

RESOURCES_DIRECTORY=`/usr/bin/dirname "$0"`
QUIT_APPS_PATH="${RESOURCES_DIRECTORY}/QuitApps.app/Contents/MacOS/QuitApps"

if [ "${COMMAND_LINE_INSTALL}" == "" ]; then
    USERNAME=$USER
    MODE="GUI_INSTALLATION"
else
    USERNAME="root"
    MODE="COMMAND_LINE_INSTALLATION"
fi

/usr/bin/su "${USERNAME}" -c "\"${QUIT_APPS_PATH}\" $MODE"
```

Some brief testing shows that the modified QuitApps binary, when run as root with a COMMAND_LINE_INSTALLATION parameter, causes open web browsers and Office apps to be quit without warning. This makes the installation of the update more effective, but isn't great user experience if you are doing this while a GUI user is logged in.

Therefore, if you deploy this update with Munki, I'd recommend either marking it as requiring a logout, or adding a blocking_applications key with a list of all the applications that !QuitApps might quit.

"What are those apps?" you might ask. QuitApps.app/Contents/Resources/MSApplicationSignatures.plist seems to contain that list:

```xml
<string>Alerts Daemon</string>
<string>Database Utility</string>
<string>Equation Editor</string>
<string>Handheld Sync Installer</string>
<string>MSMLServer</string>
<string>MSN Messenger</string>
<string>MSN Messenger Daemon</string>
<string>Microsoft AU Daemon</string>
<string>Microsoft AutoUpdate</string>
<string>Microsoft Cert Manager</string>
<string>Microsoft Chart Converter</string>
<string>Microsoft Clip Gallery</string>
<string>Microsoft Database Daemon</string>
<string>Microsoft Database Utility</string>
<string>Microsoft Entourage</string>
<string>Microsoft Outlook</string>
<string>Microsoft Error Reporting</string>
<string>Microsoft Excel</string>
<string>Microsoft Graph</string>
<string>Microsoft Help Viewer</string>
<string>Microsoft Language Register</string>
<string>Microsoft Communicator</string>
<string>Microsoft Messenger Daemon</string>
<string>Microsoft Messenger</string>
<string>Microsoft Office Notifications</string>
<string>Microsoft Office Reminders</string>
<string>Microsoft Office Setup Assistant</string>
<string>Microsoft PowerPoint</string>
<string>Microsoft Sync Services</string>
<string>SyncServicesAgent</string>
<string>Microsoft Query</string>
<string>Microsoft Word</string>
<string>My Day</string>
<string>Organization Chart</string>
<string>Project Gallery Launcher</string>
<string>Remove Office</string>
<string>AssertMonitor</string>
<string>MacBU Monitor</string>
<string>Microsoft Ship Asserts</string>
<string>MicrosoftMouseHelper</string>
<string>MicrosoftKeyboardHelper</string>
<string>Windows Live Sync</string>
<string>Windows Live Mesh</string>
<string>LiveAgent</string>
<string>Expression Media</string>
<string>Remote Desktop Connection</string>
<string>eXClient</string>
<string>MacDiff</string>
<string>ImageDiff</string>
<string>Opera</string>
<string>Google Chrome</string>
<string>Firefox</string>
<string>Safari</string>
<string>Microsoft SkyDrive</string>
<string>Microsoft SkyDrive Setup</string>
```

It's a bad idea to put applications that have no UI into the blocking_applications list, since users have no way to quit them directly; besides, QuitApps will quit them if needed. So I'd suggest pruning this list to something like:

```xml
<string>MSN Messenger</string>
<string>Microsoft Cert Manager</string>
<string>Microsoft Chart Converter</string>
<string>Microsoft Clip Gallery</string>
<string>Microsoft Entourage</string>
<string>Microsoft Outlook</string>
<string>Microsoft Error Reporting</string>
<string>Microsoft Excel</string>
<string>Microsoft Graph</string>
<string>Microsoft Help Viewer</string>
<string>Microsoft Language Register</string>
<string>Microsoft Communicator</string>
<string>Microsoft Messenger</string>
<string>Microsoft PowerPoint</string>
<string>Microsoft Query</string>
<string>Microsoft Word</string>
<string>My Day</string>
<string>Organization Chart</string>
<string>Windows Live Sync</string>
<string>Windows Live Mesh</string>
<string>LiveAgent</string>
<string>Expression Media</string>
<string>Remote Desktop Connection</string>
<string>Opera</string>
<string>Google Chrome</string>
<string>Firefox</string>
<string>Safari</string>
```

### Office 2011 14.2.0 Update

This update, released in mid-April 2012, has deployment issues with JAMF Casper and Munki. In Munki's case, the installation hangs for a very long time at the end. Munki's supervisor module will eventually kill the process, but that only happens after two hours. This hang is due to a script that is launched at the beginning of the install process. This script waits until the installer exits, then does some temp file cleanup. Unfortunately, in many circumstances, the script fails to detect that the install is complete and hangs indefinitely.

Microsoft has acknowledged the issue, and currently suggests this workaround:

> Attempts to do a command line install on Lion are failing due to the script to clean up the temporary folder used to hold the bits during installation. This issue can also occur on any OS if multiple command line installs are being done at the same time.
>
> Microsoft is aware of the issue and looking to remedy it, but in the meantime, the following steps will allow you to edit the offending script and carry on with your deployment.
>
>1. Open the 14.2.0 updater DMG
>2.   Drag the Office 2011 14.2.0 Update.pkg to your desktop
>3.   CTRL+Click on the Office 2011 14.2.0 Update.pkg and choose Show Package Contents from the contextual menu
>4.   Navigate to the Resource folder from within the Contents folder.
>5.   Open the clean_path script with any text editor
>6.   On the second line (a blank line) add this text    exit 0
>7.   Save the script and then run your installation with this modified pkg
>
>Your final code should look like this:
>
>\#!/bin/sh
>
>exit 0
>
>We recommend that you restart after this installation to remove the temporary folder from the machine and
>avoid potential update problems in the future if the temporary folder still existed.
> 
>I am sorry for any inconvenience this has caused you.
> 
>David Pelton
>Release Test Lead, Microsoft Macintosh group.


Munki tools version **0.8.3 Build 1564** makes changes to how `/usr/sbin/installer` is called that avoids the issue in this update.