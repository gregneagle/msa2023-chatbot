### TL;DR:
* You are expected to verify and trust the recipes you run.
* Make overrides for _every_ recipe you run.
* Trust information is stored in the override upon creation, establishing that you trust that version of the recipe.
* When a recipe (or custom processor used by the recipe) changes, you need to re-establish trust by auditing the changes.
* Once you have confirmed that you trust the updated recipe, run `autopkg update-trust-info override_name` to update the trust info in the override.
* Best practice is to enable strict trust verification (e.g, `defaults write com.github.autopkg FAIL_RECIPES_WITHOUT_TRUST_INFO -bool YES`) so that changed recipes fail, allowing you a chance to audit the changes first. Otherwise, the recipe will run with a warning.

### Introduction
AutoPkg encourages the use of recipes created and shared by others. You can leverage the hard work done by other admins without having to re-invent the wheel yourself. You can add "repos" of other people's recipes using the `autopkg repo-add` command.

But there is an element of risk in using other people's recipes -- a bad actor could create a malicious recipe, or a well-meaning admin could introduce an error into a recipe that causes unexpected issues.

You should audit any third-party recipes you use, especially if you do not know the recipe creator/maintainer. This means becoming familiar enough with AutoPkg recipes to be able to read and understand them. The `audit` verb can assist with this, as any text you see displayed (when running it with a recipe path) is cause for at the least researching why the recipe is constructed that way, and either following up with the vendor or the recipe maintainer, if appropriate. Contents of a recipe that are flagged by `audit` are ones that:
*   Are missing a CodeSignatureVerifier step
*   Use non-HTTPS URLs for downloads
*   Supply their own or leverage [shared](https://github.com/autopkg/autopkg/wiki/Processor-Locations#shared-recipe-processors) processors and therefore would run code not provided by AutoPkg itself
*   Use processors that may potentially be modifying the original software downloaded from the vendor
    * Processors which move, copy, modify/edit, delete, or symlink the contents fall under this definition, and their paths are included in the output

Vendors are known to make changes to their software format, its packaging, and download sites for distribution over time. Any of these can cause recipes to require updates to keep in sync. AutoPkg is designed to make it easy to "pull" updated shared recipes using the `autopkg repo-update` command. Some admins run `autopkg repo-update all` to easily update all of the recipes they may have added, which could be risky.

A bad actor could initially share an innocuous recipe that behaves exactly as expected, and then later update the recipe to do something malicious, hoping you won't notice the changes. Ideally, AutoPkg admins should re-audit any changed recipes they use, but when doing `autopkg repo-update all` might be overwhelmed with the huge number of potentially-irrelevant changes to sift through.

### Parent Trust Info

AutoPkg 1.0 introduced a new mechanism and some new tools to help with these issues. When creating a recipe override, certain information about the parent recipe(s) and the processors they use is stored in the recipe override. If a parent recipe or the non-core processors used by the parent recipes change after the override is created, running the recipe override will fail with an error. This is your cue to audit the changes for that recipe to make sure nothing unexpected has been introduced.

#### Storing Trust Info

Parent recipe trust info is stored when creating a new recipe override with `autopkg make-override some_recipe_name`. You can add or update parent recipe trust info for an existing recipe override with `autopkg update-trust-info some_recipe_name`.

#### Verifying Trust Info

If there is trust information stored for a recipe, it is automatically verified every time you run the recipe. You can also manually verify trust information with `autopkg verify-trust-info some_recipe_name`. The default output is very brief and simply indicates success or failure to verify. Add one or more `-v` flags to the command to get additional detail about why verification fails. If you wish to verify a list of recipes that you have stored in a text file (e.g., [AutoPkgr](https://github.com/lindegroup/autopkgr) users), use the `--recipe-list` option with the path to the text file.

#### Making trust verification more strict

By default, if a recipe override does not have any trust info stored (or you attempt to run a shared recipe without an override), it will run after printing a brief warning. 

```
autopkg run MakeCatalogs.munki
Processing MakeCatalogs.munki...
WARNING: MakeCatalogs.munki is missing trust info and FAIL_RECIPES_WITHOUT_TRUST_INFO is not set. Proceeding...
```

You can make AutoPkg refuse to run shared recipes that do not have any trust info by setting FAIL_RECIPES_WITHOUT_TRUST_INFO. You can do that in AutoPkg's preferences:

```
defaults write com.github.autopkg FAIL_RECIPES_WITHOUT_TRUST_INFO -bool YES
```

or at the command-line using the `-k`flag:

```
autopkg run OracleJava10.munki -k FAIL_RECIPES_WITHOUT_TRUST_INFO=yes
```

Enabling this setting will also cause any recipe that has changed since trust was established to fail. This is considered best practice.

Note: If you have enabled FAIL_RECIPES_WITHOUT_TRUST_INFO using AutoPkg's preferences, you cannot override that setting when running a recipe from the command line using `-k FAIL_RECIPES_WITHOUT_TRUST_INFO=no`. If you wish to turn off strict trust verification for a short while (e.g., while testing new or changed recipes), you may either disable the appropriate AutoPkg preference for the duration required:

```
defaults write com.github.autopkg FAIL_RECIPES_WITHOUT_TRUST_INFO -bool NO
```

or use the `--ignore-parent-trust-verification-errors` option from the command line on each run:

```
autopkg run --ignore-parent-trust-verification-errors Foo.download
```

### Workflow at a glance

Here's an example 'big picture' expected workflow:

1. Admin adds a new recipe repo to be able to fetch a product named Foo, specifically to produce a package, which we'll refer to as Foo.pkg.recipe. They examine (e.g. with the `audit` verb mentioned in the [Introduction section](https://github.com/autopkg/autopkg/wiki/AutoPkg-and-recipe-parent-trust-info#introduction) above) and test the recipe to confirm it behaves as expected
1. Admin creates an override for the recipe with `autopkg make-override Foo.pkg` (`.recipe` is optional with many autopkg verbs). This indicates that, since the admin trusts the results of running the recipe currently, they want to 'fingerprint'/produce a hash of the recipe and any parent recipes used as part of Foo.pkg.recipe (if any), and any custom processors used. (They may also optionally take this opportunity to override values (also referred to as variables) in the INPUT dictionary section of the recipe by customizing them in the override)
1. AutoPkg automatically uses the override on subsequent Foo.pkg recipe runs (either individually, or as part of a recipe list)
1. The admin periodically checks or otherwise later learns of an update having been committed/pushed to GitHub by the maintainer, and runs `autopkg repo-update foorepo-recipes` to retrieve the change, which will update their local copy
1. On the next run of Foo.pkg.recipe, it would be stopped with an error because the parent recipe (or any associated changed custom processor) no longer matches the stored fingerprint(s) in the override
1. The admin can then use `autopkg verify-trust-info -vv Foo.pkg` to get additional detail. They are encouraged to use this information to inspect the changes, perhaps looking at the git commit message and asking for help with interpreting what the changes mean (if desired) in the [#autopkg channel](https://macadmins.slack.com/archives/C056155B4) in MacAdmins Slack
1. The admin can then confirm that the new recipe still meets their needs, and would therefore update the stored trust information for the recipe with `autopkg update-trust-info Foo.pkg`

### Summary

Parent trust info provides a mechanism by which the AutoPkg admin can be alerted to changes in the shared recipes they use. AutoPkg will alert the admin upon any changes to the parent recipes and/or custom processors used by the recipe.