_Setting up a demonstration Munki Repo and client_

### Introduction

Since Munki can use virtually any web server as its server, and since macOS ships with Apache 2,  it’s very easy to set up a demonstration Munki server on any available Mac. You can even set up a Munki server on a single machine that is also a Munki client, and that is what we'll do here. We will set up Munki on a machine running macOS without Server.app installed.

**If you attempt this Demonstration Setup on a Mac with Server.app installed you will encounter pain and suffering. For this demonstration, use a Mac that does not have Server.app installed.**

> It is certainly possible to set up a Munki repo on a machine with Server.app installed. A Munki repo is simply a set of files on a web server. The exact configuration details vary from version to version of macOS Server, and are not documented here. See Apple documentation on how to configure the web service for your specific version of macOS Server.  
Nick McSpadden has published some notes on setting up a Munki repo on Yosemite Server here: https://osxdominion.wordpress.com/2015/02/26/setting-up-munki-with-os-x-yosemite-server/


### Details

#### Assumptions and requirements

This walk-through assumes the use of a single Mac running macOS 10.10 Yosemite or later. It also assumes you have administrative access, and that Server.app is _not_ installed. It is certainly possible to use Munki on Macs running versions of macOS earlier than 10.10, and to set up a Munki server on a Mac with Server.app, but this guide does not attempt to address those variations.

#### Building a "server" repository

To set up our Munki "server" (in this case, a web server running on the same machine that is also our demonstration client), we’re going to create a directory structure in `/Users/Shared`, and then configure Apache2 to serve it via HTTP. You can do the next few steps via the Finder or via the Terminal, but it’s easier to write them out as Terminal commands:

```bash
cd /Users/Shared/
mkdir munki_repo
mkdir munki_repo/catalogs
mkdir munki_repo/icons
mkdir munki_repo/manifests
mkdir munki_repo/pkgs
mkdir munki_repo/pkgsinfo
```

You might be wondering what that last directory is. The `pkgsinfo` directory holds data that is not used directly by Munki clients, but is used by other Munki tools to create the catalogs. One more thing: let’s make sure the Apache 2 can read and traverse all of these directories:

```bash
chmod -R a+rX munki_repo
```

Next, we need to tell Apache2 to serve the `munki_repo` directory via HTTP. You could edit the `/etc/apache2/httpd.conf` file, or one of the other .conf files used by Apache2, but there’s a much easier method for this demonstration.

```bash
sudo ln -s /Users/Shared/munki_repo /Library/WebServer/Documents/
```
This creates a symlink inside `/Library/WebServer/Documents/` that points to our new `munki_repo` directory. By default on macOS, `/Library/WebServer/Documents/` is Apache 2 ‘s DocumentRoot, so it will serve anything in that directory via HTTP. (Again, if you've installed Server.app, this changes the Apache config in ways not described here.)

#### Activate Apache

Turn on Apache 2 like so:

```bash
sudo apachectl start
```

   This activates the Apache web server, and also activates the launchd job so that Apache will be active across restarts.
   To revert this change:

```bash
sudo apachectl stop
```

#### Populating the repo

We now have a working Munki repo – but it’s completely empty and not useful at all. So let’s start to populate the repo.

We’re going to use some tools distributed with munki to import packages into our new Munki repo. Download the current munki installation package at https://github.com/munki/munki/releases/latest.

Install the Munki tools by double-clicking the Installer package and installing like any other package. A restart is required after installation.

The tools you’ll use as an administrator are available from the command-line, and are installed in `/usr/local/munki`.

The tool we will use to import packages into the munki repo is called `munkiimport`. We need to configure it before we can use it – telling it where to find our repo, among other things.

```bash
bash-3.2$ /usr/local/munki/munkiimport --configure
Repo URL (example: afp://munki.example.com/repo): file:///Users/Shared/munki_repo
pkginfo extension (Example: .plist): <just hit return>
pkginfo editor (examples: /usr/bin/vi or TextMate.app): TextMate.app <substitute your favorite text editor>
Default catalog to use (example: testing): testing
Repo access plugin (defaults to FileRepo): <just hit return>
```

We are first asked for the path to the Munki repo, and since we set one up at `/Users/Shared/munki_repo`, that’s what we enter with the `file://` prefix. If you were hosting a repo remotely, this would typically be an afp:// or smb:// URL specifying the share.

We are then asked to specify an extension to append to the name of pkginfo files. Some admins prefer “.plist”, some prefer “.pkginfo”. Personally, I just leave it blank – Munki doesn’t care. 

Next, you are asked for an editor to use for the pkginfo files. If you like command-line editors, you can specify `/usr/bin/vi` or `/usr/bin/emacs` for example. If you, like me, prefer GUI text editors, you can specify a GUI text editor application by name (but be sure to include the “.app” extension). I picked TextMate.app, but you could choose any suitable text editor like BBEdit.app, Atom.app, or even TextEdit.app.

Next, you are asked for the default catalog new packages/pkginfo should be added to. We'll use a "testing" catalog for this.

Finally, you'll be asked what Repo access plugin to use. Leave this blank, since we'll be using FileRepo.

Next, let’s get a package to import. Firefox is a good example package, and you can download it from http://www.mozilla.com/. As of this writing, the current version is 61.0.2, and when I download it using Safari, a disk image named “Firefox 61.0.2.dmg” is downloaded to my Downloads folder.

We’ll return to the command line to import the Firefox package.

#### Importing Firefox

```bash
bash-3.2$ /usr/local/munki/munkiimport ~/Downloads/Firefox\ 61.0.2.dmg 
           Item name: Firefox 
        Display name: Mozilla Firefox
         Description: Web browser from Mozilla
             Version: 61.0.2
            Category: Internet
           Developer: Mozilla
  Unattended install: False
Unattended uninstall: False
            Catalogs: testing    
Import this item? [y/n] y
Upload item to subdirectory path []: apps/mozilla
Path /Users/Shared/munki_repo/pkgs/apps/mozilla doesn't exist. Create it? [y/n] y
No existing product icon found.
Attempt to create a product icon? [y/n] y
Attempting to extract and upload icon...
Created icon: /Users/Shared/munki_repo/icons/Firefox.png
Copying Firefox 61.0.2.dmg to /Users/Shared/munki_repo/pkgs/apps/mozilla/Firefox 61.0.2.dmg...
Edit pkginfo before upload? [y/n]: y
Saving pkginfo to /Users/Shared/munki_repo/pkgsinfo/apps/mozilla/Firefox-61.0.2...
```

We run the `munkiimport` tool and provide it a path to our downloaded disk image. 

`munkiimport` then asks us to confirm or override some basic information about the package. We accept the item name by simply hitting return, but provide a new “Display name” and “Description”. We accept the version and the catalogs, again, by simply hitting return. We entered a category and developer.

`munkiimport` then prints back our choices and asks if we want to import the item. (If we made any mistakes, this would be a good time to say “no”!) We agree, and `munkiimport` asks us if we’d like to upload the package to a subdirectory path. We could just skip this, and upload everything to the top level of the pkgs directory in the munki repo, but as our number of packages grows, that might get hard to navigate. So we’re going to upload this into a directory named “Mozilla” inside a directory named “apps”. As a sanity check, `munkiimport` warns us that the subdirectory path we’ve chosen doesn’t yet exist. Since this is a brand new repo, we knew in advance that the directory didn’t exist, so we want `munkiimport` to create it for us. 

`munkiimport` looks for an existing uploaded icon for Firefox and doesn't find one, so it offers to create one for us. We agree.

Finally, `munkiimport` copies the Firefox package to `/Users/Shared/munki_repo/pkgs/apps/mozilla/` and saves the pkginfo to `/Users/Shared/munki_repo/pkgsinfo/apps/mozilla/Firefox-61.0.2`.

Since I chose TextMate.app as my editor when I configured `munkiimport` earlier, `munkiimport` next gives the option to open the newly created pkginfo file in TextMate. No matter which editor you choose--if you choose to edit the pkginfo at this time--you'll see a standard Apple property list file (plist) describing the package you just imported.

This gives you another opportunity to edit the pkginfo using your favorite text editor. In this case, we don’t need to make any changes, though, so we can just close it. If we return our attention to the terminal window we used to run `munkiimport`, we’ll see it’s prompting us for one more bit of information:

```
Rebuild catalogs? [y/n] 
```

Remember that Munki clients don’t use the individual pkginfo files; instead they download and consult Munki catalogs to find available software. So to actually make use of the pkginfo we just generated, we need to build new versions of all the defined catalogs. Answering “y” to this prompt causes munkiimport to rebuild the Munki catalogs.

```
Rebuild catalogs? [y/n] y
Adding apps/mozilla/Firefox-61.0.2 to testing...
```

Since we only have one package (and its corresponding pkginfo) in our Munki repo, we see a single item has been added to the testing catalog.
Again we can check our work so far. In your web browser, navigate to` http://localhost/munki_repo/catalogs/testing`. You should see a property list which contains the pkginfo for Firefox.

#### Creating a client manifest

We now have one package in our Munki repo. Our next step is to create a client manifest so that Munki knows what to install on a given machine. 

We'll use the `manifestutil` tool to create our manifest.

```bash
% /usr/local/munki/manifestutil 
Entering interactive mode... (type "help" for commands)
> new-manifest site_default
> add-catalog testing --manifest site_default
Added testing to catalogs of manifest site_default.
> add-pkg Firefox --manifest site_default
Added Firefox to section managed_installs of manifest site_default.
> exit
```

We've created a new manifest named "site_default".  "site_default" is one of the manifests a Munki client looks for by default if not configured to look for a specific manifest by name.
We added "testing" to the list of catalogs to consult, and "Firefox" to the list of packages to install.

If you examine the file at `/Users/Shared/munki_repo/manifests/site_default`, it should look like this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>catalogs</key>
    <array>
        <string>testing</string>
    </array>
    <key>included_manifests</key>
    <array>
    </array>
    <key>managed_installs</key>
    <array>
    	<string>Firefox</string>
    </array>
    <key>managed_uninstalls</key>
    <array>
    </array>
</dict>
</plist>
```

Again, you can check your work in your web browser by navigating to `http://localhost/munki_repo/manifests/site_default`. You should see the file you just created displayed in your web browser.

#### Munki Client Configuration

We’re done (for now) with the server. Next, we need to configure the Munki client so it knows about our server. The Munki client stores its configuration in `/Library/Preferences/ManagedInstalls.plist`. Unless you’ve run the Munki client before, this file won’t yet exist. We’ll use the `defaults` command to create it with the data we need.

```bash
sudo defaults write /Library/Preferences/ManagedInstalls SoftwareRepoURL "http://localhost/munki_repo"
```

We’ve told the client tools the top-level URL for the munki repo -- `http://localhost/munki_repo`. That’s it for the client configuration. If you'd like, check your work with

```bash
defaults read /Library/Preferences/ManagedInstalls
```
which will should show the setting you just made, or
```bash
sudo /usr/local/munki/managedsoftwareupdate --show-config
```
which would show if a .mobileconfig profile were overriding your earlier `defaults write` command.

Either way, make sure the value of "SoftwareRepoURL" is as expected.

> `localhost` is a special name that means "this machine that I am on". It works for the demo because the client and server are on the same machine. When you later set up a "real" Munki server, you need to configure your clients to talk to that server via DNS name (preferred) or IP address. In other words, you'd set the SoftwareRepoURL preference on your client machines to something like "https://munki.sample.org/repo".

#### Testing the Munki client software

Now the moment of truth: let’s run the Munki client from the command line.

```bash
sudo /usr/local/munki/managedsoftwareupdate 
Managed Software Update Tool
Copyright 2010-2014 The Munki Project
https://github.com/munki/munki
    
Downloading Firefox 61.0.2.dmg...
    0..20..40..60..80..100
Verifying package integrity...
The following items will be installed or upgraded:
    + Firefox-61.0.2
        Web browser from Mozilla
    
Run managedsoftwareupdate --installonly to install the downloaded updates.
```

Success! Munki saw that we needed Firefox 61.0.2 and downloaded it. (It did not yet install it – we’ll get to that in a bit.) 

But what if instead when you run `managedsoftwareupdate` you see this:

```bash
sudo /usr/local/munki/managedsoftwareupdate 
Managed Software Update Tool
Copyright 2010-2014 The Munki Project
https://github.com/munki/munki
    
No changes to managed software are available.
```

The most likely reason you see this is because you already have Firefox 61.0.2 (or later) installed. If you really want to test Munki, delete your copy of Firefox:

```bash
sudo rm –r /Applications/Firefox.app
```

Then run `/usr/local/munki/managedsoftwareupdate` again – you should see it being downloaded as in the example above.

#### Demonstrating Managed Software Center.app

We ran `managedsoftwareupdate` from the command line and verified that the munki client tools could talk to our Munki server and download the Firefox package. But, as we’ve noted, `managedsoftwareupdate` did not actually install Firefox. We could call `managedsoftwareupdate` again, this time passing it the `-–installonly` flag to make it install what it just downloaded. But instead, we’re going to introduce another tool – the one “regular” users would interact with – Managed Software Center.app. You’ll find it in the `/Applications` folder. Double-click it to launch it. 

Managed Software Center will check for updates with the Munki server, and should shortly display a window (closely resembling Apple's App Store application's main window) displaying Firefox 61.0.2.

If you click on **Update**, Firefox will be installed.

### Conclusion

You've set up a demonstration of Munki's server and client components. Please be sure to also read [Munki's Frequently Asked Questions](https://github.com/munki/munki/wiki/FAQ)

### Next steps

The demonstration setup involved setting up a Munki server on the same Mac you are using as a Munki client. For a "real" deployment, you'd want a "real" web server hosting your Munki repo. You'll have the easiest time configuring your Munki clients if you can set up that Munki repo so it is available at `http(s)://munki.yourdomain/repo`. This is not _required_, but allows your Munki clients to find your repo with no specific configuration. See [[Default Repo Detection]] for more information.

#### Addendum: cleaning up

If you want to remove and clean up the temporary local Munki server you've created:

```bash
sudo apachectl stop
sudo rm /Library/WebServer/Documents/munki_repo
sudo rm -r /Users/Shared/munki_repo
```

If you also want to remove the local install of the Munki client and its data, see [[Removing Munki]].