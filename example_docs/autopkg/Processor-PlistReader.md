# PlistReader

> **NOTE: This page is automatically generated by GitHub Actions when a new release is tagged.**<br />Updates to the information on this page should be submitted as pull requests to the AutoPkg repository. Processors are located [here](https://github.com/autopkg/autopkg/tree/master/Code/autopkglib).
## Description
Extracts values from top-level keys in a plist file, and assigns to
    arbitrary output variables. This behavior is different from other
    processors that pre-define all their possible output variables.
    As it is often used for versioning, it defaults to extracting
    'CFBundleShortVersionString' to 'version'. This can be used as a replacement
    for both the AppDmgVersioner and Versioner processors.

    Requires version 0.2.5.

## Input Variables
- **info\_path:**
    - **required:** True
    - **description:** Path to a plist to be read. If a path to a bundle (ie. a .app) is given, its Info.plist will be found and used. If the path is a folder, it will be searched and the first found bundle will be used. The path can also contain a dmg/iso file and it will be mounted.
- **plist\_keys:**
    - **required:** False
    - **default:**
        - **CFBundleShortVersionString:** version
    - **description:** ('Dictionary of plist values to query. Key names should match a top-level key to read. Values should be the desired output variable name. Defaults to: ', "{'CFBundleShortVersionString': 'version'}")

## Output Variables
- **plist\_reader\_output\_variables:**
    - **description:** Output variables per 'plist\_keys' supplied as input. Note that this output variable is used as both a placeholder for documentation and for auditing purposes. One should use the actual named output variables as given as values to 'plist\_keys' to refer to the output of this processor.


