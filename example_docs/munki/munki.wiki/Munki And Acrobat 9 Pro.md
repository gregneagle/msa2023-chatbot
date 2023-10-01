_Suppressing Self-Heal for Acrobat 9 Pro installs._

### Introduction

Adding this key to the end of your pkginfo file for Acrobat 9 Pro updates will prevent self-heal from occuring.  This is desirable when your end-users are not admins or in a lab environment.  

Ideally, this would only run after the most recent Adobe update is installed, but it would be acceptable for it to be included in each and every update.

#### postinstall_script

    	<key>postinstall_script</key>
    	<string>#!/bin/bash
    sed -i .bak 's/\&lt;string\&gt;AcroEFGPro90SelfHeal\.xml\&lt;\/string\&gt;//g' /Applications/Adobe\ Acrobat\ 9\ Pro/Adobe\ Acrobat\ Pro.app/Contents/MacOS/SHInit.xml
    sed -i .bak 's/\&lt;string\&gt;AcroEFGDist90SelfHeal\.xml\&lt;\/string\&gt;//g' /Applications/Adobe\ Acrobat\ 9\ Pro/Acrobat\ Distiller.app/Contents/MacOS/SHInit.xml
    	</string>