_Using munki with a LogoutHook_

### Introduction

When Munki logs a user out to install software, it first returns to the loginwindow, pauses for a few moments, then initiates its installation via a LaunchAgent. It is possible to initiate the Munki installation via a LogoutHook instead, in order to execute the installation right at logout rather than right after logging out. This causes Munki to behave similarly to Apple Software Update (as of 10.5) when installing packages that require a restart.


### Details

No configuration changes to Munki are required. Executing an installation via a LogoutHook harmlessly preempts Munki's own com.googlecode.munki.managedsoftwareupdate-loginwindow.plist LaunchAgent.

The following script can be called directly by a LogoutHook, or integrated into your organization's existing LoginHook/LogoutHook regime.

```bash
    #!/bin/bash
    
    if [ -e /private/tmp/com.googlecode.munki.installatlogout ]; then
    
    export ManagedSoftwareUpdateMode=MunkiStatus
    
    /Applications/Managed\ Software\ Center.app/Contents/MacOS/Managed\ Software\ Center&
    
    /usr/local/munki/managedsoftwareupdate --logoutinstall
    
    fi
    
    exit 0
```

# See also

https://support.apple.com/kb/HT2420

https://developer.apple.com/library/mac/#documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CustomLogin.html

https://afp548.com/static/mactips/loginhooks.html