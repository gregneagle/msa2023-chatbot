## Introduction
In macOS Big Sur, the `profiles` command can no longer be used to install configuration profiles. This removes the ability for Munki to install configuration profiles. You should, as much as is possible, move to using MDM to install and manage your configuration profiles for macOS. But there are some scenarios where it would be useful to have _some_ support for managed preferences in Munki.

## Scenarios

* Scenario 1: you have configuration profiles that manage preferences for a specific piece of software. You used update_for relationships to cause Munki to install the appropriate configuration profile for Foo when Foo is installed, and to remove the configuration profile for Foo when Foo is removed. Most MDM solutions do not provide a good replacement for this functionality. One option is to just install the configuration profiles on all machines, regardless if the related software is installed or not. But this can cause other issues. If a preference that is managed is related to licensing, you may have now just "licensed" every machine in your org. If you haven't purchased licenses for everyone, that could be a problem. Also, if every machine has the profile installed, it means that _manual_ installs of the software will also have their preferences managed. This may or may not be desired.

* Scenario 2: Chicken-and-egg -- in our org, user accounts are in LDAP. We configure our machines to use our LDAP server as a directory source. When a user logs into a Mac, a mobile account is created using the LDAP attributes. This means that both the LDAP configuration and the managed preferences that cause mobile accounts to be created must be in place before the first user login. This presents a problem when "bootstrapping" a machine, as enrolling into MDM generally requires logging into a user account. If you don't want to have to create a "throwaway" account, you need to have the right configuration bits in place _before_ the first attempted user login.

## Implementation

To emulate profile installs, configuration profiles are read, and if they contain managed preferences, they are converted to MCX data that is added to a ComputerGroup in the local Open Directory store. Configuration profile payloads that are not managed preferences are ignored/skipped.

The created ComputerGroup name is the profile identifier.

To delete one of these emulated profiles, the ComputerGroup is simply deleted.

## Enabling support

Since this feature/implementation is a bit of a hack and not supported by Apple, it is disabled by default, and Munki will not attempt to emulate configuration profiles in Big Sur. To enable this feature, set EmulateProfileSupport to true in Munki's preferences. (To avoid the chicken-and-egg scenario here, that might take the form of using `defaults write /Library/Preferences/ManagedInstalls EmulateProfileSupport -bool YES` or otherwise managing /Library/Preferences/ManagedInstalls.plist)