### Introduction

Info on installing and removing Adobe CS6 products with Munki.

### Details

Munki can treat Adobe CS6 deployment packages generated with AAMEE 3 exactly the same as CS5/5.5 deployment packages.

See [Adobe CS5](Munki And Adobe CS5) for details.

Abbreviated version:

1. Use AAMEE 3 (available [here](http://www.adobe.com/devnet/creativesuite/enterprisedeployment.html)) to package your Adobe CS6 product. You should not need to disable Adobe AIR components.
2. Use munkiimport to import the CS6Product_Install.pkg. You do not need the CS6Product_Uninstall.pkg.

#### CS6 Updates

Do not repackage CS6 updates using AAMEE. Simply use munkiimport to import the diskimage as downloaded from Adobe.