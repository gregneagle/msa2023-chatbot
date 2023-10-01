Launch up the `Symantec Endpoint Protection Installer.app`

Even though the installer app will warn you you'll have to reboot, you won't actually have to, so just click *Continue*.

Then, from the menu bar, select *Tools* and then *Create remote deployment package*.

This will create a .pkg you can then import into your Munki repository. For example:
`munkiimport ~/Downloads/SEPRemote.pkg`

Unfortunately, SEP will, by default, go into an endless install loop without an installs array, so you'll have to create an installs array to put into your pkginfo.

Install SEP on a client and then run this (or similar) command on the client machine to get the installs array:
`makepkginfo -f /Applications/Symantec\ Solutions/Symantec\ Endpoint\ Protection.app`

You should get something like this to paste into your pkginfo file:
```
	<key>installs</key>
	<array>
		<dict>
			<key>CFBundleIdentifier</key>
			<string>com.symantec.sep.mainapp</string>
			<key>CFBundleName</key>
			<string>Symantec Endpoint Protection</string>
			<key>CFBundleShortVersionString</key>
			<string>14.0.2415.0200</string>
			<key>CFBundleVersion</key>
			<string>12</string>
			<key>minosversion</key>
			<string>10.6</string>
			<key>path</key>
			<string>/Applications/Symantec Solutions/Symantec Endpoint Protection.app</string>
			<key>type</key>
			<string>application</string>
			<key>version_comparison_key</key>
			<string>CFBundleShortVersionString</string>
		</dict>
	</array>
```