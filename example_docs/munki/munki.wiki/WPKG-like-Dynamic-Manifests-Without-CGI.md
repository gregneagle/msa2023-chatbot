_An example of using preflight scripts and a server-side plist to achieve WPKG-like grouping of clients based on hostnames and regex._

>**NOTE:** This is a user-contributed solution and is not directly part of Munki. It may not work in your environment, or with future OS releases or future releases of Munki.

### The Problem

Out of the box, client configuration scenarios for Munki feel like trying to choose between the lesser of a handful of evils. Looking at all the documentation, I saw no middle ground between the following 3 cases:

1. Specific `ClientIdentifier`'s specifically written into the client configuration plist. This requires changing client-id's individually on the client-side when wanting to make manifest configuration more granular or changing which manifest a client receives. Large scale changes become difficult, and tracking which clients are in which group becomes a chore.
1. For server-side configuration of `ClientIdentifier`'s you can make a manifest with the exact name of a client, but then there needs to be one manifest for each client even if most of the clients have 90% similar software to each other. As well, when a new client is installed there needs to be a manifest created before it can receive software updates. This is the only future-proof way to roll-out munki without further scripting or programming.
1. As a last resort, you could simply use the default manifest to serve all software to all clients. This means department-specific licensed software isn't managed, and so needs to be done manually. That defeats a lot of the purpose of managed software.

None of these are ideal, but they're really the only options for Munki out of the box unless you want to script your own CGI based off the example. Unfortunately, this complicates the server setup. Do you really want to enable CGI just to cater to one script? What if you can't enable CGI because you're hosting the Munki repository off of a NAS box? There's elegance and worth in the flat file server structure. It makes backup and portability a cinch.

### The Solution

The answer is to adopt WPKG's behavior for attaching manifests to hostnames while using a preflight script for the matching logic in order to maintain flat file server structure. For those who haven't worked with WPKG, at its heart the hosts.xml file is just a list of hosts and profiles. The magic, though, is that it allows for regex in the definition of hostnames. So if you construct your `hosts.xml` as a list going from most specific to least specific regex then you get configuration files that are only ever as granular as they need to be. The hosts.xml, or in this case the `MunkiManagedHosts.plist`, resides on the server while the logic for matching the regex to the hostname is done through a preflight script on the client.

Below is an example based on the configuration currently in use at my organization. I have a bunch of ordinary clients that only need the basic set of software. I also have a few departments, like Editorial, that use a few other pieces of software. In addition, I have a single test machine which needs to be getting a separate set of packages so that I can test packages before rolling them out to users.

My test machine has the hostname "IT2". Editorial machines have hostnames like "Editorial1", "Editorial2","Editorial3", and so on. Other machines have a variety of other names. In practice, my `ManagedMunkiHosts.plist` file comes out looking something like this:

#### MunkiManagedHosts.plist

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">

<!--
Format of file and behavior based on WPKG.org's hosts.xml behavior.
Host names can be either direct matches or in the form of a regex.
Script returns only first match, so be careful with specificity and ordering of hosts.
-->
<dict>
    <key>hosts</key>
    <array>
         <!-- configure one specific host like my test machine-->
        <dict>
            <key>name</key>
            <string>IT1</string>
            <key>manifest-id</key>
            <string>testing</string>
        </dict>
         <!-- take advantage of internal naming schemes to separate by department -->
        <dict>
            <key>name</key>
            <string>EDITORIAL.+</string>
            <key>manifest-id</key>
            <string>editorial</string>
        </dict>
        <!-- use a catch-all for all other basic clients-->
        <dict>
            <key>name</key>
            <string>.+</string>
            <key>manifest-id</key>
            <string>default</string>
        </dict>
    </array>
</dict>
</plist>
```

The `MunkiManagedHosts.plist` regex solution allows fine control over granularity, but doesn't make that granularity a requirement for admins that don't want to shoot themselves in the foot with something that would be difficult to change later. 

In terms of the structure of my manifests, I have a default manifest for all software that needs to be installed everywhere. Then I have the editorial manifest that refers to the default manifest, but then adds a few department-specific pieces of software. My testing manifest gets all default software, but from the testing catalog rather than the default catalog.

The preflight script that makes this all possible is as follows:

#### preflight

```python
#!/usr/bin/python

import sys
import os
import socket
import re
from munkilib import fetch
from munkilib import FoundationPlist
from munkilib import prefs

## disturbing hack warning! (untested for < 10.11)
## this works around an issue with App Transport Security on 10.11
## Remove the comment hashes from the following 4 lines for 10.11+
#from Foundation import NSBundle
#bundle = NSBundle.mainBundle()
#info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
#info['NSAppTransportSecurity'] = {'NSAllowsArbitraryLoads': True}

#
#WPKG-like Dynamic Manifest based on Hostname Preflight Script by John Rozewicki
#2010-12-08
#
#Pulls the hosts plist config from Munki repo if newer. This hosts plist is 
#a regex-able mapping of hostnames to manifests in order to mimic the 
#functionality of the WPKG hosts.xml file.
#
#Hosts from the hosts plist are parsed in order, and the script bails after the
#first match. This allows for specificity of manifests to be handled server-side
#rather than on the client, and also allows for admins to make manifest
#delineation only as granular as is necessary.
#

RepoURL = "http://YOUR_REPO_ROOT_URL_HERE"
ConfigName = "ManagedInstalls.plist"
HostsFileName = "ManagedMunkiHosts.plist"
ConfigDir = "/Library/Preferences"
ConfigPath = os.path.join(ConfigDir, ConfigName)
HostsFileURL = os.path.join(RepoURL, HostsFileName)
HostsFilePath = os.path.join(ConfigDir, HostsFileName)

def UpdateClientIdentifier(ManifestName):
    prefs.set_pref( "ClientIdentifier", ManifestName )

if (sys.argv[1] != "logoutinstall") and (sys.argv[1] != "installwithnologout"):
    print "Checking for new %s" % (HostsFileName)
    if fetch.munki_resource(url=HostsFileURL, destination=HostsFilePath):
        hostname = socket.gethostname()
        print "     Matching hostname to manifest."
        for host in FoundationPlist.readPlist(HostsFilePath)["hosts"]:
            name = host["name"].lower()
            manifest = host["manifest-id"].lower()
            if re.match(name, hostname):
                print "     Setting ClientIdentifier to manifest name: %s." % (manifest)
                UpdateClientIdentifier(manifest)
                break
```

If this technique is used in conjunction with [Dynamic Client Configurations Via Preflight Scripting](Dynamic-Client-Configurations-Via-Preflight-Scripting) then we have an extremely dynamic configuration with global configuration options and client -> manifest linking all handled by just 2 extra files on the server with 1 preflight script on the client.

Client configuration in this setup then becomes a simple matter of dropping a preflight script into the `/usr/local/munki` directory. As long as the preflight script is there, the client will always download the newest configuration from the server, and it will always link the right manifest to the client.