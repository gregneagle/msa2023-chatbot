The following is a set of guidelines that should be followed when writing your own recipes, especially if you wish to share them with others via a Git repository. The AutoPkg `repo-` commands make it easy to add and update recipes from others' repos.

### Finding examples

There is quite a variety of tasks done to handle many common applications in the AutoPkg's own [recipes repo](https://github.com/autopkg/recipes). You can use existing, core AutoPkg processors to do things like:
- download and cache from a URL
- dynamically retrieve a URL from a Sparkle feed
- mount DMGs
- stage, copy, delete files
- import into Munki, providing additional `makepkginfo` options
- build flat installer packages with specific permissions, ownerships
- extract version information, read/write/merge plists

Sometimes vendors make a stable URL available that always points to the latest version, for example [Google Chrome](https://github.com/autopkg/recipes/tree/master/GoogleChrome). In other cases, a vendor may have written their own system to parse their own metadata feed structure, such as [Bare Bones Software](https://github.com/autopkg/recipes/tree/master/Barebones). In cases like the latter, it is almost always necessary to write a custom processor. There are also a number of processors in which HTML is scraped using a RegEx match for a predictable URL pattern (see [Mozilla](https://github.com/autopkg/recipes/blob/master/Mozilla/MozillaURLProvider.py), [Adium](https://github.com/autopkg/recipes/blob/5db796bcc0da46f2406a125e73e2b045472b0d66/Adium/Adium.download.recipe#L20-L30), [Puppet Labs](https://github.com/autopkg/recipes/blob/master/Puppetlabs/PuppetlabsProductsURLProvider.py)).

Custom processors are written in Python. There is not yet documentation for writing your own, but hopefully these examples can get you started.

### Separating recipe tasks

A number of the recipes in the AutoPkg [recipes repo](https://github.com/autopkg/recipes) have both `.munki` and `.pkg` variants. Because both recipes need to first download the software that's going to be later processed, it's possible to define the download steps in one place as a "parent recipe", by setting the identifier of the parent recipe in the `ParentRecipe` top-level key in the recipe. The parent recipe's steps will run before the child recipe's.

A recipe may have a ParentRecipe, and that parent recipe may have a ParentRecipe of its own. For example, you could have one recipe (Foo.download.recipe) that downloads an item, a child recipe (Foo.pkg.recipe) that repackages the item, and child of that recipe (Foo.munki.recipe) that imports the pkg into your Munki repo.

There's no rule that your recipe(s) must be broken down into parent/child recipes if you only plan to ever use them with Munki, but by separating the tasks up front you make it easier should you or anyone else wish to add another variant to a recipe (for example, importing into some other software management system).

### Identifiers

It's very important to decide on a unique identifier for the recipe that will remain fixed. The reverse-domain naming style should contain:
- home of the repo (probably usually `com.github.`)
- maintainer/org name (ie. a GitHub user name, Google Code project, etc.)
- what the recipe does (ie. `.download`, `.pkg`, `.munki`)
- the actual name of the software

For example:
`com.github.foo.pkg.myapp` - written by user "foo", builds a pkg of "myapp."

**Be careful not to end your identifier in common Apple file extensions, like `.dmg` or `.download`, as they can lead to undefined and undesirable behavior.** AutoPkg will generally create folders named after your identifier, so if your identifier is "com.github.myorg.myapp.download", you'll create a folder in your Cache directory called "xxxx.download", which the Finder will treat like a partial Safari download. Other processors may also behave in strange ways.

When a recipe override is created by an AutoPkg user, it will use the recipe's identifier to identify your recipe as the `ParentRecipe` (as overrides are actually child recipes). This means that if you should change your identifier, the override will no longer be able to locate your recipe. So, unless your recipe is very new and you are resolving a conflict or confusion about the recipe's identifier, it's strongly recommended to never change your recipe identifier once it has been made publicly available.

### Input variables

Your recipe may support additional parameters for pulling alternate versions, branches, languages, etc, and can do so via input variables. At other points in the recipe these values can be substituted in via enclosing `%` characters. For example, the `Firefox.download` [recipe](https://github.com/autopkg/recipes/blob/master/Mozilla/Firefox.download.recipe) supports `LOCALE` and `RELEASE` input variables. You'll notice these are simply passed as arguments to the `MozillaURLProvider` processor.

Any custom input variables you support in the recipe should be clearly documented in the `Description` key.

Assuming you are sharing your recipe, consider these variable names to be your recipe's "API", because changing them will mean that the recipe will no longer be overridden as expected, for as long as a user is still overriding the old key name. The only time to change existing variable names might be for an entirely new recipe. Adding new variables to support new functionality in your recipe is ok, as long as existing functionality remains unchanged.

Along the same lines, some authors have chosen to use input variables to declare constants, much like you would in a programming language. This can cause issues when sharing your recipes with others. The two most common examples of this method are:
- to define complex strings (e.g., URLs, regular expressions), thus making the recipe a little easier to read; and
- to define a value the author wanted to use more than once, making the recipe easier to write (reducing the odds of syntax errors).

In the first case, the disadvantage is that any future changes to that value will not be updated in any existing override; the user will need to change the value manually or recreate the override. In the second case, a user who overrides the default value with their own may break the recipe if it depends on the default value. 

Please carefully consider these possibilities when authoring your recipes; it may be better for sharing purposes to hard code constant values into the Process section of the recipe. If you do choose to use Input variables as constants, recommend in the Description section of your recipe that users delete those particular variables from their override, causing the default value from the parent recipe to be loaded upon run.

#### Using a VERSION Input Variable

Sometimes a recipe may be useful not only for retrieving the latest update but for a specific previous version as well. For example, a vendor may require a particular minimum version as a prerequisite for the latest update (e.g., Office 2011 updates after 14.1.0 required at least 14.1.0 to be installed first). Maybe the recipe user doesn't yet have this update in their repo and would like to get it the same way AutoPkg gets the latest updates. Alternately, a vendor may support more than one major version at a time when a paid upgrade is required for the newer version (e.g., Microsoft Office 2016 and 2019, Ableton Live 9 and 10). Perhaps you would rather author a single recipe that can retrieve multiple versions rather than writing separate recipes for every major version.

If your recipe is able to pull alternate or multiple versions, provide this capability with a `VERSION` Input variable (in comparison to the lowercase variant for internal usage by autopkg processors). Using the name `VERSION` is a convention; there are no special properties associated with the name. For example, something like `MAJOR_VERSION` may be more appropriate if your recipe is one that retrieves different major versions based on what the recipe user selects in their override. The convention of using a Version input variable is useful regardless of whether you have written a custom processor for this specific application or are using core processors (e.g., where the version number may be part of the URL used by `URLTextSearcher` or `URLDownloader`).

If you provide this input variable, users who need an intermediate update or different major version can then choose to do a one-off override of the Version variable with the `-k/--key` option. For example:
````
autopkg run -k VERSION=14.1.0 MSOffice2011Updates.munki
autopkg run --key LIVE_VERS=9 AbletonLive.download
````

For an example of how this is done in recipe-specific processors, check out the processor used for [Microsoft Office products](https://github.com/autopkg/recipes/blob/master/MSOfficeUpdates/MSOfficeMacURLandUpdateInfoProvider.py), which makes use of the same metadata XML feed used by Microsoft Auto Updater (MAU) and is therefore able to pull the same versions it exposes.

Please also note that software versioning (which can use the [semantic versioning](https://semver.org) convention to denote compatibility among other concepts) is not guaranteed to line up with package versions.
