_Options for updating Munki tools on client machines_

### tl;dr:

Use AutoPkg and run the munkitools6.munki recipe.  
Make sure "munkitools" and optionally "munkitools_app_usage" are in managed_installs in an manifest your clients will use.

### Details

The Munki tools are distributed as a distribution package, which contains multiple component packages. This enables several things for the Munki admin:

1. Admins can choose to install only a subset of the Munki tools; for example, they can choose to *not* install the Munki admin tools (makecatalogs, makepkginfo, munkiimport) on most client machines (though doing so is probably not worth the effort).
1. If you have customized or replaced the launchd jobs used by Munki, you can upgrade to newer tools without having your changes overwritten, by choosing not to install the launchd jobs that are included with the munkitools pkg.
1. You can elect to not import/install Munki's embedded Python and use a different Python install you manage.
1. In many cases, you can update the Munki tools silently in the background without needing a restart. As long as the launchd subpackage has not changed, no reboot is required.

All of these require installing only a subset of the packages included in the distribution package. There are a few approaches to accomplishing that:

1. Using installer's ChoiceChangesXML files and Munki's support for embedding them into pkginfo. You could, for example, use the following installer_choices_xml to install only the core tools, Python, and Managed Software Center.app; skipping the install of the admin tools, the app_usage tools and the launchd plists:

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
            <integer>0</integer>
            <key>choiceAttribute</key>
            <string>selected</string>
            <key>choiceIdentifier</key>
            <string>launchd</string>
        </dict>
        <dict>
            <key>attributeSetting</key>
            <integer>0</integer>
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
        <dict>
            <key>attributeSetting</key>
            <integer>0</integer>
            <key>choiceAttribute</key>
            <string>selected</string>
            <key>choiceIdentifier</key>
            <string>no_python</string>
        </dict>
    </array>
    ```

1. Editing the Distribution file inside the munkitools distribution pkg -- this would have a similar effect as the previous approach, but could be used outside of Munki -- for example, if installing the tools via ARD or manually.

#### Easier approach

An easier approach is to extract the component pkgs from the distribution pkg, and then import each component pkg seperately.  

You can create pkginfo items for munki-core, munki-admin, munki-app, munki-launchd, munki-app_usage and munki-python and use Munki's dependency relationships to ensure everything needed gets installed and that reboots are enforced only when necessary.

<table>
  <tr><td>munki-python</td><td>unattended_install: True</td><td></td></tr>
  <tr><td>munki-launchd</td><td>RestartAction: RequireRestart</td><td></td></tr>
  <tr><td>munki-core</td><td>unattended_install: True</td><td>requires: munki-python, munki-launchd</td></tr>
  <tr><td>munki-app</td><td>unattended_install: True</td><td>requires: munki-core</td></tr>
  <tr><td>munki-admin</td><td>unattended_install: True</td><td>requires: munki-core</td></tr>
  <tr><td>munki-app_usage</td><td>unattended_install: True</td><td>requires: munki-core</td></tr>
</table>

If a managed_installs in a manifest specified only "munki-app", munki-app, munki-core, munki-launchd and munki-python would be installed. For future updates, as long as munki-launchd hasn't changed, the updates would happen as unattended installs.  If a future update included an updated munki-launchd, the unattended_install would be invalidated, and a reboot would be needed, meaning the update would either wait until all users were logged out, or for a user to initiate the update via Managed Software Center.

Extracting the component packages from the distribution package might look like:

```bash
#### Expand the distribution package
$ pkgutil --expand munkitools-4.0.1.3899.pkg munkitools_pkg
$ cd munkitools_pkg
$ ls
Distribution				munkitools_core-4.0.1.3899.pkg
munkitools_admin-4.0.1.3899.pkg		munkitools_launchd-3.0.3265.pkg
munkitools_app-5.1.0.3899.pkg		munkitools_no_python-4.0.1.3899.pkg
munkitools_app_usage-4.0.1.3899.pkg	munkitools_python-3.7.4.pkg

#### Convert the expanded subpackages back to flat packages
$ pkgutil --flatten munkitools_admin-4.0.1.3899.pkg ../munkitools_admin-4.0.1.3899.pkg
$ pkgutil --flatten munkitools_app-5.1.0.3899.pkg ../munkitools_app-5.1.0.3899.pkg
$ pkgutil --flatten munkitools_app_usage-4.0.1.3899.pkg ../munkitools_app_usage-4.0.1.3899.pkg
$ pkgutil --flatten munkitools_core-4.0.1.3899.pkg ../munkitools_core-4.0.1.3899.pkg
$ pkgutil --flatten munkitools_launchd-3.0.3265.pkg ../munkitools_launchd-3.0.3265.pkg
#### odds are you don't actually want the no_python pkg, but listed here for completeness ####
$ pkgutil --flatten munkitools_no_python-4.0.1.3899.pkg ../munkitools_no_python-4.0.1.3899.pkg
$ pkgutil --flatten munkitools_python-3.7.4.pkg ../munkitools_python-3.7.4.pkg
$ cd ..
$ ls munkitools_*.pkg
munkitools_admin-4.0.1.3899.pkg		munkitools_launchd-3.0.3265.pkg
munkitools_app-5.1.0.3899.pkg		munkitools_no_python-4.0.1.3899.pkg
munkitools_app_usage-4.0.1.3899.pkg	munkitools_python-3.7.4.pkg
munkitools_core-4.0.1.3899.pkg

#### Import the extracted subpackages we want
$ munkiimport munkitools_admin-4.0.1.3899.pkg
$ munkiimport munkitools_app-5.1.0.3899.pkg
$ munkiimport munkitools_app_usage-4.0.1.3899.pkg
$ munkiimport munkitools_core-4.0.1.3899.pkg
$ munkiimport munkitools_launchd-3.0.3265.pkg
$ munkiimport munkitools_python-3.7.4.pkg
```

#### Easiest approach

The easiest approach is to use AutoPkg: https://github.com/autopkg/autopkg

Once you've installed the Munkitools recipes (hint: `autopkg repo-add recipes`) you can simply do

```
autopkg run munkitools6.munki
```

to import the Munki 6 tools into your Munki repo. This recipe does the hard/tedious work of extracting the component packages and importing them with the correct interdependencies.

### munkitools component packages

| Component             | Identifier                | Notes                                   |
| ----------------------|---------------------------|-----------------------------------------|
| Munki core tools      | com.googlecode.munki.core | Munki's core code and command-line tools |
| Munki admin tools     | com.googlecode.munki.admin | Munki's command-line administration tools |
| Managed Software Center | com.googlecode.munki.app | Munki's user-facing GUI apps and supporting files. |
| Munki launchd agents | com.googlecode.munki.launchd | Munki's LaunchDaemons and LaunchAgents. Requires a restart. |
| Munki app usage monitoring tool | com.googlecode.munki.app_usage | Munki app usage monitoring tool and launchdaemon. If installed Munki can use data collected by this tool to automatically remove unused software. |
| Munki embedded Python | com.googlecode.munki.python | Munki's own Python 3 interpreter. Selected by default. |
| System Python link | com.googlecode.munki.no_python | If you deselect Munki's Python for install, this option becomes available to configure Munki to use Apple's included Python. |

These choices can be also seen if you choose to customize a manual install:

![](https://github.com/munki/munki/wiki/images/munkitools4_pkg.png)

### pkginfo notes for Munki 4 and Munki 5

If you do not use the autopkg recipe to import munkitools packages into your repo, and instead manually import the munkitools distribution package, you need to understand the component packages. By default, the com.googlecode.munki.python component is installed, and the com.googlecode.munki.no_python component is not installed. If you do not indicate that fact in the receipts array in the pkginfo, Munki will always think Munki tools need to be installed since it will see com.googlecode.munki.no_python is not installed each time it checks.

You can remove the com.googlecode.munki.no_python receipt from the receipts array, or just mark it as optional. (See https://github.com/munki/munki/wiki/Supported-Pkginfo-Keys#receipts)

### Conclusion

These techniques should allow for quicker and more seamless updates to Munki tools for your client machines, as in many cases you can update the Munki tools with no user action required.