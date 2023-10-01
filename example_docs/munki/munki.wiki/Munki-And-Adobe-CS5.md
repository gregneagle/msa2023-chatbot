### Introduction

Version 0.6.0.640.0 of the munki tools supports deployment of Adobe CS5 products packaged using the Adobe Application Manager, Enterprise Edition (AAMEE). munki attempts to work around some of the outstanding issues with AAMEE 1.0-generated packages.

### Summary

To deploy an Adobe CS5 or CS5.5 product with Munki, package the product using AAMEE 2.1, available [here](http://www.adobe.com/devnet/creativesuite/enterprisedeployment.html). You should not need to disable Adobe Air components. Do not add any Adobe updates to the package.

Use munkiimport to import the generated CS5Product_Install.pkg. You do not need to import the CS5Product_Uninstall.pkg.

Adobe CS5/5.5 updates downloaded from adobe.com can be directly imported into Munki -- do not repackage them with AAMEE.

### Details

With the release of the Adobe CS5 products, Adobe has also introduced a new Enterprise Deployment Toolkit, which they've named "AAMEE" (Adobe Application Manager, Enterprise Edition). This new toolkit allows administrators to create Apple package installers from Adobe CS5 media. While this works, and the resulting packages can be used with munki, there are a few outstanding issues:

1. The packages cannot be installed when there is no user logged into the GUI; the install hangs while attempting to install Adobe Help or Adobe Media Player, both Adobe AIR-based applications. This is an issue Adobe is working on.
2. The "package" is actually a payload-free package with a preinstall/preupgrade script that is a wrapper around updated versions of the same Adobe install tools that shipped with CS3 and CS4. As a result of this design, Apple's Installer has no way to give useful or accurate installation progress feedback. The Installer will display "About a minute remaining..." for many, many minutes - up to an hour in some cases.
3. AAMEE-generated packages will fail when you attempt to install them from a mounted disk image. This is a problem because munki requires all bundle-style packages to be wrapped in a disk image so they can be stored and retrieved as a single file from the munki web server.
munki 0.6.0.640.0 has workarounds for all of these issues.

For the first issue, munki calls the Adobe installer using launchctl bsexec <PID_of_loginwindow> if the install is does in the loginwindow context, and monitors the install. If the install hangs on an Adobe AIR or Adobe Help install, that part of the install is killed, allowing the larger install to progress. In practice, it appears that using launchctl bsexec <PID_of_loginwindow> results in successful installation of Adobe AIR/Adobe Help in most cases.

The second issue is worked around by monitoring the install log and using that to provide percent-done feedback. An identical technique is used by munki for CS3/CS4 installs. This technique is not 100% accurate, but at least provides approximate progress feedback.

Finally, the third issue is addressed by creating some symlinks on the local disk pointing back to resources on the mounted disk image. This fools the Adobe installer into thinking the installation payloads are on a non-removable disk, and it proceeds with installation.

To use an AAMEE-1.0-generated installer package with munki, create the pacakge using the "final" 1.0 release of AAMEE, or a later release. Do not use the "preview" release or any pre-release version of the AAMEE tool.

Use munkiimport to import the AAMEE-generated install package into your Munki server.

Alternately, wrap the installation package in a disk image. Copy it to your munki web server as you would any other package, and run makepkginfo on it like any other package. makepkginfo will also encapsulate the info needed for an uninstall, so there is no need to wrap or upload the uninstall package.

**AAMEE 2.0 notes**

AAMEE 2.0, released to support Adobe Creative Suite 5.5, adds support for including product updates in the installer package. Munki does nor currently handle AAMEE packages with included updates correctly. Do not include product updates in packages built with AAMEE 2.0. You may instead manage product updates separately in Munki.