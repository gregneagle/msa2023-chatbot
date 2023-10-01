# What is a nopkg?
A nopkg is a pkginfo item that isn't associated with a .pkg, .dmg, or .mobileconfig "installer." Typically nopkgs will have an installcheck_script to see if the item is "installed" or not, and then will run a postinstall_script if the item is not "installed."

# How does a nopkg differ from a payload-free .pkg?
A payload-free .pkg will leave a receipt (as a normal .pkg would, too) indicating it ran/installed, and it can be deployed via methods other than Munki. So if you can see yourself running a script once and/or using it in non-Munki contexts, you may want to use a payload-free .pkg.

A nopkg, with every Munki run on the client, will keep checking to see if the "installed" state has changed and then will run the script again if necessary.

## How do you make a nopkg?
One way to make one is to create an installcheck_script, a postinstall_script, and an uninstall_script, and then run this command:

```bash
makepkginfo --nopkg --name=NAMEOFYOURNOPKG \
  --pkgvers=1.0 --installcheck_script=/PATH/TO/installcheck_script \
  --postinstall_script=/PATH/TO/postinstall_script \
  --uninstall_script=/PATH/TO/uninstall_script \
  --unattended_install > NAMEOFYOURNOPKG.pkginfo
```

You can then copy that .pkginfo into your Munki repo's pkgsinfo directory and run `makecatalogs`.

## Can I use an installs array instead of an installcheck_script?
Yes. Munki will use [its normal logic to determine whether an item is installed or not](https://github.com/munki/munki/wiki/How-Munki-Decides-What-Needs-To-Be-Installed), and that logic could be an installcheck_script or an installs array.

## Do I need an uninstall_script?
Only if you need to be able to undo what the "install" of the nopkg does. If you don't, you can leave off the uninstall_script. Make sure to mark the item with uninstallable = true.

## What are some examples of uses for a nopkg?
Here are a few examples:

[PrinterGenerator](https://github.com/nmcspadden/PrinterGenerator/blob/master/AddPrinter-Template.plist)

[Timed SuppressUserNotification](https://github.com/aysiu/munkiscripts/blob/master/nopkg/SuppressUserNotification.pkginfo)

[Controlling SSH Access](https://scriptingosx.com/2014/12/control-ssh-access-with-munki-nopkg-scripts/)