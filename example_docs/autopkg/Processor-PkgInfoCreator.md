# PkgInfoCreator

> **NOTE: This page is automatically generated by GitHub Actions when a new release is tagged.**<br />Updates to the information on this page should be submitted as pull requests to the AutoPkg repository. Processors are located [here](https://github.com/autopkg/autopkg/tree/master/Code/autopkglib).
## Description
Creates an PackageInfo file for a package.

## Input Variables
- **template\_path:**
    - **required:** True
    - **description:** An Info.plist template.
- **version:**
    - **required:** True
    - **description:** Version of the package.
- **pkgroot:**
    - **required:** True
    - **description:** Virtual root of the package.
- **infofile:**
    - **required:** True
    - **description:** Path to the info file to create.
- **pkgtype:**
    - **required:** True
    - **description:** 'flat' or 'bundle'.

## Output Variables


