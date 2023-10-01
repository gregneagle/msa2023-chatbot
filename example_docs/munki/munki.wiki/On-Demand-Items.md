As of version 2.3, Munki has support for on-demand user installation/execution of certain self-service items. When an item marked as supporting "OnDemand" install is included in the list of optional_installs, an end-user can install/execute this item whenever they wish, and as often as they'd like -- in other words, installing/running such an item does not cause the item to be classified as "installed". This can be useful to allow users to run scripts that perform maintenance tasks that normally require elevated privileges, or would otherwise be desirable to pre-program as a workflow that guides the end user through.

If the "OnDemand" key is present and set to True:
1. The item is never considered installed--this means Munki will never think it needs to be removed, either (because it's not installed)
1. If you add such an item to a regular manifest:
    * In managed_installs: Munki will try to install the item over and over and over (since it is never considered installed)
    * In managed_updates: It will never be updated (since it is never considered installed)
    * In managed_uninstalls: It will never be removed (since it is never considered installed)
    * In optional_installs: The only functional choice
1. If chosen by the user for optional install, the item will be installed and then removed from the local SelfServeManifest--thus making it available for a future re-install

To illustrate one possible workflow around adding an OnDemand item, please see the use case documented by Shea Craig:
https://sheagcraig.github.io/configuring-and-reconfiguring-the-default-mail-reader-self-service-through-munki-and-a-tale-of-woe/