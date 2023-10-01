## About Munki's Embedded Python

Munki 4 and above embeds its own Python 3 framework and does not rely on Apple's Python installation.

The included framework is created via this [tool](https://github.com/gregneagle/relocatable-python). The Python framework it builds is based on Python.org's 3.8.5 release, and adds PyObjC, xattr, and six to the installed Python modules.

The "embedded" Python framework is installed by default to `/usr/local/munki/Python.framework`.

The command-line tools have their "she-bang" line. This was set to `#!/usr/local/munki/python` in Munki 4 and was changed to `#!/usr/local/munki/munki-python` in Munki 5.1. `/usr/local/munki/munki-python` is a symlink to `Python.framework/Versions/Current/bin/python3`.

This arrangement has a few implications.

If you have your own customized Python 3 you'd like Munki to use, you can replace the symlink at `/usr/local/munki/munki-python` with one pointing to your own Python. You could also decide then to not install Munki's embedded Python at all. Munki's embedded Python is a optional component package within the Munkitools distribution package.

Although this is not recommended, you can also run Munki 4 under Apple's Python 2 -- just replace the `/usr/local/munki/munki-python` symlink with one pointing to `/usr/bin/python` or even `/System/Library/Frameworks/Python.framework/Versions/2.7/bin/python`. Since Munki's Python code has been updated to be compatible with both Python 2 and 3, this works in theory, but there has not been a lot of testing of the updated code against Apple's Python 2.
