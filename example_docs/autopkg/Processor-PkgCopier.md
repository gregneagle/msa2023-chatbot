# PkgCopier

> **NOTE: This page is automatically generated by GitHub Actions when a new release is tagged.**<br />Updates to the information on this page should be submitted as pull requests to the AutoPkg repository. Processors are located [here](https://github.com/autopkg/autopkg/tree/master/Code/autopkglib).
## Description
Copies source\_pkg to pkg\_path.

## Input Variables
- **source\_pkg:**
    - **required:** True
    - **description:** Path to a pkg to copy. Can point to a path inside a .dmg which will be mounted. This path may also contain basic globbing characters such as the wildcard '\*', but only the first result will be returned.
- **pkg\_path:**
    - **required:** False
    - **description:** Path to destination. Defaults to RECIPE\_CACHE\_DIR/os.path.basename(source\_pkg)

## Output Variables
- **pkg\_path:**
    - **description:** Path to copied pkg.
- **pkg\_copier\_summary\_result:**
    - **description:** Description of interesting results.

