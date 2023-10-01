_How to future-proof your Munki configurations by using a preflight script to download the newest configuration information from your repository._

>**NOTE:** This is a user-contributed solution and is not directly part of Munki. It may not work in your environment, or with future OS releases or future releases of Munki.

Configuring a Munki client for the first time isn't difficult. Mostly it's just copying a single `ManagedInstalls.plist` into the `/Library/Preferences` folder. This, however, kind of paints you into a corner.

What if you ever want to change your repository URL? What if you want to change how often users get notified? What if you want to change your policy, and allow users to cancel updates after you've already rolled out Munki to the entirety of your organization? In these scenarios, you'll have to touch every single machine either physically or virtually(through SSH, etc.) to make those configuration changes. That's not a good use of anyone's time. These may seem like crazy things to want to account for in advance, but they actually can be accounted for very simply through the use preflight scripting.

If we think about the informational problems involved for a moment, we can see that there's really only one thing a client absolutely has to know about the configuration...the URL of the server. The server URL is the only setting Munki can't live without. Every other setting has some sort of default that will allow the program to work in some fashion.

The following script abuses that fact:

#### preflight

```python
import sys
import os
from munkilib import fetch
from munkilib import FoundationPlist
from munkilib import prefs

#Dynamic Config Munki Preflight Script by John Rozewicki
#2010-12-08
#
#Script merges config from Munki repo into local config if newer.

## disturbing hack warning! (untested for < 10.11)
## this works around an issue with App Transport Security on 10.11
## Remove the comment hashes from the following 4 lines for 10.11+
#from Foundation import NSBundle
#bundle = NSBundle.mainBundle()
#info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
#info['NSAppTransportSecurity'] = {'NSAllowsArbitraryLoads': True}

RepoURL = "http://YOUR_REPO_ROOT_URL_HERE"
ConfigName = "ManagedInstalls.plist"
ServerConfigName = "ManagedMunkiServer.plist"
ConfigDir = "/Library/Preferences"
ConfigPath = os.path.join(ConfigDir, ConfigName)
ServerConfigURL = os.path.join(RepoURL, ServerConfigName)
ServerConfigPath = os.path.join(ConfigDir, ServerConfigName)

def MergePlists(FromPlist, ToPlist):
    FromPlistData = FoundationPlist.readPlist(FromPlist)
    for item in FromPlistData:
        prefs.set_pref(item, FromPlistData[item])


if (sys.argv[1] != "logoutinstall") and (sys.argv[1] != "installwithnologout"):
    os.system("touch /Users/Shared/.com.googlecode.munki.checkandinstallatstartup")
    print "Checking for new %s" % (ServerConfigName)
    if fetch.munki_resource(
            ServerConfigURL, ServerConfigPath):
        print "     Merging new server settings into configuration."
        MergePlists(ServerConfigPath, ConfigPath)
```

This script looks to the munki repository for a file called `ManagedMunkiServer.plist`. This file is a version of the configuration that contains all non-unique configuration items such as the URL of our Server, the time between notifications, whether a user can cancel updates or not, etc. If the file on the server is newer than the version on the disk then it downloads it. It then opens this file, and overwrites the elements of  `ManagedInstalls.plist` with the elements from the newly downloaded `ManagedMunkiServer.plist`.

This means we can change the configuration of all of our clients at any point by editing a file on the server. If this technique is used in conjunction with WPKGlikeDynamicManifestsWithoutCGI then we have an extremely dynamic configuration with global configuration options and client -> manifest linking all handled by just 2 extra files on the server with 1 preflight script on the client.

Client configuration in this setup then becomes a simple matter of dropping a preflight script into the /usr/local/munki directory. As long as the preflight script is there, the client will always download the newest configuration from the server, and it will always link the right manifest to the client.