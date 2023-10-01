In Munki 5, if one or more updates has been pending for a long time (the default is 14 days), when `managedsoftwareupdate` triggers Managed Software Center to notify about pending updates, the app will switch to a mode that makes it difficult to ignore.

![](https://github.com/munki/munki/wiki/images/munki5-9.png)

In this mode:
* Only the Updates tab/view is available in Managed Software Center
* Access to the Command-Tab task switcher and Dock is removed
* The ability to click other applications to switch to them is blocked
* Other apps appear "grayed out"/disabled
* Force-quit is blocked
* Several other items in the Apple menu are disabled

The user is highly encouraged to interact with Managed Software Center.app. The rest of the behavior is as described in  [Additional update encouragement](additional-update-encouragement-in-munki-5).