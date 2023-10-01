_Some pointers on repackaging software_

### Introduction

Munki can install software distributed in Apple package format, from "drag-n-drop" disk images, and software "packaged" with Adobe CS3/4/5/6/CC Enterprise Deployment tools.

But some software may have to be repackaged in order to be installed by Munki. Some examples of types of software that may need to be packaged or repackaged:

- Software distributed in InstallVISE or InstallAnywhere format.
- Software distributed in Apple package format, but the package doesn't work silently or at the loginwindow.
- Software you develop yourself that isn't packaged at all

Generally speaking, you should avoid repackaging software unless there is no choice. If you repackage, you accept responsibility for any issues your non-vendor-supported installer might create.

### Details

#### Tools

Here are some useful tools for creating Apple Installer packages. This is not an exhaustive list; there are other tools available. These are either ones I've used personally, or can recommend for other reasons.

**AutoPkg**

https://github.com/autopkg/autopkg

AutoPkg is an automation tool that runs recipes to automate the tasks of finding, downloading and preparing software for mass deployment. Some of the available recipes do repackaging of some problematic software; if you need to repackage, consider first looking for an AutoPkg recipe that does it for you.

Some notes on using AutoPkg as a general-purpose packaging tool:  
https://managingosx.wordpress.com/2015/07/30/using-autopkg-for-general-purpose-packaging/

**munkipkg**

https://github.com/munki/munki-pkg

munkipkg is a simple tool for building packages in a consistent, repeatable manner from source files and scripts in a project directory.

Files, scripts, and metadata are stored in a way that is easy to track and manage using a version control system like git.

**pkgbuild and productbuild**

Command-line tools for building packages. Installed by default on OS X 10.7 and up. See their man pages for more information.

Pros: universally available. Supported by Apple. Easy to integrate into automated workflows.

Cons: command-line only, so requires some mental work to get started.

**Packages**

http://s.sudre.free.fr/Software/Packages.html

Modern packaging tool from the creator of Iceberg. Recommended as a GUI tool to build flat packages.

**Jamf Composer**

https://www.jamf.com/products/jamf-composer/

Composer is one of the macOS tools included with Jamf Pro, but it is also available separately from Jamf for USD $100 (an educational discount is available). Composer can create packages using a number of methods, most notably by comparing filesystem snapshots or by monitoring file system events. It can also create installation packages with extra abilities when used with Jamf Pro, such as installing default preferences into users' home directories. If you want to edit an existing package, Composer can import it for editing and repackaging.

Pros: Easy to use. Good documentation.

Cons: It's not free. Composer's special package features work only with Jamf Pro.

### Commandments of (re)packaging

These are old, but still hold some relevance if you do need to re-package someones software, or indeed for Vendors learning how to package their tools for macOS:

https://wiki.afp548.com/index.php/Guidelines_for_Mac_software_packaging#The_Commandments_of_Packaging