### How autopkg's recipe search order works

`autopkg` supports a search order system for recipes, so that full paths to recipe files don't need to be entered with every command. 

`autopkg` searches any recipe override directories, followed by recipes in the recipe search directories, described below.

### Recipe override directories

1. The default recipe override directory is `~/Library/AutoPkg/RecipeOverrides`
1. You may set the RECIPE_OVERRIDE_DIRS [[preference|Preferences]] to an array of directories instead.

### Search directories

The recipe search directories are set in four possible ways:

1. Set the `RECIPE_SEARCH_DIRS` [[preference|Preferences]].
1. Use the `-d/--search-dir` command-line option
1. Do neither and let it use the defaults: the current directory, followed by `~/Library/AutoPkg/Recipes`, followed by `/Library/AutoPkg/Recipes`
1. Any recipe repos added via the `repo-add` verb are automatically appended to the `RECIPE_SEARCH_DIRS` preference, which is created if needed.  These repos are searched in order of addition, therefore in the event of a recipe name collision, the recipe from the repo highest in the `RECIPE_SEARCH_DIRS` preference is used.

### Finding the actual recipe

See the [[Recipe naming conventions|recipe naming conventions]] details page.