If your machines are not running the latest major version of macOS -- for example, at the time of this writing, if your machines are running macOS Mojave -- when your users open the Software Update preferences pane, instead of seeing the updates applicable to the major version of macOS their machine is currently running, instead they may be presented with an "advertisement" to upgrade to the latest major macOS release.

![](https://github.com/munki/munki/wiki/images/macOS-Catalina-Upgrade-Now.png)

Clicking "Upgrade Now" causes the latest "Install macOS" application to be downloaded and launched.

To get to the updates applicable for the currently installed macOS, one must click the blue "More info.." link under an "Other updates are available" message.

This behavior becomes more problematic with Munki 5, since Munki directs users to the Software Update preferences pane to install Apple updates that require a restart. If instead of the updates you want them to install, they see an advertisement to upgrade to the latest macOS, you may find users upgrading their machines before your organization is ready, or doing so in a way that doesn't ensure additional required updates are applied in a timely manner.

If you don't want your users to upgrade to the latest macOS yet (or via the Software Update preferences pane), you currently have two options:

1. Run a script that does `softwareupdate --ignore "macOS Catalina"` (as root/with `sudo`)
1. Run your own internal softwareupdate server (or offer your own softwareupdate catalogs) that don't include the macOS Catalina item.

macOS 10.15.5 and Security Update 2020-003 for macOS Mojave and High Sierra remove the `--ignore` option. It was added back in 10.15.7 (and 10.14.6 with latest security update) for Mac devices enrolled via Apple Business Manager or Apple School Manager. However, macOS Big Sur removed this option again. 

macOS Big Sur 11.x has removed the option to set a custom softwareupdate CatalogURL. 

This means your only remaining option might be user education -- begging them not to click "Upgrade Now" and training them to instead click the "More info..." link to see the updates applicable to the currently installed version of macOS.

(One other option might be to deploy something that blocks the "Install macOS" application from running, but done without care could lead to terrible user experience...)

See also:
* https://lapcatsoftware.com/articles/software-update.html
* https://derflounder.wordpress.com/2019/10/07/preventing-the-macos-catalina-upgrade-advertisement-from-appearing-in-the-software-update-preference-pane-on-macos-mojave/
* https://babodee.wordpress.com/2020/04/16/apple-plans-on-removing-enterprise-options-for-macos-software-update/
