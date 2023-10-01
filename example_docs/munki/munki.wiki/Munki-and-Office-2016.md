# Munki and Office 2016

> ***
Here is very in-depth information that may supersede some of the information below:  
https://clburlison.com/demystify-office2016/ (Published 04 Jan 2016)
***
Microsoft had significant issues early in their release process for 2016, but have been responsive and addressed many of the common ones. This page may change to reflect updates in the future.
***

With Office 2016, Microsoft has made significant changes to how Office is packaged and deployed. The individual apps are now sandboxed and can be deployed individually. Additionally, there are now 2 ways you can purchase/license Office 2016:
 * Traditional Volume-licensed model
 * Office 365 Subscription

## Volume-licensed customers

As done previously, Office 2016 is available as a traditional volume-licensed installer. This is downloadable as an ISO image from Microsoft's Volume-license portal. The volume-license installer is suitable for deployment via Munki as of version 15.13.4 without changes, otherwise you'd need to use a custom [ChoiceChangesXML](ChoiceChangesXML) to exclude the specific volume licensing package from it. Some are also excluding the Microsoft AutoUpdate installer so there isn't a first-launch prompt asking to also launch the associated daemon, since Munki will be handling those updates.

Some have found that they prefer to install AND update Office 2016 via Munki by using [AutoPkg](https://github.com/autopkg/autopkg) and the collection of Office 2016 recipes available in the main autopkg [recipes](https://github.com/autopkg/recipes/tree/master/MSOfficeUpdates) repo subdirectory. These recipes package and import the individual Office apps by pulling the "updates" directly from Microsoft. (As of 15.19.1 'deltas' are also available, but there are 'internal' tracks that Microsoft would like you to test by manually running MAU - more info here:.) Minus some shared fonts that could be left out for languages you may not need, the only component definitely needed from the volume-license installer was your actual volume license file (which would be present at `/Library/Preferences/com.microsoft.office.licensingV2.plist`). As of the 15.17.1 version of the volume license, the download includes a package that can serialize a disk, which should be used instead of other methods, and works with either the SKU-Less or 'Standalone' installer versions. The Office 2016 recipes are:

 * MSExcel2016.munki
 * MSWord2016.munki
 * MSPowerpoint2016.munki
 * MSOneNote2016.munki
 * MSOutlook2016.munki

## Office 365 customers

If the Office updates (detailed above) are deployed to a system without installing the licensing file, the first Office 2016 app opened will prompt the user to log in to Office 365. Each additional app launched may prompt the end user to access the credentials in the keychain set by the first licensed app, but in any case Munki has no additional work to perform.

## SKU-Less
Additionally, SKU-less versions of the suite (which can be used with either flavor of licensing), can be found (along with other helpful info) at [macadmins.software](http://macadmins.software)