Logger Pro comes as a password-protected .dmg.

To get it into your Munki repo, just use the password you got from Vernier to get to the .pkg on the disk image, and then run `munkiimport` on the .pkg.

Install Logger Pro on a client machine and run `makepkginfo -f /Applications/Logger\ Pro\ 3/Logger\ Pro.app` (or whatever the relevant path is) and then paste the installs array into the pkginfo for Logger Pro. The installs array will prevent the Logger Pro item from getting into an endless install loop.

Here's an example of what that installs array might look like:
```
	<key>installs</key>
	<array>
		<dict>
			<key>CFBundleIdentifier</key>
			<string>com.vernier.loggerpro</string>
			<key>CFBundleName</key>
			<string>Logger Pro</string>
			<key>CFBundleShortVersionString</key>
			<string>3.11</string>
			<key>CFBundleVersion</key>
			<string>3.11</string>
			<key>path</key>
			<string>/Applications/Logger Pro 3/Logger Pro.app</string>
			<key>type</key>
			<string>application</string>
			<key>version_comparison_key</key>
			<string>CFBundleShortVersionString</string>
		</dict>
	</array>
```