New in Munki 6.1 is support for "default_installs" in a manifest:

```xml
<key>default_installs</key>
<array>
   <string>GoogleChrome</string>
   <string>Firefox</string>
   <string>MicrosoftWord</string>
   <string>MicrosoftExcel</string>
</array>
```

This feature is intended for environments where it is useful to offer a set of commonly-used apps as installed by default, but also give the end-user the option of removing these items if they do not use them.

When `managedsoftwareupdate` runs, if it finds any `default_installs`, it checks to see if they have already been added to the local SelfServeManifest under the `default_installs` key. If they have not, they are  added to the local SelfServeManifest, under the `default_installs` key _and also_ under the `managed_installs` key.

The SelfServiceManifest is processed as normal, and any items in `managed_installs` are ensured installed. But since this is the SelfServeManifest, the end-user can use Managed Software Center to cancel the installation of an item (before it is actually installed, or remove it (after it has been installed).

If they cancel or remove it, it will be removed from the SelfServiceManifest’s `managed_installs`. On a subsequent `managedsoftwareupdate` run, Munki will see the item was already added to `default_installs` in the SelfServeManifest, and so will not re-add it to the `managed_installs` of that same manifest.

Note the items in `default_installs` must also exist in `optional_installs` — they are simply a set of optional install items that will be installed by default. So in the above example, GoogleChrome, Firefox, MicrosoftWord, and MicrosoftExcel must also exist in `optional_installs`.