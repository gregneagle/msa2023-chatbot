### Introduction

Munki supports embedding metapackage ChoiceChangesXML information into a pkginfo item to customize the installation of a package.

### Details

It's possible to customize package installs with Apple's installer using a "ChoiceChangesXML" file.
This is a snippet of plist-compatible XML that modifies package selection choices when installing a package. See `man installer` for more information. The installer that ships with Mac OS X 10.6.6 or later contains more and better information than earlier versions on ChoiceChangesXML files.

Munki supports embedding ChoiceChangesXML information into a pkginfo item to customize the installation of a metapackage.

Previously, generating a working ChoiceChangesXML was difficult. With 10.6.6 or later's `/usr/sbin/installer`, you can generate a template ChoiceChangesXML file like so:

```bash
installer -showChoiceChangesXML -pkg /path/to/pkg -target /
```

Let's use the munki tools package as an example:

```bash
installer -showChoiceChangesXML -pkg munkitools-6.1.0.4536.pkg -target /
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<array>
	<dict>
		<key>attributeSetting</key>
		<true/>
		<key>choiceAttribute</key>
		<string>visible</string>
		<key>choiceIdentifier</key>
		<string>core</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<true/>
		<key>choiceAttribute</key>
		<string>enabled</string>
		<key>choiceIdentifier</key>
		<string>core</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<integer>1</integer>
		<key>choiceAttribute</key>
		<string>selected</string>
		<key>choiceIdentifier</key>
		<string>core</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<true/>
		<key>choiceAttribute</key>
		<string>visible</string>
		<key>choiceIdentifier</key>
		<string>admin</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<true/>
		<key>choiceAttribute</key>
		<string>enabled</string>
		<key>choiceIdentifier</key>
		<string>admin</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<integer>1</integer>
		<key>choiceAttribute</key>
		<string>selected</string>
		<key>choiceIdentifier</key>
		<string>admin</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<true/>
		<key>choiceAttribute</key>
		<string>visible</string>
		<key>choiceIdentifier</key>
		<string>app</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<true/>
		<key>choiceAttribute</key>
		<string>enabled</string>
		<key>choiceIdentifier</key>
		<string>app</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<integer>1</integer>
		<key>choiceAttribute</key>
		<string>selected</string>
		<key>choiceIdentifier</key>
		<string>app</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<true/>
		<key>choiceAttribute</key>
		<string>visible</string>
		<key>choiceIdentifier</key>
		<string>launchd</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<true/>
		<key>choiceAttribute</key>
		<string>enabled</string>
		<key>choiceIdentifier</key>
		<string>launchd</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<integer>1</integer>
		<key>choiceAttribute</key>
		<string>selected</string>
		<key>choiceIdentifier</key>
		<string>launchd</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<true/>
		<key>choiceAttribute</key>
		<string>visible</string>
		<key>choiceIdentifier</key>
		<string>app_usage</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<true/>
		<key>choiceAttribute</key>
		<string>enabled</string>
		<key>choiceIdentifier</key>
		<string>app_usage</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<integer>1</integer>
		<key>choiceAttribute</key>
		<string>selected</string>
		<key>choiceIdentifier</key>
		<string>app_usage</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<true/>
		<key>choiceAttribute</key>
		<string>visible</string>
		<key>choiceIdentifier</key>
		<string>python</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<true/>
		<key>choiceAttribute</key>
		<string>enabled</string>
		<key>choiceIdentifier</key>
		<string>python</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<integer>1</integer>
		<key>choiceAttribute</key>
		<string>selected</string>
		<key>choiceIdentifier</key>
		<string>python</string>
	</dict>
</array>
</plist>
```

There are 6 subpackage choices and 3 choiceAttributes ("visible", "enabled", and "selected") for each choice, for a total of 18 dictionaries inside the array. Changing the "visible" and "enabled" attributes only affects their display in Installer.app; to control what is installed, we need to control the "selected" choiceAttributes.  We can delete the other choiceAttributes, and are left with:

```xml
<array>
	<dict>
		<key>attributeSetting</key>
		<integer>1</integer>
		<key>choiceAttribute</key>
		<string>selected</string>
		<key>choiceIdentifier</key>
		<string>core</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<integer>1</integer>
		<key>choiceAttribute</key>
		<string>selected</string>
		<key>choiceIdentifier</key>
		<string>admin</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<integer>1</integer>
		<key>choiceAttribute</key>
		<string>selected</string>
		<key>choiceIdentifier</key>
		<string>app</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<integer>1</integer>
		<key>choiceAttribute</key>
		<string>selected</string>
		<key>choiceIdentifier</key>
		<string>launchd</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<integer>1</integer>
		<key>choiceAttribute</key>
		<string>selected</string>
		<key>choiceIdentifier</key>
		<string>app_usage</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<integer>1</integer>
		<key>choiceAttribute</key>
		<string>selected</string>
		<key>choiceIdentifier</key>
		<string>python</string>
	</dict>
</array>
```

Note that I've also removed the plist "wrapper" from around the array. We are going to later add this array to a pkginfo file and we don't want the plist wrapper.

If we don't want to install the munki admin tools (Currently: makecatalogs, makepkginfo, and munkiimport) we'd change the attributeSetting to 0 for choiceAttribute "selected" for choiceIdentifier "admin":

```xml
<array>
	<dict>
		<key>attributeSetting</key>
		<integer>1</integer>
		<key>choiceAttribute</key>
		<string>selected</string>
		<key>choiceIdentifier</key>
		<string>core</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<integer>0</integer>
		<key>choiceAttribute</key>
		<string>selected</string>
		<key>choiceIdentifier</key>
		<string>admin</string>
	</dict>  
	<dict>
		<key>attributeSetting</key>
		<integer>1</integer>
		<key>choiceAttribute</key>
		<string>selected</string>
		<key>choiceIdentifier</key>
		<string>app</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<integer>1</integer>
		<key>choiceAttribute</key>
		<string>selected</string>
		<key>choiceIdentifier</key>
		<string>launchd</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<integer>1</integer>
		<key>choiceAttribute</key>
		<string>selected</string>
		<key>choiceIdentifier</key>
		<string>app_usage</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<integer>1</integer>
		<key>choiceAttribute</key>
		<string>selected</string>
		<key>choiceIdentifier</key>
		<string>python</string>
	</dict>
</array>
```

We can then add this plist/XML snippet to a pkginfo item. The key is "installer_choices_xml":

```xml
<key>installer_choices_xml</key>
<array>
	<dict>
		<key>attributeSetting</key>
		<integer>1</integer>
		<key>choiceAttribute</key>
		<string>selected</string>
		<key>choiceIdentifier</key>
		<string>core</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<integer>0</integer>
		<key>choiceAttribute</key>
		<string>selected</string>
		<key>choiceIdentifier</key>
		<string>admin</string>
	</dict>  
	<dict>
		<key>attributeSetting</key>
		<integer>1</integer>
		<key>choiceAttribute</key>
		<string>selected</string>
		<key>choiceIdentifier</key>
		<string>app</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<integer>1</integer>
		<key>choiceAttribute</key>
		<string>selected</string>
		<key>choiceIdentifier</key>
		<string>launchd</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<integer>1</integer>
		<key>choiceAttribute</key>
		<string>selected</string>
		<key>choiceIdentifier</key>
		<string>app_usage</string>
	</dict>
	<dict>
		<key>attributeSetting</key>
		<integer>1</integer>
		<key>choiceAttribute</key>
		<string>selected</string>
		<key>choiceIdentifier</key>
		<string>python</string>
	</dict>
</array>
```

When installing, munki will pass this ChoiceChangesXML to `/usr/sbin/installer` to customize the installation of the munkitools metapackage. You can use this same technique to customize the installation of most metapackages.

If you change what is installed via this technique, the "receipts" array generated by makepkginfo/munkiimport is likely to contain receipts for components that aren't (now) installed. This can cause Munki to offer the item repeatedly for installation, since the items its looking for to verify installed state are not present. You may need to add an installs array, or edit the receipts array (possibly marking some receipts as optional). See [[How Munki Decides What Needs To Be Installed]] for even more information on this topic.

#### Pre-10.6.6

ChoiceChangesXML generated by 10.6.6 or later's `/usr/sbin/installer` are usable with the installer in earlier versions of Mac OS X, at least back through 10.5, which is the earliest version of the OS on which Munki will run. My recommendation is to save yourself the pain of manually creating ChoiceChangesXML and let `/usr/sbin/installer` in 10.6.6 or later assist you.