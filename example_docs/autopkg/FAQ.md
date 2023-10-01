### Every time I run a recipe it downloads something even if it didn't change. Why?

AutoPkg's download processor makes use of a couple of standard HTTP headers ("last-modified" and "etag") to determine if the file has changed before requesting a download. If the vendor's web server does not send those headers, or the file is hosted on one of several replicas, AutoPkg cannot tell if the file on the server is different from the one it has.

For example:  
VLC is hosted on multiple mirrors, and the different mirrors have different "last-modified" time stamps. If AutoPkg gets a mirror with a "last-modified" date that's different than what AutoPkg previously saw for VLC, AutoPkg will download the "newer" VLC. Of course, once it's downloaded, AutoPkg will discover it's a VLC version it already has.

### Every time I run a .munki recipe it keeps importing the item into my repo. Why?

AutoPkg doesn't automatically rebuild your Munki catalogs for you, so the new items copied to the repo don't actually exist in any catalogs.

There is however, a special recipe, `MakeCatalogs.munki`, that's part of the [autopkg/recipes](https://github.com/autopkg/recipes) repo. It must be run as part of the _same AutoPkg run_ as other Munki recipes, for example:

`autopkg run GoogleChrome.munki MakeCatalogs.munki`

If it detects that any new items were imported into the Munki repo during this run, it rebuilds catalogs. If no new items were imported, it does not. If this recipe is run separately from other Munki recipes, it will not detect a need to rebuild catalogs and _it will do nothing_.  If you need to rebuild Munki catalogs in this situation, just use Munki's `makecatalogs` tool.


### Everyone says a new version of Application X was released, but AutoPkg doesn't pick it up. Why?

Many recipes rely on the same auto-update mechanism that's available within the application itself to detect new versions. Sometimes a release is made generally available via a web page before it is via the in-application update mechanism. This is very common with the Flash Player recipe - it is often available for download hours before it's published on Adobe's auto-update feed.

So, wait a short while. To confirm for yourself, you may also check by running the application in question and seeing whether it thinks a new version is available. If it considers the version you're running to be the latest, then AutoPkg likely will as well.

If you can't wait, in most cases you can override AutoPkg's download mechanism with a path to a version of the package you've downloaded manually:

`autopkg run --pkg /path/to/downloaded/package <recipe>`


### Can I change a recipe to do *X* instead of *Y*? Do I use [overrides](https://github.com/autopkg/autopkg/wiki/Recipe-Overrides) for that?

Check the next FAQ as well, but it's possible that you can. The best way to know is by checking the recipe with `autopkg info [recipe name]` for the `Input` stanza to see if what you're trying to modify is listed in that section. If it is, congratulations! As described [here](https://github.com/autopkg/autopkg/wiki/Recipe-Overrides), running `make-override` will provide you with a template you can make your changes in.
If not, you could do any of the following: 
+ Modify the recipe directly (not recommended, since it could cause difficulty when running a repo-update)
+ File an issue at the GitHub repo that the recipe came from (usually `https://github.com/autopkg/[repo name]`)
+ Fork the repo and add that flexibility in, sending a Pull Request to the originating repo to start the conversation with (very much recommended, tips [here](https://www.afp548.com/2014/08/05/look-less-silly-on-github/)).

### I would like to customize a pkg recipe to add a custom preinstall/postinstall script. Can this be done with an override?

Not currently. The [[PkgCreator processor|Processor-PkgCreator]] can take a path to a scripts directory, but this is passed in as a [dictionary key](https://github.com/autopkg/autopkg/blob/812565979d73a3859b86ba1f2896dc737ed49c5b/Code/autopkgserver/autopkgserver#L69-L71) to the `pkg_request` variable. This means that the step of the recipe that runs the PkgCreator processor must be replaced with one that provides a path to the scripts directory.

Because an override can't replace an entire step of a recipe, it's necessary to make your own modified copy of the pkg recipe. Making a new recipe and using the pkg recipe as a `ParentRecipe` is possible, however when the steps from the parent recipe run a package will still be built, so the pkg building will happen twice, once by the parent recipe and once in your recipe with its modifications.

It's possible that in the future, there will be a mechanism available to support this. An alternate approach is to package your script(s) separately from the update such that they need not be bundled along with every application update.

### This recipe used to work, but now it doesn't. What should I try?

Don't despair! The repo containing the recipe may have been updated to fix the issue. Try `autopkg repo-update <repo-name>` or just `autopkg repo-update all`. It's also possible that you have an override for the recipe and a recent recipe update has caused a conflict with your override. First check the documentation for the version of the recipe you have by looking at the description printed out with `autopkg info <recipe>`. If it's still unclear as to why the recipe is not working, you can find the author's recipe repo [on GitHub](https://github.com/autopkg) and open an issue.

### I'm behind a proxy and recipes seem to be not working.

You should set `http_proxy` and/or `https_proxy` environment variables so that AutoPkg code that makes requests to servers (Python's `urllib2` module and possibly the `curl` binary) will use them. You can either set them at the same time as the command invocation:

`http_proxy=my.proxy:port autopkg run <recipe>`

Or you may prefer to export these as is suggested in [this StackOverflow thread](https://stackoverflow.com/questions/9445489/linux-curl-command-with-proxy), so that they will be used with every invocation of `autopkg` or `curl`

### Can I fetch multiple variations of the same product, e.g. Office 2016 delta updates/full installers?

Yes, and again, overrides are the way in which you'd go about doing so. It's similar to the workflow for [AppStore Apps](https://github.com/autopkg/nmcspadden-recipes#appstoreapp-recipe), in that you can use the `--name` option when making your override, to denote what option in that particular recipe you're taking advantage of. If you'd like to fetch several at once, e.g. in a recipe list, you can make multiple distinctly-named overrides and refer to each by its filename just like any other recipe. (No need to use the full path to the file, just like other overrides/recipes.)

### I'm getting a warning message "com.github.autopkg.recipe.foo is missing trust info and FAIL_RECIPES_WITHOUT_TRUST_INFO is not set". Do I need to do something?

It's optional, please see [this wiki page](https://github.com/autopkg/autopkg/wiki/Autopkg-and-recipe-parent-trust-info) for more info on how to operate AutoPkg in a safer way. This is just a warning message, it won't block you from operating AutoPkg as you had in the past (if you were using it previously).

### I'm getting a failure message "Code signature verification failed..." What should I do?

This is commonly due to a botched download (due to proxy failures or other network conditions) that leaves you with what would be non-functional software - in that case it's doing you a favor by alerting you! In the rare case that the codesigning actually changed, you may just need to update the recipe repo and trust info (if applicable). If you have a good reason and still want to ignore this warning, please review the last section on this page: [Using CodeSignatureVerification](https://github.com/autopkg/autopkg/wiki/Using-CodeSignatureVerification#disabling-codesignatureverification-in-an-existing-recipe)

### If there is more than one recipe available with the same name, how can I make certain that AutoPkg is referencing the particular one I want?

If you specify a recipe by name, (e.g., `autopkg run SomeProduct.download`), AutoPkg uses the first recipe that matches that name in the [[recipe search order|Recipe Search Order]]. If that doesn't reference the recipe you want, you can specify the recipe identifier instead of the recipe name (e.g., `autopkg make-override com.github.foo.download.someproduct`) — this works with all the recipe-related verbs and is case-sensitive. Alternatively, you may specify the full path to the recipe (e.g., `autopkg run /Users/someuser/Library/AutoPkg/Recipes/SomeProduct.download`) — this does not work with `make-override`, but can be used with other recipe-related verbs such as `run`.

### How do I provide a GitHub Personal Access Token to AutoPkg?

It can be beneficial to provide a Personal Access Token to AutoPkg. An example of why someone might need to do this is if they are hitting GitHub's API rate limit, which can sometimes happen when executing automated searching (e.g., using the `autopkg info -p` command to pull parent repositories). In version [1.0.4](https://github.com/autopkg/autopkg/releases/tag/v1.0.4), AutoPkg introduced a way to use a [personal access token](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token). AutoPkg looks for either a GITHUB_TOKEN preference key or a file containing the token present in the logged-in user's home folder: `~/.autopkg_gh_token`.

If you're only planning to use the token for `autopkg search foo`, you can set the scope (or permission) for your new token to `public_repo` and leave the other options unchecked.