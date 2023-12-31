# SparkleUpdateInfoProvider

> **NOTE: This page is automatically generated by GitHub Actions when a new release is tagged.**<br />Updates to the information on this page should be submitted as pull requests to the AutoPkg repository. Processors are located [here](https://github.com/autopkg/autopkg/tree/master/Code/autopkglib).
## Description
Provides URL to the highest version number or latest update.

## Input Variables
- **appcast\_url:**
    - **required:** True
    - **description:** URL for a Sparkle Appcast feed xml.
- **appcast\_request\_headers:**
    - **required:** False
    - **description:** Dictionary of additional HTTP headers to include in request.
- **appcast\_query\_pairs:**
    - **required:** False
    - **description:** Dictionary of additional query pairs to include in request. Manual url-encoding isn't necessary.
- **alternate\_xmlns\_url:**
    - **required:** False
    - **description:** Alternate URL for the XML namespace, if the appcast is using an alternate one. Defaults to that used for 'vanilla' Sparkle appcasts.
- **curl\_opts:**
    - **required:** False
    - **description:** Optional array of options to include with the download request.
- **pkginfo\_keys\_to\_copy\_from\_sparkle\_feed:**
    - **required:** False
    - **description:** Array of pkginfo keys that will be derived from any available metadata from the Sparkle feed and copied to 'additional\_pkginfo'. The usefulness of these keys will depend on the admin's environment and the nature of the metadata provided by the application vendor. Note that the 'description' is usually equivalent to 'release notes' for that specific version. Defaults to ['minimum\_os\_version']. Currently supported keys: description, minimum\_os\_version
- **urlencode\_path\_component:**
    - **required:** False
    - **description:** Boolean value to specify if the path component from the sparkle feed needs to be urlencoded. Defaults to True.
- **update\_channel:**
    - **required:** False
    - **description:** Sparkle 2 provides specifying what channel an update is on. You can specify which channel to look for via this key. If a channel is defined, and exists, then this defined channel will be used.
- **PKG:**
    - **required:** False
    - **description:** Local path to the pkg/dmg we'd otherwise download. If provided, the download is skipped and we just use this package or disk image.

## Output Variables
- **url:**
    - **description:** URL for a download.
- **version:**
    - **description:** Version for the download extracted from the feed. This is a human-readable version if the feed has it (e.g., 2.3.4-pre4), and the basic machine-readable version (e.g., 823a) otherwise.
- **additional\_pkginfo:**
    - **description:** A pkginfo containing additional keys extracted from the appcast feed. Currently this is 'description' and 'minimum\_os\_version' if it was defined in the feed.


