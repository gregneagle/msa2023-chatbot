_Adding additional metadata for use with Apple Software Updates_

### Introduction

Munki supports admin-provided additional metadata for Apple Software Updates.

By specifying additional metadata, admins can allow an Apple Software Update to be installed in an unattended manner, force an install after a given date, or override the `display_name`, `description`, `RestartAction` and/or array of `blocking_applications`.

### Details

Read more about Munki's support for installing Apple software updates here: [Apple Software Updates With Munki](/munki/munki/wiki/Apple-Software-Updates-With-Munki)

**This additional metadata does not and can not influence what updates are offered by Apple Software Update -- it can only provide additional information for Munki to use when displaying and installing available updates.**

Pkginfo items created for this purpose (providing additional Apple software update metadata) **should never be added to any manifest.** Think instead of the list of available Apple software updates as a dynamically generated manifest. If an update is offered by Apple Software Update (and therefore in this virtual Apple update manifest), Munki will check for an apple_update_metadata item with the same name as the update's ProductKey.

#### Identifying Updates

Apple Software Update items are uniquely identified by their ProductKey. You can find the ProductKey in a Reposado product listing, or by getting detail on an update using Apple's Software Update Service.

Some recent versions of OS X/macOS also record the product keys for pending updates in /Library/Preferences/com.apple.SoftwareUpdate.plist under 'RecommendedUpdates'.

You may also browse the contents of /Library/Updates.

Finally, you might find this tool useful: [https://github.com/hjuutilainen/sus-inspector](https://github.com/hjuutilainen/sus-inspector)

Here's an example of using Reposado to find ProductKeys for iTunes:

```bash
% ./repoutil --products | grep iTunes
061-3453        iTunes Producer                                    1.6        2007-11-29  (Deprecated)
041-5144        iTunes Producer                                    2.6.0      2012-03-28  (Deprecated)
zzzz041-6245    iTunes                                             10.6.3     2012-10-11  
041-8613        iTunes Producer                                    2.8.0      2012-11-05  (Deprecated)
zzzz041-9793    iTunes                                             11.0.2     2013-02-21  
zzzz041-9792    iTunes                                             11.0.2     2013-02-21  
041-8900        iTunes Producer                                    2.9.0      2013-03-06  
```

The ProductKey is displayed in the first column of the Product listing.

Munki uses the ProductKey as the "name" of the update.

#### Supported additional metadata keys:

```
  blocking_applications
  description
  display_name
  force_install_after_date
  unattended_install
  RestartAction
```

#### Creating Apple Update Metadata pkginfo:

Both `makepkginfo` and `munkiimport` can use a new option: `--apple-update`, which is intended to accept an Apple update `productKey`.  Let's use the recent iTunes 11.0.2 update as an example:

```bash
$ makepkginfo --apple-update zzzz041-9597 --unattended_install --catalog=testing
```
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>catalogs</key>
    <array>
        <string>testing</string>
    </array>
    <key>installer_type</key>
    <string>apple_update_metadata</string>
    <key>name</key>
    <string>zzzz041-9597</string>
    <key>unattended_install</key>
    <true/>
    <key>version</key>
    <string>1.0</string>
</dict>
</plist>
```

If an update has 2 ProductKeys such as the 11.0.2 iTunes update, you should make a separate pkginfo file for each ProductKey.

You may also use `munkiimport`; `munkiimport` will then upload the created pkginfo into your repo.

Again, you should never add the name of an apple_update_metadata item to any Munki manifest.