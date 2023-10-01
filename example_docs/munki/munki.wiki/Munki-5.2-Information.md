### Introduction

Munki 5.2 was released on November 24, 2020.

#### Compatibility
Munki 5.2 (or more specifically, Managed Software Center 5.3) has been fairly well-tested on macOS Catalina and macOS Big Sur, and should run on macOS Mojave. Support has been dropped for macOS 10.10. Not a lot of testing has been done on macOS 10.11 and 10.12, but it should work.

##### Apple Silicon
Munki 5.2 will run on Apple Silicon Macs via Rosetta 2. Munki 5.2 will not be a "Universal2" release. Until recently, building Universal2 apps required a special beta of Xcode 12. Very recently, Apple released Xcode 12.2 and it is now possible to build Universal2 apps with a public release of Xcode.

But even if the GUI apps were Universal2 apps, most of the heavy lifting Munki does is in its command-line tools, which are Python scripts. So we need a Universal2 Python. Munki's Python is a modified version of the Python 3.8.5 framework from Python.org, and Python.org has not yet released Universal2 builds of Python. When they do, they will almost certainly be version 3.9.x, which will require a new round of extensive testing with Munki. So Universal2 support for Munki will have to wait for the future.

#### Managed Software Center
Munki 5.2 introduces a visual redesign of Managed Software Center that is more in keeping with the "design language" of macOS Big Sur. More information [here](Managed-Software-Center-in-Munki-5.2).

#### Configuration Profile Emulation
Munki 5.2 also adds support for limited emulation of configuration profile installs on Big Sur, which removes the ability to install configuration profiles with the `profiles` command. See [here](Configuration-Profile-Emulation) for more information.

