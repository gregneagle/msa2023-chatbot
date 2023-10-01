# Automatic build (if the requirements.txt file works correctly):
1. Clone https://github.com/gregneagle/relocatable-python
2. You will need some version of Python 3 already installed to use this. Either use the one from CLI Tools, or use Munki's Python. This example will use Munki's python.
3. Call "make_relocatable_python.py" using Python 3, passing in AutoPkg's requirements.txt file:
```
/usr/local/munki/munki-python make_relocatable_python_framework.py --pip-requirements=autopkg/requirements.txt --upgrade-pip --os-version=11 --python-version=3.10.4
```

# Manual build:
1. Clone https://github.com/gregneagle/relocatable-python
2. You will need some version of Python 3 already installed to use this. Either use the one from CLI Tools, or use Munki's Python. This example will use Munki's python.
3. Call "make_relocatable_python.py" using Python 3 with no requirements file file:
```
/usr/local/munki/munki-python make_relocatable_python_framework.py --upgrade-pip --os-version=11 --python-version=3.10.4 --cache
```
4. Open up the local Python framework:
```
cd Python.framework/Versions/current/bin
```
5. Install the listed requirements in the requirements.txt file with pip:
```
./pip3 install pyobjc xattrs X Y Z...
```
6. Freeze the pip requirements into a new file:
```
./pip3 freeze > new_requirements.txt
```
7. Manually edit the new requirements file to reflect system requirements:
```
#
# *nix Requirements
#
xattr==0.9.6; sys_platform == 'darwin' or sys_platform == 'linux'
#
# MacOS Requirements
#
pyobjc==8.2; sys_platform == 'darwin'
...
#
# Windows Requirements
#
generateDS==2.35.24; sys_platform == 'win32'
```
8. To make it Universal, we have to add this to the new requirements.txt:
```
--no-binary :all:
```
9. Copy the framework into AutoPkg:
```
sudo cp Python.framework /Library/AutoPkg/Python3/
```
10. Run the tests using the script in the Scripts folder:
```
% ./run_tests.py 
................sss.........................WARNING: Did not load any default preferences.
..WARNING: Did not load any default preferences.
WARNING: Did not load any default preferences.
WARNING: Did not load any default preferences.
.WARNING: Did not load any default preferences.
....WARNING: Did not load any default preferences.
WARNING: Did not load any default preferences.
.WARNING: Did not load any default preferences.
..WARNING: Did not load any default preferences.
WARNING: Preference change TEST_KEY=''fake_value'' was not saved.
.Nothing found.
.
To add a new recipe repo, use 'autopkg repo-add <repo name>'
.No search query specified!
.
To add a new recipe repo, use 'autopkg repo-add <repo name>'

Warning: Search yielded more than 100 results. Please try a more specific search term.
.ss......................
----------------------------------------------------------------------
Ran 83 tests in 2.375s

OK (skipped=5)
```
11. Test some other AutoPkg functions
```
% autopkg run Firefox.download
```
12. Test a build using AutoPkgGitMaster.pkg:
```
% autopkg run AutoPkgGitMaster.pkg -vvvv -k PYTHON_VERSION=3.10.4 -k REQUIREMENTS_FILENAME=new_requirements.txt
```