_How to remove the Munki tools and associated files_

While an uninstaller is not provided as a package, you can use the commands below to disable the root Munki service and remove all of its components, configuration, and cached data:

    sudo /bin/launchctl unload /Library/LaunchDaemons/com.googlecode.munki.*
 
    # uncomment the following line to remove the app path for pre-Munki 2(!), released late 2014
    # sudo /bin/rm -rf "/Applications/Utilities/Managed Software Update.app"
    sudo /bin/rm -rf "/Applications/Managed Software Center.app"
    
    sudo /bin/rm -f /Library/LaunchDaemons/com.googlecode.munki.*
    sudo /bin/rm -f /Library/LaunchAgents/com.googlecode.munki.*
    sudo /bin/rm -rf "/Library/Managed Installs"
    sudo /bin/rm -f /Library/Preferences/ManagedInstalls.plist
    sudo /bin/rm -rf /usr/local/munki
    sudo /bin/rm /etc/paths.d/munki
    
    sudo /usr/sbin/pkgutil --forget com.googlecode.munki.admin
    sudo /usr/sbin/pkgutil --forget com.googlecode.munki.app
    sudo /usr/sbin/pkgutil --forget com.googlecode.munki.core
    sudo /usr/sbin/pkgutil --forget com.googlecode.munki.launchd
    sudo /usr/sbin/pkgutil --forget com.googlecode.munki.app_usage
    sudo /usr/sbin/pkgutil --forget com.googlecode.munki.python

If you currently leverage the app usage code and services described in [[Removal of Unused Software]], the user-specific launchagent/daemon/service may still be running even after the above. When running as sudo or root, you could see if you have success stopping that particular service by detecting the logged in users ID with code like the following:

    loggedInUserID=$( /usr/sbin/scutil <<< "show State:/Users/ConsoleUser" | /usr/bin/awk '/UID :/ { print $3 }' )
    # we're running at the loginwindow or otherwise got an empty var somehow, bail forcing exit zero because meh
    [[ -n "$loggedInUserID" ]] || exit 0
    if [[ "$loggedInUserID" -gt 499 ]]; then
      /bin/launchctl bootout gui/"$loggedInUserID"/com.googlecode.munki.app_usage_monitor
    fi
