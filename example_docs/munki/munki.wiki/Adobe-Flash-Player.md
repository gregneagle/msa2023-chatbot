### Current Recommendation

Use [AutoPkg](https://autopkg.github.io/autopkg/).

The AdobeFlashPlayer.munki recipe finds the latest Flash Player installer, downloads it, extracts the embedded package, and imports it into your Munki repo.

### Details for those who like extra work

Starting with release 10.1 of Adobe Flash Player, and at least through the current 10.3 releases, the item at the root of the disk image is NOT an Apple package, but rather a wrapper application. 

To use this with munki, open the "Install Adobe Flash Player" application bundle (control-click on the application and choose "Show Package Contents"), navigate to the Resources folder and extract the "Adobe Flash Player.pkg" from this folder.  Wrap it in a disk image to use with munki.

Even better, let `munkiimport` do the hard work for you. Mount the disk image, then:

    /usr/local/munki/munkiimport /Volumes/Flash\ Player/Install\ Adobe\ Flash\ Player.app/Contents/Resources/Adobe\ Flash\ Player.pkg

(You might have to alter the path if the disk image mounts under another name.)

Later releases of Flash Player made this trickier, as the promoted download was often an app that did *not* have an embedded package. If you signed up for a "Flash Player Distribution Agreement" with Adobe, you'd be given a URL that pointed to a download that did contain the embedded package.