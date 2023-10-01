[Geometer's Sketchpad's own documentation on silent installs](http://www.dynamicgeometry.com/Technical_Support/FAQ/Installation_and_Compatibility/Silent_and_command-line_installs.html) is actually incorrect.

To get the silent install to work properly, you need to use single quotes instead of double quotes when activating, and you need to wait a few seconds before doing so. Here's an example of what would be your postinstall_script in your Munki pkginfo:
```
#!//bin/bash
sleep 3
/Applications/GSP5.app/Contents/MacOS/GSP5_Rel_KCPT_31_105 -license register -name 'Name of Your School' –code ************************
sleep 2
```
Similarly, your preuninstall_script would be:
```
#!/bin/bash
/Applications/GSP5.app/Contents/MacOS/GSP5_Rel_KCPT_31_105 -license deregister -name 'Name of Your School' –code ************************
sleep 3
```
