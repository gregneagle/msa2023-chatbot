If you `munkiimport` the .pkg that installs SMART Notebook (or the entire SMART Learning Suite), you may find the item seems to keep needing to be reinstalled.

To prevent that, install the .pkg on one client machine and then run
```
makepkginfo -f /Applications/SMART\ Technologies/Notebook.app
```
to get the installs array, which you can put into the pkginfo for SMART Notebook.

Here's an example of what that installs array might look like:
```
	<key>installs</key>
	<array>
		<dict>
			<key>CFBundleIdentifier</key>
			<string>com.smarttech.notebook.Notebook.10</string>
			<key>CFBundleShortVersionString</key>
			<string>17.0.1181.0</string>
			<key>CFBundleVersion</key>
			<string>17.0.1181.0</string>
			<key>path</key>
			<string>/Applications/SMART Technologies/Notebook.app</string>
			<key>type</key>
			<string>application</string>
			<key>version_comparison_key</key>
			<string>CFBundleShortVersionString</string>
		</dict>
	</array>
```