## Customizing Python for Munki

Munki 4+ ships with its own Python 3 interpreter, currently based on the Python.org 3.8.5 release, and adding some additional modules to allow calling Apple's Cocoa frameworks. The additional modules are defined in code/tools/py3_requirements.txt in standard `pip` requirements format, and are intended to support Munki's own Python needs.

### Why customize?

You may find you need additional Python modules to be installed -- especially if you use third-party [repo plugins](Repo-Plugins) or [middleware](Middleware).

The maintainers of the Munki project want to be slow, cautious, and conservative about what Python modules are included in the "official" Munki distribution, as it puts them on the hook to keep them updated and to answer support questions for modules they may not even use. It's possible, even likely, over time that additional modules _will_ be added to the set in the "official" Munki distribution, but if you need certain modules, you should not (and do not have to) wait for those modules to be included in the Python bundled with Munki 4+.

### Customization options

#### Installing additional Python modules

Additional Python modules can be installed in `/usr/local/munki/Python.framework/Versions/3.8/lib/python3.8/site-packages` (note that path will change if Munki's embedded Python moves in the future).

`/usr/local/munki/Python.framework/Versions/Current/bin/python3 -m pip install <some_python_module>` would be one way to install modules when developing or testing, though that would not be a good choice for mass-deployment.

For mass-deployment, you could build an Apple installer package that installs the files you need added to the `python3.8/site-packages` directory.

#### Building a custom Python framework

You can build a munkitools package yourself containing any modules you want.

You can edit the py3_requirements.txt in code/tools and add your additional modules, then run code/tools/build_python_framework.sh to build that customized framework.

Or you can use https://github.com/gregneagle/relocatable-python directly to build a Python framework containing whatever modules you'd like.

### Custom Python deployment options

If you decide to build a customized Python framework, you'll need to deploy it. Here are a couple of options.

#### Building a custom munkitools package

Once you have your custom Python framework, save/copy it to the root of your Munki code repo. You can then run code/tools/make_munki_mpkg.sh to build a munkitools distribution pkg containing your customized Python. See [Building Munki Packages](Building-Munki-packages) for additional information.

#### Separate Python package

Another deployment alternative would be to use the "official" Munki tools releases, but install the tools with the embedded Python deselected, and instead install your custom Python in its place. Building a package of your custom Python is outside the scope of this documentation. You may find some useful pointers [here](Repackaging).
