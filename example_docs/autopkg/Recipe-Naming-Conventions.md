A recipe can be a simple plist or yaml file, but it can also be a folder, similar to bundles in macOS, a logical unit that can contain multiple variants of the recipe, custom processors, or additional required resources.

Going through each search directory in order, `autopkg` will look for files ending in ".recipe", ".recipe.plist", or ".recipe.yaml", starting from the root of the directory, and return the first one it finds.

1. `NAME.recipe`
1. `**/NAME.recipe` (where `**` is equivalent to basic shell globbing, returning any directory at this level in the tree) AutoPkg does not recurse any deeper than one directory "below" a given search directory.
1. `NAME.recipe.yaml`
1. `**/NAME.recipe.yaml` (again, only one directory below)

The recipes in the [autopkg/recipes](https://github.com/autopkg/recipes) repo follow an additional naming convention, and you are encouraged to follow it as well for your own recipes, especially if you will be sharing them with others:

- `NAME.download.recipe` (or `NAME.download.recipe.yaml`) indicates a recipe that only downloads a product and does no further processing (other than verifying the code signature of the downloaded product). These recipes are often the basis for `NAME.munki` and `NAME.pkg` recipes.

- `NAME.munki.recipe` (or `NAME.munki.recipe.yaml`) indicates a recipe intended for use with Munki.

- `NAME.pkg.recipe` (or `NAME.pkg.recipe.yaml`) indicates a recipe intended to extract or build packages, possibly for use with deployment systems other than Munki.

Some recipe names:

1. `GoogleChrome.pkg.recipe`  –  a simple standalone plist recipe that repackages Google Chrome
1. `GoogleChrome.pkg.recipe.yaml`  –  a yaml version of the above
1. `Firefox/Firefox.pkg.recipe`  –  a Firefox recipe in its own folder, possibly with additional resources
1. `OmniGroup/OmniFocus.munki.recipe`  –  a Munki recipe for OmniFocus, which imports it into Munki. Stored together with recipes for other OmniGroup products.
1. `AdobeAcrobatPro/AdobeAcrobatProXUpdate.munki.recipe`  –  an Acrobat Pro recipe that makes use of a processor (also located in this directory) that can parse Adobe's ARM update feed, which can be shared by multiple recipes for Acrobat
