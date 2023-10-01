**NOTE:** AutoPkg Windows is NOT officially supported today and is a work in progress. Not all functionality will work.

## Prerequisites:

There are a few prerequisites required to run AutoPkg on Windows

- [Python3 and Pip](https://www.python.org/downloads/windows/)
- [GIT for Windows](https://gitforwindows.org/index.html)
- [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
  - depends on which version of Python you are using and if wheels are available for all dependancies

Recommended:

- Windows Terminal
- Visual Studio Code
  - Python Extension

## AutoPkg Prefs:

AutoPkg loads Preferences from a file on windows (and linux) but does not currently automatically create the file if it does not exist, and it won't add preferences to it if it is missing.

At the moment you must create one.

For Windows, Generally: 

- `C:\Users\_YOUR_USER_NAME_\AppData\Local\Autopkg\config.json`
- Directory Given by `appdirs.user_config_dir("Autopkg", appauthor=False)`


## References:

### Examples:

- AutoPkg Dev Setup and Check: https://github.com/jgstew/jgstew-recipes/blob/main/check_setup_win.bat
- GitHub Action that works on Windows: https://github.com/jgstew/jgstew-recipes/blob/main/.github/workflows/VersionGetMajorMinor.yaml