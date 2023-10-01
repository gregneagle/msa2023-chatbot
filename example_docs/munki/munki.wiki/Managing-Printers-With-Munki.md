_How to add, remove, and manage printers with Munki._

### Introduction

Why add and remove printers using Munki? Why not just use MCX/Profiles?

One major issue with managing printer lists with MCX or Profiles is if the driver file isn't installed on the client system prior to the printer, the printer will be added using the Generic Printer Driver. Even if the printer driver file is installed later the printer continues to use the Generic Printer Driver. Using Munki, the administrator can make the drivers be required to be installed ahead of time.

### Automated Scripts Method

Graham Gilbert has created a script to automate this for the Munki administrator. The original version of printer-pkginfo can be [found here](https://github.com/grahamgilbert/printer-pkginfo), but is no longer being maintained. An updated version is being maintained by Hilary B. Brenum [here](https://github.com/HBBisenieks/printer-pkginfo).

1. The new printer-pkginfo can be used with an XML plist file as input or run interactively.
2. Use the script interactively to generate .pkginfo files `./printer-pkginfo -i -o /PATH/TO/printer.pkginfo`
3. Copy the .pkginfo file to your Munki repo's `pkgsinfo/` directory.
4. Run `makecatalogs`

Nick McSpadden has also created a similar script, [PrinterGenerator](https://github.com/nmcspadden/PrinterGenerator), that leverages the "nopkg" method described below.

1. PrinterGenerator accepts command line options, or a path to a CSV file that lists all the necessary fields for your printers.
2. Use PrinterGenerator to produce your .pkginfo files: `./printer_generator.py --csv /PATH/TO/printers.csv`
3. Copy your pkginfo files into your Munki repository, somewhere in your `munki/pkgsinfo/` directory.
4. Run `makecatalogs`.

### nopkg Method

As of Munki 0.8.3.1634, there is now a "nopkg" type for package-free installation.  This allows us to run scripts directly in Munki without having to create packages to install.  We can use this "nopkg" type to run all of our printer installs from Munki pkginfos, which allows for easy editing in the future.

There are some pros and cons to this approach, but here's the method.

#### Concepts Behind Installing Printers Using nopkg

Normally, when installing packages with Munki, we check receipts or installs arrays to determine whether an install/update is necessary.  Payload-free packages don't leave receipts, so we'd use an installs array.  With nopkg, we can't use receipts because no packages are being installed, so we have to have the logic take place in an installcheck_script instead.

We can use the installcheck_script to determine:
1. Does the printer currently exist on the system?
2. Do the current options of the printer match our specified set of options?

From there, the postinstall_script can actually make the necessary changes by removing any existing matching printer queue and then adding it, with all specified options.

Lastly, the uninstall_script makes it easy to delete the queue by using `lpadmin -x`.

#### How the "nopkg" Pkginfo Works

1) The `installcheck_script` should check the options of the printer.  Note that we don't have to separately call `lpstat` to determine if the printer is installed, because `lpoptions` will exit non-zero if the print queue name doesn't exist.  If you have no printer options to specify, just leave the printerOptions dictionary empty:  

```python
#!/usr/bin/python
import subprocess
import sys

printerOptions = { }

cmd = ['/usr/bin/lpoptions', '-p', 'PRINTERNAME', '-l']
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(lpoptOut, lpoptErr) = proc.communicate()

if lpoptErr:
    sys.exit(0)

for option in lpoptOut.splitlines():
    for myOption in printerOptions.keys():
        optionName = option.split("/", 1)[0]
        optionValues = option.split("/",1)[1].split(":")[1].strip().split(" ")
        for opt in optionValues:
            if "*" in opt:
                actualOptionValue = opt.replace('*', '')
                break
        if optionName == myOption:
            if not printerOptions[myOption] == actualOptionValue:
                sys.exit(0)
                
sys.exit(1)
```

2) The postinstall_script is where the print queue is installed.  If it already exists, remove it first and then reinstall:

```python
#!/usr/bin/python
import subprocess
import sys

# Populate these options if you want to set specific options for the printer. E.g. duplexing installed, etc.
printerOptions = { OPTIONS }

cmd = [ '/usr/sbin/lpadmin', '-x', 'PRINTERNAME' ]
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(lpadminxOut, lpadminxErr) = proc.communicate()

# Install the printer
cmd = [ '/usr/sbin/lpadmin',
        '-p', 'PRINTERNAME',
        '-L', 'LOCATION',
        '-D', 'DISPLAY_NAME',
        '-v', 'lpd://ADDRESS',
        '-P', '/Library/Printers/PPDs/Contents/Resources/DRIVER',
        '-E',
        '-o', 'printer-is-shared=false',
        '-o', 'printer-error-policy=abort-job' ]

for option in printerOptions.keys():
    cmd.append("-o")
    cmd.append(str(option) + "=" +  str(printerOptions[option]))

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(lpadminOut, lpadminErr) = proc.communicate()

if lpadminErr:
    print "Error: %s" % lpadminErr
    sys.exit(1)
print "Results: %s" % lpadminOut    
sys.exit(0)
```

3) The uninstall_script is very simple:

```bash
#!/bin/bash
/usr/sbin/lpadmin -x PRINTERNAME
```

4) The complete pkginfo looks more like this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>autoremove</key>
	<false/>
	<key>catalogs</key>
	<array>
		<string>testing</string>
	</array>
	<key>description</key>
	<string>DESCRIPTION</string>
	<key>display_name</key>
	<string>DISPLAY_NAME</string>
	<key>installcheck_script</key>
	<string>#!/usr/bin/python
import subprocess
import sys

printerOptions = { OPTIONS }

cmd = ['/usr/bin/lpoptions', '-p', 'PRINTERNAME', '-l']
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(lpoptOut, lpoptErr) = proc.communicate()

if lpoptErr:
    sys.exit(0)

for option in lpoptOut.splitlines():
    for myOption in printerOptions.keys():
        optionName = option.split("/", 1)[0]
        optionValues = option.split("/",1)[1].split(":")[1].strip().split(" ")
        for opt in optionValues:
            if "*" in opt:
                actualOptionValue = opt.replace('*', '')
                break
        if optionName == myOption:
            if not printerOptions[myOption] == actualOptionValue:
                sys.exit(0)
                
sys.exit(1)</string>
	<key>installer_type</key>
	<string>nopkg</string>
	<key>minimum_os_version</key>
	<string>10.7.0</string>
	<key>name</key>
	<string>AddPrinter-PRINTERNAME</string>
	<key>postinstall_script</key>
	<string>#!/usr/bin/python
import subprocess
import sys

# Populate these options if you want to set specific options for the printer. E.g. duplexing installed, etc.
printerOptions = { OPTIONS }

cmd = [ '/usr/sbin/lpadmin', '-x', 'PRINTERNAME' ]
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(lpadminxOut, lpadminxErr) = proc.communicate()

# Install the printer
cmd = [ '/usr/sbin/lpadmin',
        '-p', 'PRINTERNAME',
        '-L', 'LOCATION',
        '-D', 'DISPLAY_NAME',
        '-v', 'lpd://ADDRESS',
        '-P', '/Library/Printers/PPDs/Contents/Resources/DRIVER',
        '-E',
        '-o', 'printer-is-shared=false',
        '-o', 'printer-error-policy=abort-job' ]

for option in printerOptions.keys():
    cmd.append("-o")
    cmd.append(str(option) + "=" +  str(printerOptions[option]))

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(lpadminOut, lpadminErr) = proc.communicate()

if lpadminErr:
    print "Error: %s" % lpadminErr
    sys.exit(1)
print "Results: %s" % lpadminOut    
sys.exit(0)</string>
	<key>unattended_install</key>
	<true/>
	<key>uninstall_method</key>
	<string>uninstall_script</string>
	<key>uninstall_script</key>
	<string>#!/bin/bash
/usr/sbin/lpadmin -x PRINTERNAME</string>
	<key>uninstallable</key>
	<true/>
	<key>version</key>
	<string>VERSION</string>
</dict>
</plist>
``` 

This pkginfo makes it an unattended_install, which means it'll trigger even if a user is logged in, without requiring the GUI to activate. It's also an unattended_uninstall, so it can also be removed without user intervention.

The important parts to change:

* **DESCRIPTION** - This is the cosmetic description in Munki.
* **DISPLAY_NAME** - The name that users see in Managed Software Center.
* **PRINTERNAME** - This is the name of the print queue itself.
* **VERSION** - The version number of the pkginfo.  When updating this pkginfo, make sure you update the version accordingly, for your own sanity.
* **LOCATION** - The location of the printer as displayed in the System Preferences.
* **ADDRESS** - The IP or DNS address of the printer to add.
* **DRIVER** - The name of the driver file used for this printer.
* **OPTIONS** - A dictionary of options to configure the printer with on creation.  Since this is a Python dictionary, it should look like "HPOptionDuplexer":"True" for each option you want to specify, comma-separated. See the section below for more details.

5) Throw your pkginfo into your Munki repo and run `makecatalogs`.  Add it to a manifest, and test it out!

#### Pros & Cons to the nopkg Approach

The advantage to using the nopkg method is that all of your logic is being done in the pkginfo directly.  To make any changes to the process simply involves editing the pkginfo.  You don't have to rebuild packages when you make these changes.

This solution offers a bit more flexibility than rebuilding packages, because there's no intermediate step between making changes and seeing results on end clients.  

The disadvantage is that your printer installation is tethered to Munki compatibility only.  If you built standard Apple packages, you could optionally use any tool that supports package installation to install these printers - ARD, Jamf Pro, even a thumb drive and double clicking and going through Installer.app.  If you have a need to install printers without always being able to use Munki, consider building a package that runs the postinstall-script from above instead.

##### An important note about printer drivers and `lpadmin`

If the printer driver that is specified is not installed at the time `lpadmin` installs the printer, you won't see it show up in the Printers pane of the System Preferences.  However, you will still see it listed via `lpstat` or `lpinfo` - which is why Munki may think the printer is installed, even if your users can't actually use it.  

In other words, it's important that `/Library/Printers/PPDs/Contents/Resources/DRIVER` exists *before* you use `lpadmin` to install a printer using that driver. You can do this with Munki logic, by adding a "Requires" array and adding your printer driver packages to it, which will guarantee that the printer won't be installed until after Munki has successfully installed the driver.

### How do I find out what options are available to configure the printer with (Duplex, etc.)?

Install the printer in question on your system first.

Then in terminal:
```bash
lpoptions -p YOUR_CUPS_PRINTER_QUEUE_NAME -l
```
This command will output a list of configurable options for your printer.
So if the output is this:
```bash
BRMonoColor/Color/Grayscale: *Color Mono
BRSlowDrying/Slow Drying Paper: *OFF ON
```
You could set the options variables in the above script to look like this:
```python
printerOptions = { "BRMonoColor":"Color", "BRSlowDrying":"OFF" }
```


### Legacy Method using The Luggage to build packages

*Note: The following method uses The Luggage, however any packager can be used.

To install and remove a printer using Munki, do the following:

**I. Install The Luggage**

1. Install XCode: http://developer.apple.com/technologies/xcode.html

2. Install The Luggage: Download: https://github.com/unixorn/luggage/zipball/master

3. Open Terminal and type:
    ```bash
    cd ~/Downloads/directory_you_extracted_the_luggage_to/
    make pkg
    ```
4. Install the package that was created by the previous command. This installs The Luggage on your system.

**II. Prepare the Printer Install Script**

1. Create a postflight script for a package that will be installed using Munki. This simple shell
script can be modified as necessary:

    ```bash
    #!/bin/sh
    
    # (c) 2010 Walter Meyer SUNY Purchase College
    
    # Script to install and setup printers on a Mac OS X system in a "Munki-Friendly" way.
    # Make sure to install the required drivers first!
    
    # Variables. Edit these.
    printername="SOME_PRINTER_NAME"
    location="SOME LOCATION"
    gui_display_name="HP Color LaserJet 9500N Example"
    address="lpd://printserver.yourcompany.org/SOME_PRINTER_NAME"
    driver_ppd="/Library/Printers/PPDs/Contents/Resources/hp color LaserJet 9500.gz"
    # Populate these options if you want to set specific options for the printer. E.g. duplexing installed, etc.
    option_1=""
    option_2=""
    option_3=""
    
    ### Printer Install ###
    # In case we are making changes to a printer we need to remove an existing queue if it exists.
    /usr/bin/lpstat -p $printername
    if [ $? -eq 0 ]; then
    	/usr/sbin/lpadmin -x $printername
    fi
    
    # Now we can install the printer.
    /usr/sbin/lpadmin \
            -p "$printername" \
            -L "$location" \
            -D "$gui_display_name" \
            -v "$address" \
            -P "$driver_ppd" \
            -o "$option_1" \
            -o "$option_2" \
            -o "$option_3" \
            -o printer-is-shared=false \
            -E
    # Enable and start the printers on the system (after adding the printer initially it is paused).
    /usr/sbin/cupsenable $(lpstat -p | grep -w "printer" | awk '{print$2}')
    
    # Create an uninstall script for the printer.
    uninstall_script="/private/etc/cups/printers_deployment/uninstalls/$printername.sh"
    mkdir -p /private/etc/cups/printers_deployment/uninstalls
    echo "#!/bin/sh" > "$uninstall_script"
    echo "/usr/sbin/lpadmin -x $printername" >> "$uninstall_script"
    echo "/usr/bin/srm /private/etc/cups/printers_deployment/uninstalls/$printername.sh" >> "$uninstall_script"
    
    # Permission the directories properly.
    chown -R root:_lp /private/etc/cups/printers_deployment
    chmod -R 700 /private/etc/cups/printers_deployment
    
    exit 0
    ```

The script installs a printer based on the variables set at the beginning of the script.

**III. Build the Package**

The administrator must build a package that contains the postflight script made using The Luggage.

1. Create a directory where you want the printer installer package to be output to and stored in on your system.

2. Create a file called 'Makefile' in the directory you created. You can use the example Makefile below. Edit the TITLE and the REVERSE_DOMAIN at a minimum.

    ```bash
    #
    #   Copyright 2009 Joe Block <jpb@ApesSeekingKnowledge.net>
    #
    #   Licensed under the Apache License, Version 2.0 (the "License");
    #   you may not use this file except in compliance with the License.
    #       You may obtain a copy of the License at
    #
    #       https://www.apache.org/licenses/LICENSE-2.0
    #
    #   Unless required by applicable law or agreed to in writing, software
    #   distributed under the License is distributed on an "AS IS" BASIS,
    #   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    #   See the License for the specific language governing permissions and
    #   limitations under the License.
    #
    # 
    #  Luggage makefile for building a package that installs a printer.
    
    include /usr/local/share/luggage/luggage.make
    
    TITLE=SOME_UNIQUE_PRINTER_INSTALLER_NAME
    REVERSE_DOMAIN=com.yourcompany
    PAYLOAD=pack-script-postflight
    PACKAGE_VERSION=1.0
    ```

3. Put the postflight script made earlier in this directory.

4. Open terminal and navigate to the directory with your Makefile and postflight script. `cd /PATH/TO/FILES/`

5. Run this command: `make dmg` This will create a dmg file, ready for Munki.

**IV. Add the dmg to your munki repo**

1. Run `makepkginfo` on your printer install dmg/package located on your repo.
E.g:
    ```bash
    makepkginfo /PATH/TO/munki_repo/path_to_your_pkg.dmg > /PATH/TO/munki_repo/path_to_your_pkg.dmg.pkginfo
    ```

2. Next change the uninstall_method key in the pkginfo file to look like so (edit this):
    ```xml
        <key>uninstall_method</key>
    <string>/etc/cups/printers_deployment/uninstalls/your_printername_variable_from_the_postflight_script.sh</string>
    ```

3. Finally add a requires key to the pkginfo file and reference the required driver installation package(s) for the printer (if you haven't added the printer driver installer(s) to your repo yet do it now). E.g.:

    ```xml
        <key>requires</key>
        <array>
            <string>PRINT_DRIVER_INSTALLER.pkg</string>
        </array>
    ```
Here is an example pkginfo file: http://pastebin.com/uwakXxVH

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
    	<key>autoremove</key>
    	<false/>
    	<key>catalogs</key>
    	<array>
    		<string>printer_deployments</string>
    	</array>
    	<key>description</key>
    	<string></string>
    	<key>display_name</key>
    	<string>printserver01_PRINTER01</string>
    	<key>installer_item_hash</key>
    	<string>5b27f8f3df91798b33b74d858adc293b6cbcd1e5d728e0f48c17c19a42bc4592</string>
    	<key>installer_item_location</key>
    	<string>printer_deployments/printers/printserver01_PRINTER01-1.1.dmg</string>
    	<key>installer_item_size</key>
    	<integer>13</integer>
    	<key>minimum_os_version</key>
    	<string>10.4.0</string>
    	<key>name</key>
    	<string>printserver01_PRINTER01</string>
    	<key>receipts</key>
    	<array>
    		<dict>
    			<key>filename</key>
    			<string>printserver01_PRINTER01-1.1.pkg</string>
    			<key>installed_size</key>
    			<integer>0</integer>
    			<key>packageid</key>
    			<string>edu.purchase.printserver01_PRINTER01</string>
    			<key>version</key>
    			<string>1.0</string>
    		</dict>
    	</array>
    	<key>uninstall_method</key>
    	<string>/etc/cups/printers_deployment/uninstalls/printserver01_PRINTER01.sh</string>
    	<key>uninstallable</key>
    	<true/>
    	<key>version</key>
    	<string>1.0</string>
    </dict>
    </plist>
    ```

**Specifying options**

Install the printer in question on your system first.

Then in terminal:
```bash
    lpoptions -p YOUR_CUPS_PRINTER_QUEUE_NAME -l
```
This command will output a list of configurable options for your printer.
So if the output is this:
```bash
    BRMonoColor/Color/Grayscale: *Color Mono
    BRSlowDrying/Slow Drying Paper: *OFF ON
```
I could set the options variables in the script to look like this:
```bash
    option_1="BRMonoColor=Mono"
    option_2="BRSlowDrying=ON"
    option_3=""
```

**Potential Problems:**

If a privileged user removes the printer manually, Munki would have no way of knowing that the printer has been removed. Munki is only aware of the printer being installed based on the fact that your package was installed.

If you change the 'printername' variable in the script with the intention of changing the CUPS name of a printer that is already installed, this will not work. A new printer will be installed if you try this. If you want to change the CUPS printer name for a printer that is already installed you have to remove the existing printer with Munki first.

Also remember that Munki determines whether a printer package is installed based on the information set in your Makefile you built the package with. If you change the TITLE or REVERSE_DOMAIN and build a package with the intention of modifying an existing install it won't work! Just iterate the PACKAGE_VERSION from 1.0 to 1.1 or 1.1 to 1.2, etc.
