You'll likely want to edit the FileMaker Pro .mpkg to get your organization's license information into the Assisted Install.txt. You can find those steps on [FileMaker Pro's website](http://help.filemaker.com/app/answers/detail/a_id/7099/~/assisted-install-for-filemaker-pro-and-filemaker-pro-advanced).

FileMaker Pro will get into an endless install loop unless you create the proper installs array.

For Munki 2, you may want to do the installs array based on the Info.plist instead of the larger bundle, since more recent versions of FileMaker still have `com.filemaker.client.advanced12` as the `CFBundleIdentifier`.

Here's an example of getting the installs array based on the Info.plist:
`makepkginfo -f /Applications/FileMaker\ Pro\ 14\ Advanced/FileMaker\ Pro\ Advanced.app/Contents/Info.plist`

And the resulting installs array you'd put into the pkginfo file:
```
	<key>installs</key>
	<array>
		<dict>
			<key>CFBundleShortVersionString</key>
			<string>14.0.6</string>
			<key>CFBundleVersion</key>
			<string>14.0.6</string>
			<key>path</key>
			<string>/Applications/FileMaker Pro 14 Advanced/FileMaker Pro Advanced.app/Contents/Info.plist</string>
			<key>type</key>
			<string>plist</string>
			<key>version_comparison_key</key>
			<string>CFBundleShortVersionString</string>
		</dict>
	</array>
```

Based on [changes in Munki 3](https://groups.google.com/forum/?utm_medium=email&utm_source=footer#!msg/munki-discuss/SsSb7ZbgGqk/asauUn42CgAJ), it may be okay to get the installs array from the general bundle:
`makepkginfo -f /Applications/FileMaker\ Pro\ 14\ Advanced/FileMaker\ Pro\ Advanced.app`

