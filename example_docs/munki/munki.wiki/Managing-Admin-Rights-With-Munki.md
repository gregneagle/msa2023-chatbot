_How to manage local administrative rights for users and groups with Munki._

### Introduction

There is a simple way to manage users and groups who need local admin rights on specific client machines or groups of client machines using Munki.

Benefits of managing local admin rights using this method:

- Faster: Add and remove users and groups to and from the local admin group on machines in an automated-fashion.
- Secure: Ability to track and audit who has admin rights on machines, and remove those rights if necessary.

### Details

We are going to create a script that will do a few things. It will either add a user or a group to the local admin group on a machine. The script will then create an uninstall script and place it on the target system. This script can then be called by Munki to remove the user's or group's admin rights from the machine. The script will also create a file that Munki will use to check if the package is installed.

Steps:

1. Create a postflight script for a package that will be installed using Munki. This is the script I made that you can use or modify if you deem it necessary:

    ```bash
    #!/bin/sh
    
    # (c) 2010 Walter Meyer SUNY Purchase College
    # Add a user or group to the administrators group on a workstation in a "Munki-Friendly" way.
    
    # Change one variable, either the USER or GROUP that you want to give administrative rights to.
    # Make sure to leave one variable empty depending on whether you are adding a user or group.
    USER="some.user"
    GROUP=""
    
    # Create a directory to store the files we will need.
    /bin/mkdir -p /Library/Scripts/Administrative-Rights
    
    # Add the USER or GROUP to the local admin group.
    if [ -n "${USER}" ]; then
    	/usr/sbin/dseditgroup -o edit -n /Local/Default -a $USER -t user admin
    	
    	# Create a file based on what user or group is getting admin rights that Munki can checksum.
    	/bin/echo "$USER" > /Library/Scripts/Administrative-Rights/granted-admin-rights_$USER
    	
    	# Create script that can be used by Munki to remove the user from the admin group.
    	uninstall_script="/Library/Scripts/Administrative-Rights/remove-admin-rights_$USER.sh"
    	/bin/echo "#!/bin/sh" > "$uninstall_script"
    	/bin/echo "/usr/sbin/dseditgroup -o edit -n /Local/Default -d $USER -t user admin" >> "$uninstall_script"
    	/bin/echo "/usr/bin/srm /Library/Scripts/Administrative-Rights/granted-admin-rights_$USER" >> "$uninstall_script"
    	/bin/echo "/usr/bin/srm /Library/Scripts/Administrative-Rights/remove-admin-rights_$USER.sh" >> "$uninstall_script"
    	/bin/echo "exit 0" >> "$uninstall_script"
    else
    	/usr/sbin/dseditgroup -o edit -n /Local/Default -a $GROUP -t group admin
    	
    	# Create a file based on what user or group is getting admin rights that Munki can checksum.
    	/bin/echo "$GROUP" > /Library/Scripts/Administrative-Rights/granted-admin-rights_$GROUP
    	
    	# Create script that can be used by Munki to remove the user from the admin group.
    	uninstall_script="/Library/Scripts/Administrative-Rights/remove-admin-rights_$GROUP.sh"
    	/bin/echo "#!/bin/sh" > "$uninstall_script"
    	/bin/echo "/usr/sbin/dseditgroup -o edit -n /Local/Default -d $GROUP -t group admin" >> "$uninstall_script"
    	/bin/echo "/usr/bin/srm /Library/Scripts/Administrative-Rights/granted-admin-rights_$GROUP" >> "$uninstall_script"
    	/bin/echo "/usr/bin/srm /Library/Scripts/Administrative-Rights/remove-admin-rights_$GROUP.sh" >> "$uninstall_script"
    	/bin/echo "exit 0" >> "$uninstall_script"
    fi
    
    # Permission the directory properly.
    /usr/sbin/chown -R root:admin /Library/Scripts/Administrative-Rights
    /bin/chmod -R 700 /Library/Scripts/Administrative-Rights
    
    exit 0
    ```

2. Make a package that contains the postflight script. I recommend using The Luggage to build the package, but you don't have to. http://wiki.github.com/unixorn/luggage/

3. Add the package to munki and run makepkginfo on the package you made.

4. Install the package on a test workstation. Then run the following command (if you used my script):

    ```bash
    makepkginfo -f /Library/Scripts/Administrative-Rights/granted-admin-rights_some.user
    ```

Take the installs key information and append it to your pkginfo file you created.

5. Next change the uninstall_method key in the pkginfo file to look
like this:

    ```xml
    	<key>uninstall_method</key>
    	<string>/Library/Scripts/Administrative-Rights/remove-admin-rights_some.user.sh</string>
    ```