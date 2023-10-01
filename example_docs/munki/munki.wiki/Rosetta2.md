## Introduction
When managing Apple silicon Macs, it's a common need to ensure that the Rosetta2 Intel translation software is installed in order to run software that has not been re-compiled into native arm64 code.

## nopkg

Consider using this [nopkg](nopkgs) item:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>autoremove</key>
    <false/>
    <key>catalogs</key>
    <array>
      <string>production</string>
    </array>
    <key>category</key>
    <string>Systems Administration</string>
    <key>description</key>
    <string>Install's Apple's Rosetta2 Intel instruction translation software for Apple silicon</string>
    <key>developer</key>
    <string>Apple</string>
    <key>display_name</key>
    <string>Rosetta translation software</string>
    <key>installcheck_script</key>
    <string>#!/bin/sh

if [ $(/usr/bin/arch) == "arm64" ] ; then
    if ! /usr/bin/arch -x86_64 /usr/bin/true 2&gt;/dev/null ; then
        /usr/sbin/softwareupdate --install-rosetta --agree-to-license
    fi
fi
exit 1
    </string>
    <key>installer_type</key>
    <string>nopkg</string>
    <key>minimum_os_version</key>
    <string>11.0</string>
    <key>name</key>
    <string>InstallRosetta2</string>
    <key>unattended_install</key>
    <true/>
    <key>unattended_uninstall</key>
    <false/>
    <key>uninstallable</key>
    <false/>
    <key>version</key>
    <string>1.0</string>
  </dict>
</plist>
```

The installcheck_script deserves some additional explanation:

```bash
#!/bin/sh

if [ $(/usr/bin/arch) == "arm64" ] ; then
    if ! /usr/bin/arch -x86_64 /usr/bin/true 2>/dev/null ; then
        /usr/sbin/softwareupdate --install-rosetta --agree-to-license
    fi
fi
exit 1
```

The first if statement checks to see if we're running on Apple silicon; if not, we skip to the end.
The second if statement attempts to run the x86_64 (Intel) code for `/usr/bin/true`. If Rosetta2 is not installed, that will fail and be evaluated as false; the ! character is a negation or NOT operator, so the statement as a whole would be evaluated as true, leading to an attempt to install Rosetta. If Rosetta _is_ installed, running the x86_64 code for `/usr/bin/true` will _succeed_ and the entire statement will be evaluated as false, skipping the attempted install of Rosetta.

Since this nopkg item only installs Rosetta on Apple silicon, and only attempts to install it if it's not already present, this item is safe to put in managed_installs for all machines running macOS 11 or later. It will also re-install Rosetta if it somehow gets removed (there have been some reports or Rosetta disappearing during a macOS update).

The installcheck_script always exits 1 to indicate no need to install since the actual installation (if needed) is taken care of during the installcheck_script. This means that Rosetta2 will be installed before any packages are installed during the "normal" install phase, which is arguably a good thing. If this bothers you, you could replace the installcheck_script with something like

```bash
#!/bin/sh

if [ $(/usr/bin/arch) == "arm64" ] ; then
    if ! /usr/bin/arch -x86_64 /usr/bin/true 2>/dev/null ; then
        # exit 0 to indicate we need to install
        exit 0
    fi
fi
# exit non-zero to indicate no need to install
exit 1
```

and then add an postinstall_script like so: 

```bash
#!/bin/sh

/usr/sbin/softwareupdate --install-rosetta --agree-to-license
```

This alternate approach is untested by the author.