# Example of how the tools work

# Introduction

Here's a look at the current functionality of the tools.


# Details

To wrap your head around the current functionality of the munki tools, here's a sample workflow...

On the server, we have a manifest file for a client that looks like this:

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
            <key>catalogs</key>
            <array>
                <string>testing</string>
                <string>production</string>
            </array>
            <key>included_manifests</key>
            <array>
            </array>
            <key>managed_installs</key>
            <array>
                    <string>ServerAdminTools</string>
                    <string>TextWrangler</string>
                    <string>Silverlight</string>
            </array>
            <key>managed_uninstalls</key>
            <array>
            </array>
    </dict>
    </plist>

Note that under "managed_installs" we have listed three items.
On the client:

    root# /usr/local/munki/managedsoftwareupdate
    Managed Software Update
    
    Retreiving list of software for this machine...
    	0..20..40..60..80..100
    

The manifest is downloaded from the server.  In this demo, it's simply named after the FQDN of the host.

    Retreiving catalog 'testing'...
    	0..20..40..60..80..100
    Retreiving catalog 'production'...
    	0..20..40..60..80..100

The testing and production catalogs are downloaded from the server.  Each contains a list of available software.

    Downloading TextWrangler2.3.dmg
    	0..20..40..60..80..100
    Downloading Silverlight.2.0.40115.0.dmg
    	0..20..40..60..80..100

managedsoftwareupdate compares the list of managed_installs to what's actually installed on the machine and determines that TextWrangler and Silverlight need to be installed. It then downloads installer items for those items.
Finally, it prints a summary of what needs to be done:

    The following items will be installed or upgraded:
        + TextWrangler-2.3
            Free text editor from the makers of BBEdit
        + Silverlight-2.0.40115.0.0
            Microsoft browser plugin for rich Internet experience

That's the initial run of managedsoftwareupdate.  It writes out an InstallInfo.plist that looks like this:

    root# cat /Library/Managed\ Installs/InstallInfo.plist 
    
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
    	<key>managed_installs</key>
    	<array>
    		<dict>
    			<key>description</key>
    			<string>Apple's administration tools for OS X server.</string>
    			<key>installed</key>
    			<true/>
    			<key>installed_version</key>
    			<string>10.5.3</string>
    			<key>manifestitem</key>
    			<string>ServerAdminTools</string>
    			<key>name</key>
    			<string>ServerAdministrationSoftware</string>
    		</dict>
    		<dict>
    			<key>description</key>
    			<string>Free text editor from the makers of BBEdit</string>
    			<key>display_name</key>
    			<string>TextWrangler</string>
    			<key>installed</key>
    			<false/>
    			<key>installer_item</key>
    			<string>TextWrangler2.3.dmg</string>
    			<key>manifestitem</key>
    			<string>TextWrangler</string>
    			<key>name</key>
    			<string>TextWrangler</string>
    			<key>version_to_install</key>
    			<string>2.3</string>
    		</dict>
    		<dict>
    			<key>description</key>
    			<string>Microsoft browser plugin for rich Internet experience</string>
    			<key>display_name</key>
    			<string>Microsoft Silverlight</string>
    			<key>installed</key>
    			<false/>
    			<key>installer_item</key>
    			<string>Silverlight.2.0.40115.0.dmg</string>
    			<key>manifestitem</key>
    			<string>Silverlight</string>
    			<key>name</key>
    			<string>Silverlight</string>
    			<key>version_to_install</key>
    			<string>2.0.40115.0.0</string>
    		</dict>
    	</array>
    	<key>removals</key>
    	<array>
    	</array>
    </dict>
    </plist>

This shows the state of each managed item, and is used by the managedsoftwareupdate to do the actual installs.  Let's do that now:

    root# /usr/local/munki/managedsoftwareupdate --installonly 
    Mounting disk image TextWrangler2.3.dmg
    Preparing for installation
    Preparing the Disk
    Preparing Target Volume
    Preparing TextWrangler2.3
    Installing TextWrangler2.3
    Configuring Installation
    Validating package
    Writing files
    Writing files: 28% complete
    Writing files: 66% complete
    Writing package receipt
    Finishing Installation
    Finishing Installation
    The software was successfully installed
    Mounting disk image Silverlight.2.0.40115.0.dmg
    Preparing for installation
    Preparing the Disk
    Preparing Target Volume
    Preparing Microsoft® Silverlight™ Browser Plug-In
    Running Microsoft® Silverlight™ Browser Plug-In Installer script
    Installing Microsoft® Silverlight™ Browser Plug-In
    Configuring Installation
    Validating package
    Writing files
    Writing files: 0% complete
    Writing files: 95% complete
    Writing package receipt
    Finishing Installation
    Running Microsoft® Silverlight™ Browser Plug-In Installer script
    Finishing Installation
    The software was successfully installed

managedsoftwareyupdate reads the contents of !InstallInfo.plist and installs the items in order, using the installation packages downloaded and cached earlier.  It also logs its actions in /Library/Managed\ Installs/Logs/ManagedSoftwareUpdate.log:

    Mon May 11 11:36:06 2009 ### Beginning managed installer session ###
    Mon May 11 11:36:06 2009 Processing installs
    Mon May 11 11:36:06 2009 Mounting disk image TextWrangler2.3.dmg
    Mon May 11 11:36:10 2009 Installing TextWrangler2.3 from TextWrangler2.3.pkg
    Mon May 11 11:36:12 2009  Package name is TextWrangler2.3
    Mon May 11 11:36:12 2009  Installing at base path /
    Mon May 11 11:36:16 2009  The install was successful.
    Mon May 11 11:36:21 2009 Install of TextWrangler2.3 was successful.
    Mon May 11 11:36:21 2009 Mounting disk image Silverlight.2.0.40115.0.dmg
    Mon May 11 11:36:26 2009 Installing Microsoft® Silverlight™ Browser Plug-In from Silverlight.2.0.pkg
    Mon May 11 11:36:28 2009  Package name is Microsoft® Silverlight™ Browser Plug-In
    Mon May 11 11:36:28 2009  Installing at base path /
    Mon May 11 11:36:31 2009  The install was successful.
    Mon May 11 11:36:32 2009 Install of Microsoft® Silverlight™ Browser Plug-In was successful.
    Mon May 11 11:36:33 2009 ###    End managed installer session    ###

If we run managedsoftwareupdate again...

    root# /usr/local/munki/managedsoftwareupdate 
    Managed Software Update
    
    No changes to managed software scheduled.

For more info, let's look at the log (/Library/Managed Installs/Logs/ManagedSoftwareUpdate.log):

    Mon May 11 11:38:10 2009 ### Beginning managed software check ###
    Mon May 11 11:38:10 2009 Getting manifest client_manifest.plist from http://munki/repo/manifests/greg_neagle...
    Mon May 11 11:38:10 2009 **Checking for installs**
    Mon May 11 11:38:10 2009 Getting catalog testing from http://munki/repo/catalogs/testing...
    Mon May 11 11:38:10 2009 Getting catalog production from http://munki/repo/catalogs/production...
    Mon May 11 11:38:10 2009 Looking for detail for: ServerAdminTools, version latest...
    Mon May 11 11:38:10 2009 Found: ServerAdministrationSoftware  10.5.6.1.1  apps/ServerAdmin10.5.6v1.1.dmg
    Mon May 11 11:38:10 2009 ServerAdminTools version 10.5.3 is already installed.
    Mon May 11 11:38:10 2009 Looking for detail for: TextWrangler, version latest...
    Mon May 11 11:38:10 2009 Found: TextWrangler  2.3  apps/TextWrangler2.3.dmg
    Mon May 11 11:38:10 2009 TextWrangler version 2.3 is already installed.
    Mon May 11 11:38:10 2009 Looking for detail for: Silverlight, version latest...
    Mon May 11 11:38:10 2009 Found: Silverlight  2.0.40115.0.0  internet/Silverlight.2.0.40115.0.dmg
    Mon May 11 11:38:11 2009 Silverlight version 2.0.40115.0.0 is already installed.
    Mon May 11 11:38:11 2009 **Checking for removals**
    Mon May 11 11:38:11 2009 No changes to managed software scheduled.
    Mon May 11 11:38:11 2009 ###    End managed software check    ###

managedsoftwareupdate determines that all our managed items are installed and schedules no work to be done.

We can run managedsoftwareupdate --installonly again:

    aquaman:~ root# /usr/local/munki/managedsoftwareupdate --installonly
    aquaman:~ root#

and it does nothing:

    root# tail /Library/Managed\ Installs/Logs/ManagedSoftwareUpdate.log 
    Mon May 11 11:41:53 2009 ### Beginning managed installer session ###
    Mon May 11 11:41:53 2009 ###    End managed installer session    ###

I can remove a managed item:

    root# rm -rf /Applications/TextWrangler.app

and when I run managedsoftwareupdate again:

    root# /usr/local/munki/managedsoftwareupdate 
    Managed Software Update
    
    Downloading TextWrangler2.3.dmg
    	0..20..40..60..80..100
    The following items will be installed or upgraded:
        + TextWrangler-2.3
            Free text editor from the makers of BBEdit

It sees !TextWrangler is missing and schedules a reinstall.

    root# /usr/local/munki/managedsoftwareupdate --installonly 
    Mounting disk image TextWrangler2.3.dmg
    Preparing for installation
    Preparing the Disk
    Preparing Target Volume
    Preparing TextWrangler2.3
    Installing TextWrangler2.3
    Configuring Installation
    Validating package
    Writing files
    Writing files: 3% complete
    Writing files: 9% complete
    Writing files: 17% complete
    Writing files: 29% complete
    Writing files: 38% complete
    Writing files: 47% complete
    Writing files: 58% complete
    Writing files: 65% complete
    Writing files: 65% complete
    Writing files: 67% complete
    Writing files: 71% complete
    Writing files: 75% complete
    Writing files: 77% complete
    Writing files: 77% complete
    Writing files: 91% complete
    Writing package receipt
    Finishing Installation
    Finishing Installation
    The software was successfully installed


Finally, we can edit the manifest on the server to remove items:

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
            <key>catalogs</key>
            <array>
                    <string>testing</string>
                    <string>production</string>
            </array>
            <key>included_manifests</key>
            <array>
            </array>
            <key>managed_installs</key>
            <array>
                    <string>ServerAdminTools</string>
            </array>
            <key>managed_uninstalls</key>
            <array>
                    <string>TextWrangler</string>
                    <string>Silverlight</string>
            </array>
    </dict>
    </plist>
    

Here we've moved !TextWrangler and Silverlight from the managed_installs to the managed_uninstalls.  On the client, we'll run managedsoftwareupdate again:

    root# /usr/local/munki/managedsoftwareupdate 
    Managed Software Update
    
    Retreiving list of software for this machine...
    	0..20..40..60..80..100
    The following items will be removed:
        - TextWrangler
        - Silverlight

A little more detail:

    root# tail /Library/Managed\ Installs/Logs/ManagedSoftwareUpdate.log
    Mon May 11 11:48:39 2009 ### Beginning managed software check ###
    Mon May 11 11:48:39 2009 Getting manifest client_manifest.plist from http://localhost/repo/manifests/greg_neagle...
    Mon May 11 11:48:39 2009 **Checking for installs**
    Mon May 11 11:48:39 2009 Getting catalog testing from http://localhost/repo/catalogs/testing...
    Mon May 11 11:48:39 2009 Getting catalog production from http://localhost/repo/catalogs/production...
    Mon May 11 11:48:39 2009 Looking for detail for: ServerAdminTools, version latest...
    Mon May 11 11:48:39 2009 Found: ServerAdministrationSoftware  10.5.6.1.1  apps/ServerAdmin10.5.6v1.1.dmg
    Mon May 11 11:48:39 2009 ServerAdminTools version 10.5.3 is already installed.
    Mon May 11 11:48:39 2009 **Checking for removals**
    Mon May 11 11:48:39 2009 Processing manifest item TextWrangler...
    Mon May 11 11:48:39 2009 Looking for all items matching: TextWrangler...
    Mon May 11 11:48:40 2009 Removal of TextWrangler added to ManagedInstaller tasks.
    Mon May 11 11:48:40 2009 Processing manifest item Silverlight...
    Mon May 11 11:48:40 2009 Looking for all items matching: Silverlight...
    Mon May 11 11:48:41 2009 Removal of Silverlight added to ManagedInstaller tasks.
    Mon May 11 11:48:41 2009 The following items will be removed:
    Mon May 11 11:48:41 2009     - TextWrangler
    Mon May 11 11:48:41 2009     - Silverlight
    Mon May 11 11:48:41 2009 ###    End managed software check    ###

managedsoftwareupdate notes that !ServerAdminTools is already installed.  It then looks at !TextWrangler, sees it is currently installed, and schedules it for removal. Same for Silverlight.  Here's what the !InstallInfo.plist now looks like:

    root# cat /Library/Managed\ Installs/InstallInfo.plist 
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
    	<key>managed_installs</key>
    	<array>
    		<dict>
    			<key>description</key>
    			<string>Apple's administration tools for OS X server.</string>
    			<key>installed</key>
    			<true/>
    			<key>installed_version</key>
    			<string>10.5.3</string>
    			<key>manifestitem</key>
    			<string>ServerAdminTools</string>
    			<key>name</key>
    			<string>ServerAdministrationSoftware</string>
    		</dict>
    	</array>
    	<key>removals</key>
    	<array>
    		<dict>
    			<key>description</key>
    			<string>Free text editor from the makers of BBEdit</string>
    			<key>display_name</key>
    			<string>TextWrangler</string>
    			<key>installed</key>
    			<true/>
    			<key>installed_version</key>
    			<string>2.3</string>
    			<key>manifestitem</key>
    			<string>TextWrangler</string>
    			<key>name</key>
    			<string>TextWrangler</string>
    			<key>packages</key>
    			<array>
    				<string>com.poleposition-sw.lanrev_installease_TextWrangler2.3.pkg</string>
    			</array>
    			<key>uninstall_method</key>
    			<string>removepackages</string>
    		</dict>
    		<dict>
    			<key>description</key>
    			<string>Microsoft browser plugin for rich Internet experience</string>
    			<key>display_name</key>
    			<string>Microsoft Silverlight</string>
    			<key>installed</key>
    			<true/>
    			<key>installed_version</key>
    			<string>2.0.40115.0.0</string>
    			<key>manifestitem</key>
    			<string>Silverlight</string>
    			<key>name</key>
    			<string>Silverlight</string>
    			<key>packages</key>
    			<array>
    				<string>com.microsoft.installSilverlightPlugin</string>
    			</array>
    			<key>uninstall_method</key>
    			<string>removepackages</string>
    		</dict>
    	</array>
    </dict>
    </plist>

We run managedsoftwareupdate --installonly again:

    root# /usr/local/munki/managedsoftwareupdate --installonly 
    Removing TextWrangler...
    Gathering information on installed packages: 
    	0..20..40..60..80..100
    Determining which filesystem items to remove: 
    Removing filesystem items: 
    	0..20..40..60..80..100
    Removing receipt info: 
    	0..20..40..60..80..100
    
    Removing Silverlight...
    Determining which filesystem items to remove: 
    Removing filesystem items: 
    	0..20..40..60..80..100
    Removing receipt info: 
    	0..20..40..60..80..100
    

Looking at the log:

    Mon May 11 11:54:05 2009 ### Beginning managed installer session ###
    Mon May 11 11:54:05 2009 Processing removals
    Mon May 11 11:54:05 2009 Removing TextWrangler...
    Mon May 11 11:54:05 2009 Gathering information on installed packages
    Mon May 11 11:54:05 2009 /Library/Receipts/BSD.pkg is not a valid receipt. Skipping.
    Mon May 11 11:55:20 2009 Determining which filesystem items to remove
    Mon May 11 11:55:28 2009 Removing filesystem items
    Mon May 11 11:55:28 2009 Removing: /usr/share/man/man1/edit.1
    Mon May 11 11:55:28 2009 Removing: /usr/bin/edit
    Mon May 11 11:55:28 2009 Removing: /Applications/TextWrangler.app/Contents/Resources/twdiff.1
    Mon May 11 11:55:28 2009 Removing: /Applications/TextWrangler.app/Contents/Resources/twdiff
    [snip]
    Mon May 11 11:55:30 2009 Removing: /Applications/TextWrangler.app/Contents/Info.plist
    Mon May 11 11:55:30 2009 Removing: /Applications/TextWrangler.app/Contents
    Mon May 11 11:55:30 2009 Removing: /Applications/TextWrangler.app
    Mon May 11 11:55:30 2009 Removing receipt info
    Mon May 11 11:55:30 2009 Removing /Library/Receipts/TextWrangler2.3.pkg...
    Mon May 11 11:55:50 2009 Uninstall of TextWrangler was successful.
    Mon May 11 11:55:50 2009 Removing Silverlight...
    Mon May 11 11:55:50 2009 Determining which filesystem items to remove
    Mon May 11 11:55:57 2009 Removing filesystem items
    Mon May 11 11:55:57 2009 Removing: /Library/Internet Plug-Ins/Silverlight.plugin/Contents/Resources/zh-Hant.lproj/Localizable.strings
    Mon May 11 11:55:57 2009 Removing: /Library/Internet Plug-Ins/Silverlight.plugin/Contents/Resources/zh-Hant.lproj
    [snip]
    Mon May 11 11:55:59 2009 Removing: /Library/Internet Plug-Ins/Silverlight.plugin/Contents/MacOS
    Mon May 11 11:55:59 2009 Removing: /Library/Internet Plug-Ins/Silverlight.plugin/Contents/Info.plist
    Mon May 11 11:55:59 2009 Removing: /Library/Internet Plug-Ins/Silverlight.plugin/Contents
    Mon May 11 11:55:59 2009 Removing: /Library/Internet Plug-Ins/Silverlight.plugin
    Mon May 11 11:55:59 2009 Removing receipt info
    Mon May 11 11:55:59 2009 Removing /Library/Receipts/Silverlight.2.0.pkg...
    Mon May 11 11:56:12 2009 Uninstall of Silverlight was successful.
    Mon May 11 11:56:12 2009 ###    End managed installer session    ###

If we run managedsoftwareupdate again, there's nothing to do:

    root# ./usr/local/munki/managedsoftwareupdate
    Managed Software Update
    
    No changes to managed software scheduled.