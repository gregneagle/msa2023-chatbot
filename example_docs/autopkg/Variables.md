There are four ways that variables are established and their values set in AutoPkg:
1. Via the Input section of the recipe;
2. Via the Arguments section of a Processor call;
3. Via output from a processor; and
4. Via [AutoPkg Preferences](https://github.com/autopkg/autopkg/wiki/Preferences).

Once a variable is set, it is in the environment for that run and can be used by any processor until the end of the run. By convention, variables in `UPPER_CASE` have string values (e.g., Input variables) and variables in `lower_case` are related to a processor or represent a non-string structure like boolean or dict. (For more details and specific exceptions, [see the Input Variables page in this wiki](https://github.com/autopkg/autopkg/wiki/Input-Variables).)

## Input Variables

Input variables are established when the recipe is loaded to run and their values will persist throughout the run of the recipe (assuming conventions are being followed)—in this way, they are variables because you can change their value via an override but they are constants once the recipe is loaded because they are not expected to change. If the recipes in a recipe chain define an Input variable in more than one place (e.g., the `NAME` variable is set in both the `.download` and `.munki` recipe for a certain app), the value in the last child recipe in which it appears (usually an override) shall be the value used. You can use variable substitution to set Input variable values, but only from the variables established in the Input section (e.g., setting an input variable to `%NAME% Latest` would work if `NAME` was an Input variable, but `%NAME%-%version%` would not work if `version` is not set until a particular processor like `Versioner` is run).

## Processor Variables

All other variables are created via Processor recipe steps. Any variable defined in the Arguments section of a Processor step becomes available to that processor and all subsequent processors. AutoPkg simply loads the dictionary of key-value pairs defined in the Arguments section; it does not evaluate whether the processor actually needs or supports the variables defined. This fact can be leveraged to arbitrarily create variables for later use, such as when you need to preserve a value that might get overwritten by a subsequent processor ([see the Defining Custom Variables page in this wiki](https://github.com/autopkg/autopkg/wiki/Defining-Custom-Variables) for more details).

Processors commonly use output variables to pass useful information back to the recipe for subsequent use and/or evaluation. As with variables established via processor Arguments, these variables are available for the rest of the run after creation. Some processors may create more values than are apparent in their definition. For example, `URLTextSearcher` will return a single value by default, but if your regular expression uses the syntax that allows you to capture more than one value from that expression (i.e., `(?P<variablename>regex)`), `URLTextSearcher` will add such values to the environment.

Many core processors pass output variables with names that match (input) arguments needed for subsequent processors. Because of this, you will see some recipes where there are processors used without arguments where the definition of said processors says that there are mandatory arguments. So long as these values have been set in the run environment, AutoPkg will use them. This allows for some convenient shorthand.

There are also two side effects of this. You should assume that a variable established via a processor (input or output) may change its value during the run, especially if it is commonly used as a processor output variable. Running a recipe with at least two levels of verbosity (`autopkg run -vv`) will help you determine the value of a variable at various points during the recipe run. 

As well, some processors have optional input arguments that match common output variable names. The `AppPkgCreator` processor is an example of where this needs to be handled carefully. If the value for `version` has been set by whatever means when `AppPkgCreator` is called, it will use that string for the version number and skip the routines that attempt to determine the version number from CFBundleShortVersionString in the app bundle. That is beneficial if CFBundleShortVersionString does not hold the version information you wish to use — you might have used `Versioner` to extract the version number from a different key in the Info.plist for the app, for example. However, if you want `AppPkgCreator` to determine the app version and you have established the value of `version` when running an earlier processor like `URLTextSearcher` (because the version string used for the download path is different in some way than the version number in CFBundleShortVersionString), you may need to arbitrarily set the value of `version` to an empty string when calling `AppPkgCreator` in order to run its versioning routine.

## Preferences

[AutoPkg’s preferences](https://github.com/autopkg/autopkg/wiki/Preferences) are used to establish many key operational functions, including the location of the recipe repos, overrides, and cache, as well as the repo search order and trust verification status. It is also possible to establish arbitrary variables and corresponding values (e.g., `defaults write com.github.autopkg VARIABLE value`). This is often done when multiple recipes need the same information, such as a server address (e.g., `MUNKI_REPO` for Munki, `JSS_URL` for JamfUploader). Any variable established this way will be loaded from the preferences on each run. Your recipe may choose to change the value during the run (e.g., using an Input variable with the same name), but it will reload the value stored in AutoPkg’s preferences for subsequent runs.

## Other Information on Variables

In addition to the pages already cited on [Input Variables](https://github.com/autopkg/autopkg/wiki/Input-Variables) and [Defining Custom Variables](https://github.com/autopkg/autopkg/wiki/Defining-Custom-Variables), the following pages may also be of interest:

* [Recipe Format: Variables, String Substitution, and Input](https://github.com/autopkg/autopkg/wiki/Recipe-Format#variables)
* [Recipe Writing Guidelines: Input Variables](https://github.com/autopkg/autopkg/wiki/Recipe-Writing-Guidelines#input-variables)
* [Important Variable Names](https://github.com/autopkg/autopkg/wiki/Important-Variable-Names)
