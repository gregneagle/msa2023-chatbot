_Allowing the installation of packages signed with untrusted or expired certificates_

### Introduction
Munki 3 supports optionally allowing the installation of packages signed with untrusted or expired certificates.

### Background
Apple installer packages can be (and often are) signed by their creator, to ensure that the contents have not been tampered with. Apple's `installer` by default will refuse to install packages with invalid or untrusted signatures. A package that was signed without the use of a trusted timestamp will also refuse to validate if any of the certificates in the signing chain have expired. This can mean that a package Munki would happily install this week will now fail to install because a cert has expired.

A `managedsoftwareupdate` session with such an expired package might look like this:
```
$ sudo managedsoftwareupdate --installonly
Managed Software Update Tool
Copyright 2010-2017 The Munki Project
https://github.com/munki/munki

Starting...
Installing Adobe Photoshop Lightroom (1 of 2)...
    Mounting disk image Lightroom_5_LS11_mac_5_7-5.7-0.0.dmg...
    Install of Adobe Photoshop Lightroom 5.pkg failed with return code 1...
ERROR: ------------------------------------------------------------------------------
ERROR: installer: Package name is Adobe Photoshop Lightroom 5.7
ERROR: installer: Certificate used to sign package is not trusted. Use -allowUntrusted to override.
ERROR: ------------------------------------------------------------------------------
```

We can examine the package signature:
```
$ pkgutil --check-signature /Volumes/Lightroom\ 5.7/Adobe\ Photoshop\ Lightroom\ 5.pkg 
Package "Adobe Photoshop Lightroom 5.pkg":
   Status: signed by a certificate that has since expired
   Certificate Chain:
    1. Developer ID Installer: Adobe Systems, Inc.
       SHA1 fingerprint: 9D 75 C9 20 01 4A 65 04 94 A7 63 95 E3 91 93 47 04 E8 57 DF
       -----------------------------------------------------------------------------
    2. Developer ID Certification Authority
       SHA1 fingerprint: 3B 16 6C 3B 7D C4 B7 51 C9 FE 2A FA B9 13 56 41 E3 88 E1 86
       -----------------------------------------------------------------------------
    3. Apple Root CA
       SHA1 fingerprint: 61 1E 5B 66 2C 59 3A 08 FF 58 D1 4A E2 24 52 D1 98 DF 6C 60
```

And as expected, we see "Status: signed by a certificate that has since expired".

Traditionally, the Munki admin had two options when this situation occurred: get an updated package from the vendor, or when that was not possible, [strip the signature from the expired package](https://managingosx.wordpress.com/2012/03/24/fixing-packages-with-expired-signatures/). (Apple's `installer` will happily install unsigned packages.) This latter approach can be a lot of work.

### Another solution
Munki 3 will support an optional key added to the pkginfo for Apple package installer items.
```xml
<key>allow_untrusted</key>
<true/>
```
Adding `allow_untrusted` = True to a pkginfo for an Apple package installer item will cause Munki to add the `-allowUntrusted` option when using `/usr/sbin/installer` to install a package. From `man installer`:
```
-allowUntrusted
       Allow install of a package signed by an untrusted (or expired) certificate.
```

With this new feature, and with the proper key and value added to the pkginfo for Lightroom 5.7, the `managedsoftwareupdate` session now looks like this:
```
$ sudo managedsoftwareupdate --installonly
Managed Software Update Tool
Copyright 2010-2017 The Munki Project
https://github.com/munki/munki

Starting...
Installing Adobe Photoshop Lightroom (1 of 1)...
    Mounting disk image Lightroom_5_LS11_mac_5_7-5.7-0.0.dmg...
    Preparing for installation…
    Preparing the disk…
    Preparing Adobe Photoshop Lightroom 5.7…
<snip>
    97.2625 percent complete...
    Registering updated applications…
    97.75 percent complete...
    Running installer actions…
    Finishing the Installation…
    100.0 percent complete...
    The software was successfully installed.
```
Munki has successfully installed a package with an expired signature.