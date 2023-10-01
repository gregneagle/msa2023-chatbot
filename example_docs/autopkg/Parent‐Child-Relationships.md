We describe recipes both by function (e.g., .download, .pkg, .munki) and by relationship (parent, child). While it is entirely possible to author monolithic recipes that are self-contained, it is more common ([and best practice](https://github.com/autopkg/autopkg/wiki/Recipe-Writing-Guidelines#separating-recipe-tasks)) to separate recipes out by function and have them reference each other, creating a kind of chain of recipes that AutoPkg assembles at run time into a single recipe object.

Such relationships are established by having a recipe declare a `ParentRecipe`. The recipe that declares a Parent recipe is referred to as a Child recipe. Any recipe can be used as a Parent recipe and it is possible (and very common) for more than two recipes to be chained together in this way.

For example, in the core `recipes` repo, you will find these recipes for Firefox:
* [Firefox.download](https://github.com/autopkg/recipes/blob/master/Mozilla/Firefox.download.recipe)
* [Firefox.munki](https://github.com/autopkg/recipes/blob/master/Mozilla/Firefox.munki.recipe)
* [Firefox.pkg](https://github.com/autopkg/recipes/blob/master/Mozilla/Firefox.pkg.recipe)

(There are others, but these are the ones we will be examining.)

If we look at the Firefox.munki recipe, it has only one processor: `MunkiImporter`. But it also states in the main Dictionary (`<dict>`) that it has a `ParentRecipe`: `com.github.autopkg.download.firefox-rc-en_US`. This is the unique identifier for Firefox.download, so if you run Firefox.munki, it will run all the processor steps in Firefox.download in order and then the MunkiImporter processor in Firefox.munki. We refer to Firefox.download as a Parent recipe and Firefox.munki as a Child recipe in this instance.

Similarly, if you look at the Firefox.pkg recipe, it uses 4 processor steps to create a package, but it also declares the same `ParentRecipe` as the Munki recipe: `com.github.autopkg.download.firefox-rc-en_US`. It is very common for download recipes to have more than one child recipe, as different management systems have different requirements for the kind of payloads they are able to deploy  (e.g., Munki can deploy a drag-and-drop app inside a dmg, but Jamf Pro requires a package installer). If you run Firefox.pkg, it will run all the processor steps in Firefox.download in order and then its own 4 processor steps.

### Other Repos

Because authors generally write recipes to serve their own specific needs, you may find that all the parent recipes for a particular recipe are not found in the same repo. For example, a Munki user may not choose to write a pkg recipe for a product if they don’t need it, but someone else who does can write the pkg recipe using the original download recipe as a Parent. This allows recipe authors to leverage the work of others while simultaneously avoiding duplication, but it can cause confusion for new users. In order for AutoPkg to assemble the single recipe object it will run, it needs to have access to all the repos of all the parent recipes, not just the child recipe you are invoking. In short, AutoPkg can’t run what it can’t find.

Similarly, if a recipe uses a [shared processor](https://github.com/autopkg/autopkg/wiki/Processor-Locations#shared-recipe-processors), AutoPkg will need to access the repo that hosts the shared processor in order to compile the processor steps for the single recipe object.

For a recipe object to be assembled by AutoPkg, all of the necessary repos must be located locally on your AutoPkg runner and the repos must be listed in its `RECIPE_SEARCH_DIRS`, which happens by default when you add a repo using the `repo-add` verb. (For more information on how AutoPkg searches for recipes, see the [Recipe Search Order](https://github.com/autopkg/autopkg/wiki/Recipe-Search-Order) Wiki page.)

If you find a recipe you wish to use, you can also ask AutoPkg to add any repos needed to run that recipe and its parent(s) using the `--pull` flag when using the `make-override` or `info` verbs (e.g., `autopkg make-override Recipename.pkg --pull`).

### Overrides

Overrides are, by definition, child recipes, as they declare a `ParentRecipe` (the recipe you are overriding). Taking the above examples further, if you were running Firefox.munki in production, you would generally create an override for it and run the override. When you run the override, it sees that com.github.autopkg.munki.firefox-rc-en_US (Firefox.munki) is its parent, which itself has a parent of com.github.autopkg.download.firefox-rc-en_US (Firefox.download). Thus, it would create a single recipe object that runs the processors from Firefox.download, then Firefox.munki, then your override (which conventionally has no processors) in order.