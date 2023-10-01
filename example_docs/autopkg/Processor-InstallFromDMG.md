# InstallFromDMG

> **NOTE: This page is automatically generated by GitHub Actions when a new release is tagged.**<br />Updates to the information on this page should be submitted as pull requests to the AutoPkg repository. Processors are located [here](https://github.com/autopkg/autopkg/tree/master/Code/autopkglib).
## Description
Calls autopkginstalld to copy items from a disk image to the root
    filesystem.

## Input Variables
- **dmg\_path:**
    - **required:** True
    - **description:** Path to the disk image.
- **items\_to\_copy:**
    - **required:** True
    - **description:** Array of dictionaries describing what is to be copied. Each item should contain 'source\_item' and 'destination\_path', and may optionally include: 'destination\_item' to rename the item on copy, and 'user', 'group' and 'mode' to explicitly set those items.
- **download\_changed:**
    - **required:** False
    - **description:** download\_changed is set by the URLDownloader processor to indicate that a new file was downloaded. If this key is set in the environment and is False or empty the installation will be skipped.

## Output Variables
- **install\_result:**
    - **description:** Result of install request.
- **install\_from\_dmg\_summary\_result:**
    - **description:** Description of interesting results.

