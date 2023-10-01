### Introduction

An overview of deploying Mac App Store applications using Munki.

### Details

This is technical advice, not legal advice. Make sure you are complying with vendor agreements and have purchased the appropriate number of licenses for the software you wish to deploy.

Basic steps:

1. Purchase one or more licenses for an application from the App Store under an institutional AppleID.
1. Download the application (using the institutional AppleID) on a Mac with the Munki admin tools installed.
1. Import the application into your Munki repo using `munkiimport /Applications/Foo.app`, where "/Applications/Foo.app" is the path to the downloaded/purchased application.
1. Deploy the application using Munki the same way as any other application.

When there are updates for the application, repeat steps 2-4 above.

This technique will work for applications that do not do App Store receipt validation. For applications that do App Store receipt validation, you'll need to use something other than Munki to distribute these applications.

Related links:

https://support.apple.com/kb/HT5061<br>
https://support.apple.com/kb/ht4781<br>
https://support.apple.com/kb/HT4831

VPP and Managed Distribution:

https://www.apple.com/business/vpp/<br>
https://www.apple.com/education/it/vpp/


**Q: How do I know if an application does App Store receipt validation?**<br>
**A:** I don't know how to tell in advance. You'll know when you try to deploy it and it asks for authorization and refuses to run on deployed machines!