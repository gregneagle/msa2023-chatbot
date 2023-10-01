# Developing Custom Processors
Custom processors are Python files with some specific boilerplate templates. You can run any Python code inside a custom processor, which means you can do just about anything in one.

## Basic Processor Structure
All processors are structured the same basic way:
* A custom processor class that inherits from `Processor` or `URLGetter`
* The class defines `input_variables` and `output_variables`, which determines what input is expected/required and what output is provided
* The class must have a `main()` function
* If you want to be able to execute a processor standalone (and not just within the context of running a recipe), you need to run `execute_shell()` at the bottom of the file

Look at the [Sample Custom Processor](https://github.com/autopkg/recipes/blob/master/SampleSharedProcessor/SampleSharedProcessor.py), which is a good example of the boilerplate:
```
from autopkglib import Processor, ProcessorError

__all__ = ["SampleSharedProcessor"]


class SampleSharedProcessor(Processor):
    """This processor doesn't do anything useful. It is a demonstration of using
    a shared processor via a recipe repo."""

    description = __doc__
    input_variables = {
        "shared_processor_input_var": {
            "required": True,
            "description": "Test the use of an input variable in a shared processor.",
        }
    }
    output_variables = {
        "module_file_path": {"description": "Outputs this module's file path."}
    }

    def main(self):
        // do stuff here
        print("My custom processor!")


if __name__ == "__main__":
    PROCESSOR = SampleSharedProcessor()
    PROCESSOR.execute_shell()
```

You could copy and paste this boilerplate and just put your code into `main()`, and replace the input/output variables, and run it.

### Should I inherit from Processor, or URLGetter?
If your custom processor needs to [download anything from the internet](https://github.com/autopkg/autopkg/wiki/Downloading-from-the-Internet-in-Custom-Processors), use `URLGetter` as your base class. Otherwise, use `Processor`.

## Where do custom processors go?
All processors must be within AutoPkg's search paths to be found.
Generally speaking, any custom processor needs to be in one of two places:
* Within the same folder as the recipes that use it (**most common**)
* In a shared folder with a stub recipe so it can located by identifier (see [Shared Processors](https://github.com/autopkg/autopkg/wiki/Processor-Locations#shared-recipe-processors))

## How do I use it in a recipe?
If the custom processor is in the same folder as the recipe, you can just use class name directly in your recipe. Note that the `.py` source file name must match the class name exactly.

Example: recipes/Mozilla
[Firefox.download](https://github.com/autopkg/recipes/blob/master/Mozilla/Firefox.download.recipe) uses a custom processor [MozillaURLProvider](https://github.com/autopkg/recipes/blob/master/Mozilla/MozillaURLProvider.py). The processor invocation within the recipe [looks like this](https://github.com/autopkg/recipes/blob/master/Mozilla/Firefox.download.recipe#L29-L41):
```
        <dict>
            <key>Arguments</key>
            <dict>
                <key>product_name</key>
                <string>firefox</string>
                <key>release</key>
                <string>%RELEASE%</string>
                <key>locale</key>
                <string>%LOCALE%</string>
            </dict>
            <key>Processor</key>
            <string>MozillaURLProvider</string>
        </dict>
```

The `Processor` key simply calls `MozillaURLProvider`, which is also the [name of the custom processor class](https://github.com/autopkg/recipes/blob/master/Mozilla/MozillaURLProvider.py#L74).

See [Processor Locations](https://github.com/autopkg/autopkg/wiki/Processor-Locations) for more details.

## Running a Custom Processor standalone
The Processor class comes with the convenience function `execute_shell()`. This function allows you to run a processor as a standalone script via the command line, which is helpful when developing, testing, or debugging a custom processor.

##### Sample Usage - Plist input
```zsh
# Set processor required variables in the plist
defaults write /tmp/processor.plist ARTICLE_NUMBER '1888'
# Enable SSJ3 verbose
defaults write /tmp/processor.plist verbose -int 3
# Ensure the plist is in XML format (as of writing this, the code only expects XML format, not binary [or json])
plutil -convert xml1 /tmp/processor.plist

# Ensure your PYHTONPATH includes the AutoPkg libraries
export PYTHONPATH=/Library/AutoPkg

# Run your custom processor
/Library/AutoPkg/Python3/Python.framework/Versions/Current/bin/python3 ${HOME}/src/autopkg/n8felton-recipes/SharedProcessors/AppleSupportDownloadInfoProvider.py < /tmp/processor.plist
```

##### Sample Usage - Command line arguments/variables
```zsh
# Ensure your PYHTONPATH includes the AutoPkg libraries
export PYTHONPATH=/Library/AutoPkg

# Run your custom processor
/Library/AutoPkg/Python3/Python.framework/Versions/Current/bin/python3 ${HOME}/src/autopkg/n8felton-recipes/SharedProcessors/AppleSupportDownloadInfoProvider.py ARTICLE_NUMBER=1888 verbose=3

# Press CTRL-D to send EOF to Python waiting for stdin input. (Improvement for later).
```

##### Sample Output
```
AppleSupportDownloadInfoProvider: Article URL: https://support.apple.com/kb/DL1888
AppleSupportDownloadInfoProvider: Download URL: https://support.apple.com/downloads/DL1888/en_US/&
AppleSupportDownloadInfoProvider: Full URL: https://updates.cdn-apple.com/2019/cert/041-88763-20191011-6e70f498-9d39-420c-b11b-b252b17233e2/HewlettPackardPrinterDrivers.dmg
AppleSupportDownloadInfoProvider: Article title: HP Printer Drivers v5.1 for OS X
AppleSupportDownloadInfoProvider: Version: 5.1
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>ARTICLE_NUMBER</key>
	<string>1888</string>
	<key>article_url</key>
	<string>https://support.apple.com/kb/DL1888</string>
	<key>url</key>
	<string>https://updates.cdn-apple.com/2019/cert/041-88763-20191011-6e70f498-9d39-420c-b11b-b252b17233e2/HewlettPackardPrinterDrivers.dmg</string>
	<key>verbose</key>
	<integer>3</integer>
	<key>version</key>
	<string>5.1</string>
</dict>
</plist>
```
