### Introduction

Munki supports the concept of 'blocking_applications'. This causes Munki to skip unattended_installs or uninstalls if certain applications are running, and causes Managed Software Center.app to warn the user to quit conflicting applications if they are running when the user chooses to update without logging out.

### Details

Munki will skip any unattended_installs or unattended_uninstalls if:

- There is a blocking_applications key in the pkginfo, and any application listed is running, or
- There is no blocking_applications key in the pkginfo, and any application in the **installs** list (if it exists) is running.

Additionally, using similar logic as above, Managed Software Update.app will display an alert asking the user to quit any blocking apps that are running if the user chooses to update without logging out.

The blocking_applications list may be added to the pkginfo for any package, and takes this form:

```xml
    <key>blocking_applications</key>
    <array>
    	<string>Firefox</string>
    	<string>Safari</string>
    	<string>Opera</string>
    </array>
```

or

```xml
    <key>blocking_applications</key>
    <array>
    	<string>Firefox.app</string>
    	<string>Safari.app</string>
    	<string>Opera.app</string>
    </array>
```

This sample blocking_applications list would be suitable for use with the Adobe Flash Player installation package.

The string used to identify the application should be the name of the application bundle -- the ".app" extension is optional. Apps do not have to be installed or managed by munki to be included in a blocking_applications list.

Even though it might be useful to block on faceless background applications (like iTunesHelper) or other processes, since normal users do not have the ability to easily quit such processes, don't use them as blocking_applications; instead specify the item needs a logout or restart as applicable. It would be confusing and frustrating for a user to be notified that installation cannot continue because "Microsoft Database Daemon" is running.

#### blocking_applications vs. installs
If there is no blocking_applications array, and there is an installs array containing one or more applications, Munki will use those applications as a substitute blocking_applications array. This can be convenient, as Munki can "automagically" discover blocking applications for drag-n-drop dmg installs. If you need to override this behavior, simply create an actual blocking_applications array listing the actual applications you want to block an install. If you want NO applications to block an install, provide an _empty_ blocking_applications array.

```xml
<key>blocking_applications</key>
<array>
</array>
```

#### --installonly flag also ignores blocking_applications
Blocking applications works when you run `managedsoftwareupdate --auto` or use Managed Software Center.app. If you run `managedsoftwareupdate --installonly`, Munki will ignore any blocking applications.