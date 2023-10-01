#### Defining & using custom variables in recipes
​
## Overview
​At the end of the day, AutoPkg input and output variables are just arbitrary strings that are used as a substitute for another string value.

While processors define a set of required and optional variables that can be used within its arguments, you can define your own custom variables within this structure. This is valuable when you need to use a particular processor multiple times within a recipe but need to persist the collected values, as on each subsequent processor run the previous output variable values get overwritten.

Typically, recipes do not need the previous values of a given output variable to persist. For example, a recipe needing to find multiple files (`FileFinder`) and copy them to a central location (`Copier`) in order to create a PKG, you can simply run the necessary processors for one item and repeat those processor steps for each additional item. Once you've completed the larger task of copying the files from the collected paths, storing what the previous values were for each item is unnecessary.
​
## Defining custom variables
​Defining a custom variable is as simple as supplying it as a key in the Arguments dictionary and setting its value to the previously collected output variable.
​
```xml
<dict>
	<key>Arguments</key>
	<dict>
		<key>your_custom_variable</key>
		<string>%your_collected_output_variable%</string>
	</dict>
	<key>Processor</key>
	<string>PROCESSOR_NAME</string>
</dict>
```
​
### Example
​In the example below, the `FileFinder` processor is used twice to collect the paths of two different files.

The first time `FileFinder` is run ([per the processor’s info](https://github.com/autopkg/autopkg/wiki/Processor-FileFinder)), the found file path is assigned to the `found_filename` output variable. The second run of `FileFinder` sets the previously collected `found_filename` to a custom `previous_file` variable and overwrites `found_filename` with the collected second file path.

Subsequent processors not listed below can then use `%previous_file%` and `%found_filename%` in their Arguments dictionary.
​
```xml
<dict>
	<key>Comment</key>
	<string>Collect the first file path.</string>
	<key>Arguments</key>
	<dict>
		<key>pattern</key>
		<string>%RECIPE_CACHE_DIR%/%NAME%/*.pkg</string>
	</dict>
	<key>Processor</key>
	<string>FileFinder</string>
</dict>
<dict>
	<key>Comment</key>
	<string>Take the collected first file path and assign it to the custom previous_file variable. Collect the second file path and overwrite the previously collected output variables.</string>
	<key>Arguments</key>
	<dict>
		<key>pattern</key>
		<string>%RECIPE_CACHE_DIR%/%NAME%/*.txt</string>
		<key>previous_file</key>
		<string>%found_filename%</string>
	</dict>
	<key>Processor</key>
	<string>FileFinder</string>
</dict>
​
```