# StopProcessingIf

> **NOTE: This page is automatically generated by GitHub Actions when a new release is tagged.**<br />Updates to the information on this page should be submitted as pull requests to the AutoPkg repository. Processors are located [here](https://github.com/autopkg/autopkg/tree/master/Code/autopkglib).
## Description
Sets a variable to tell AutoPackager to stop processing a recipe if a
    predicate comparison evaluates to true.

## Input Variables
- **predicate:**
    - **required:** True
    - **description:** NSPredicate-style comparison against an environment key. See http://developer.apple.com/library/mac/#documentation/Cocoa/Conceptual/Predicates/Articles/pSyntax.html

## Output Variables
- **stop\_processing\_recipe:**
    - **description:** Boolean. Should we stop processing the recipe?


