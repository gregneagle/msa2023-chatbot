## Munki 4

Munki 4 is a major release of the Munki tools.

All of the command-line tools have been converted to be compatible with Python 3, and a Python 3 interpreter is included with Munki 4. This is a major architectural change for Munki, and so the major version has been incremented to help bring attention to this.

Functionality for the initial release is intended to be identical to that of Munki 3.6. There are currently no changes in the GUI tools between the current 3.6.x release and the planned initial Munki 4 release.

### Repo plugins and middleware
If you use custom [[Repo Plugins]] or [[Middleware]], do not upgrade to Munki 4 until you have verified these plugins are compatible with Python 3 and Munki 4.

### What happened to Munki 3.7?
The first few betas were released as Munki 3.7 betas before the decision was made to number this release as 4.0.

## More information:

* [[About Munki's Embedded Python]]
* [[Customizing Python for Munki]]
* [[Upgrading to Munki 4]]
