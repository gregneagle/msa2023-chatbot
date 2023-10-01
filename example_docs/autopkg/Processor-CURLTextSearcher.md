# CURLTextSearcher

> **NOTE: This page is automatically generated by GitHub Actions when a new release is tagged.**<br />Updates to the information on this page should be submitted as pull requests to the AutoPkg repository. Processors are located [here](https://github.com/autopkg/autopkg/tree/master/Code/autopkglib).
## Description
Downloads a URL using curl and performs a regular expression match
    on the text.

    Requires version 1.4.

## Input Variables
- **re\_pattern:**
    - **description:** Regular expression (Python) to match against page.
    - **required:** True
- **url:**
    - **description:** URL to download
    - **required:** True
- **result\_output\_var\_name:**
    - **description:** The name of the output variable that is returned by the match. If not specified then a default of "match" will be used.
    - **required:** False
    - **default:** match
- **request\_headers:**
    - **description:** Optional dictionary of headers to include with the download request.
    - **required:** False
- **curl\_opts:**
    - **description:** Optional array of curl options to include with the download request.
    - **required:** False
- **re\_flags:**
    - **description:** Optional array of strings of Python regular expression flags. E.g. IGNORECASE.
    - **required:** False

## Output Variables
- **result\_output\_var\_name:**
    - **description:** First matched sub-pattern from input found on the fetched URL. Note the actual name of variable depends on the input variable "result\_output\_var\_name" or is assigned a default of "match."

