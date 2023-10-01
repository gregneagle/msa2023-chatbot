# Introduction
With the release of AutoPkg 2, AutoPkg migrated to Python 3. 

As such, custom processors in recipe repos will also need to be compatible with Python 3. This document will attempt to explain some of the tasks you might need to do.

# Considerations 
AutoPkg 1.x is Python 2, AutoPkg 2.x Python 3.

A custom processor which is written in Python 2 will only run in AutoPkg 1.x, & likewise a custom processor which is written in Python 3 will only run in AutoPkg 2.x.

However, as AutoPkg 2 was only recently released recently. The best approach currently is to update your processors with code compatible with Python 2 and 3.

The below advises on some ways to make your custom processors be compatible with Python 2 and 3, & therefore AutoPkg 1.x & AutoPkg 2.x. 

# Tools

[python-modernize](https://python-modernize.readthedocs.io/en/latest/) is an excellent tool for adding Python 3 compatibility to existing Python 2 code, while maintaining Python 2 compatibility.

[pylint](https://pylint.readthedocs.io/en/latest/) is another tool to help you ensure your code is compatible with Python 3.

You can use `pip` to install these tools under your current Apple Python 2.7 install:
```
pip install modernize
pip install pylint
```

There is also an Apple installer package built by Greg Neagle for an event at Penn State MacAdmins 2019 that makes these two tools available: https://www.dropbox.com/s/nxk5uq8b1vg2xij/psumacpytools-1.0.pkg

# Guides

Here are a few guides outlining some strategies and techniques for making your code compatible with both Python 2 and 3:

* [The Conservative Python 3 Porting Guide](https://portingguide.readthedocs.io/en/latest/index.html)
* [Cheat Sheet: Writing Python 2-3 Compatible Code](https://python-future.org/compatible_idioms.html)

# Process

## Automatically generate Python 3 fixes
Run `python-modernize /path/to/SomeProcessor.py`  
`python-modernize`, when run without flags, generates a lot of output, including a UNIX diff-style output showing its suggested changes.

Here's an example, using an AutoPkg processor that I never published (and which is no longer useful):

```
$ python-modernize AamporterProcessor.py
 Loading the following fixers:
    lib2to3.fixes.fix_apply  (apply)
    <many lines of detail removed for clarity>
    libmodernize.fixes.fix_zip  (zip)
 Applying the following explicit transformations:
    (None)

RefactoringTool: Skipping optional fixer: idioms
RefactoringTool: Skipping optional fixer: set_literal
RefactoringTool: Skipping optional fixer: ws_comma
RefactoringTool: Refactored AamporterProcessor.py
--- AamporterProcessor.py	(original)
+++ AamporterProcessor.py	(refactored)
@@ -15,6 +15,8 @@
 # limitations under the License.
 """See docstring for AamporterProcessor class"""
 
+from __future__ import absolute_import
+from __future__ import print_function
 import os
 import subprocess
 import sys
@@ -57,9 +59,9 @@
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
         while proc.poll() == None:
-            print proc.stdout.readline().rstrip()
+            print(proc.stdout.readline().rstrip())
         if proc.poll() != 0:
-            print >> sys.stderr, proc.stderr
+            print(proc.stderr, file=sys.stderr)
         if 0:
             self.env['aamporter_processor_summary_result'] = {
                 'summary_text': 'The following new items were downloaded:',
RefactoringTool: Files that need to be modified:
RefactoringTool: AamporterProcessor.py
```

`python-modernize` would add

```
from __future__ import absolute_import
from __future__ import print_function
```

to the imports -- these imports make other Python imports behave as they do in Python 3, and make the `print` function from Python 3 replace the `print` statement from Python 2. `python-modernize` would also fix the `print` statements in the code to make them Python 3 compatible:

```
            print proc.stdout.readline().rstrip()
```
becomes
```
            print(proc.stdout.readline().rstrip())
```
and
```
            print >> sys.stderr, proc.stderr
```
becomes
```
            print(proc.stderr, file=sys.stderr)
```
That's the entire set of changes `python-modernize` would perform.

## Apply the automatically-generated Python fixes
If you accept the changes proposed by `python-modernize` (and until you get more experienced at this, you might as well), you can call the tool again with the `-w` flag to cause it to actually write its changes back to the original file:

```
python-modernize -w /path/to/SomeProcessor.py
```

`python-modernize` will create a backup of the unchanged file at `/path/to/SomeProcessor.py.bak`. If you have your Processors in a git repo (and you should), you may decide having these backups is unnecessary and just causes additional cleanup work. If so, you can tell `python-modernize` to skip creating backups using the `-n` flag:

```
python-modernize -w -n /path/to/SomeProcessor.py
```

## Double-check with PyLint
Run `pylint --py3k /path/to/SomeProcessor.py` to check the updated file for syntax that is not Python 3-compatible.

We'll use the `python-modernize`-updated AamporterProcessor as an example:

```
$ pylint --py3k AamporterProcessor.py
No config file found, using default configuration

------------------------------------
Your code has been rated at 10.00/10
```

`pylint` found nothing to complain about. If it had, you might need to do some additional work to make your code Python 3 compatible. 

## Testing

Now the hard part. You should test your updated processor with both AutoPkg 1.3.1 and AutoPkg 2. Just because the code _syntax_ is now compatible with both Python 2 and 3 does not guarantee it will _behave_ correctly/as desired under both Python 2 and 3.

> more documentation to come.

## Common issues

Below are some common issues which might be encountered.

### ModuleNotFoundError: No module named 'FoundationPlist'
Historically `FoundationPlist` shipped with AutoPkg as `FoundationPlist` can work with binary plists where Python 2's plistlib could not.

However, as plistlib in Python 3 can work with binary plists `FoundationPlist` became superfluous & as such was dropped.

Unfortunately, this is not a straight swap as the Python 2's plistlib's readPlistFromString() was replaced in Python 3.6+'s plistlib with load().

The below can be added to a processor to overcome this. Where FoundationPlist.readPlistFromString() was employed this can be changed to load_plist.

```
try:
    from plistlib import loads as load_plist
except ImportError:
    from FoundationPlist import readPlistFromString as load_plist
```

### ModuleNotFoundError: No module named xxxx
Some modules no longer exist in Python 3, & have been replaced.

As an example, the StringIO module was replaced with the IO module in Python 3.

Again we can import the needed module as required:

```
try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO
```

How to import the needed replacement modules will depend on the modules themselves.

### Error: 'dict' object has no attribute 'iteritems'

Python 3's dict does not have the 'iteritems' attribute, swap this for 'items' & test.

For example:

```
for key, value in some_dict.iteritems()
```

becomes:

```
for key, value in some_dict.items()
```

### Error: a bytes-like object is required, not 'str'

Python 3 brings with it a new data-type: bytes.

Some times a processor will generate a variable with a type of bytes instead of the expected string type.

The variable can be decoded as a string to overcome this issue.

For example:

```
toc = toc.strip().split('\n')
```

becomes:

```
toc = toc.decode("utf-8").strip().split('\n')
```

### [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1076)

> This could do with more detail

Python 3's urllib on macOS doesn't install its root certificates by default.

However, the [URLGetter superclass](https://github.com/autopkg/autopkg/wiki/Downloading-from-the-Internet-in-Custom-Processors) can be employed here instead of urllib. This works across AutoPkg 1.x & AutoPkg 2.x.

To add URLGetter:

• Add to your processors AutoPkg imports (from autopkglib import URLGetter)

• In your class declaration, change from myclass(Processor) to myclass(URLGetter)

• Replace any urllib or urllib2 url open calls with 'self.download(request)' where 'request' is a string of the URL wanted to get.

### Error: execv() arg 2 must contain only strings
The is likely raised via URLGetter.

This processor needs a string passed to it, not a urllib.request

# Additional info and Resources

* [Six documentation](https://six.readthedocs.io)
* [One porting case study](https://medium.com/@boxed/moving-a-large-and-old-codebase-to-python3-33a5a13f8c99)
* More to be added.