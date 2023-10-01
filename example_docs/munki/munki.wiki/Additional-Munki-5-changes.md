Here are some additional changes in Munki 5 that are less dramatic than the major changes:

* When mounting a disk image prior to an install, Apple's diskimage checksum verification is skipped. Since Munki already does its own checksum verification to ensure the local copy of the file matches that on the server, this speeds up installs without significantly affecting safety/security.

* When installing a major macOS upgrade, `managedsoftwareupdate` now checks for an undocumented nvram variable in an attempt to determine if a BridgeOS update has been staged. If the variable is present and appears to be valid, a shutdown is performed instead of a restart after the macOS upgrade has been staged.

* When the munkitools_app package is installed, preflight and postflight scripts quit and relaunch Managed Software Center.app if needed.