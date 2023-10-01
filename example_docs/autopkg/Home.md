# Introduction

AutoPkg is an automation framework for macOS software packaging and distribution, oriented towards the tasks one would normally perform manually to prepare third-party software for mass deployment.

These tasks typically involve at least several of the following steps:

* downloading an application and/or updates for it, usually via a web browser
* extracting them from a multitude of archive formats
* adding site-specific configuration
* adding sane versioning information
* "fixing" poorly-written installer scripts
* saving these modifications back to a compressed disk image or installer package
* importing these into a software distribution system like Munki, Jamf Pro, FileWave, etc.
* customizing the associated metadata for such a system with site-specific data, post-installation scripts, version info or other metadata

Often these tasks follow similar patterns for each individual application, and when managing many applications this becomes a daily task full of sub-tasks that one must remember (and/or maintain documentation for) about exactly what had to be done for a successful deployment of every update for every managed piece of software.

A goal of AutoPkg is to be able to define these steps in a "Recipe", which can be defined in an understood (plist or yaml) format, run automatically instead of by hand, and shared with others.
