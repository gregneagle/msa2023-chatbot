It is possible to use a configuration profile to block the install of Apple updates by non-admins. If your organization does this, once you migrate to Munki 5, your non-admin users may have no way to install Apple updates that require a restart.

There are two preference domains and keys that affect this functionality:

| Preference domain        | Preference key                                    | Type    |
|--------------------------|---------------------------------------------------|---------|
| com.apple.SoftwareUpdate | restrict-software-update-require-admin-to-install | Boolean |
| com.apple.appstore       | restrict-store-require-admin-to-install           | Boolean |

If either is set to true, non-admins will not be able to install Apple updates, nor will they be able to install software from the App Store. Not managing these, or setting them to false, allows non-admins to install from both sources. (Yes, despite the two different preference domains and the names of the keys, these keys appear to function identically and affect both Software Update installs _and_ App Store installs. File bugs with Apple if you think this behavior should change.)

If you want to allow non-admin users to install Apple software updates, but not to install apps from the App Store, the only Apple-supported way to accomplish this would be to not manage either of the above preferences, and to manage `com.apple.appstore` `restrict-store-softwareupdate-only` to True. This will have the result of blocking all use of the App Store, even for admin users.

See also:  
https://developer.apple.com/documentation/devicemanagement/appstore  
https://developer.apple.com/documentation/devicemanagement/softwareupdate