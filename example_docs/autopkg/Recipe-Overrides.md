Overrides are how you configure certain exposed "Input variables" for a recipe, where you can customize the configuration for your environment. This allows for a recipe to be later updated by its maintainer(s) without overwriting your own local configuration changes. You can think of them somewhat like the ".local" config file pattern found throughout UNIX programs that are configured via text files, where you inherit a default configuration but can override specifics.

For example, if the recipe is Firefox, perhaps you want to fetch a different language version. If the recipe is designed for use with Munki, you will likely want to specify a specific location in your repo's file hierarchy, or modify certain pkginfo keys.

Another important role for recipe overrides is storing [recipe parent trust information](AutoPkg-and-recipe-parent-trust-info). As of AutoPkg 1.0, it is expected that you will create overrides for every recipe you run in production so that you can audit changes in parent recipes and non-core processors.

## Getting info

Run `autopkg info [name](recipe)` to print out some useful info about the recipe:

```
Description:         Downloads Firefox disk image and imports into Munki.
                     Values for FIREFOX_BUILD correspond to directories here: http://download-origin.cdn.mozilla.net/pub/mozilla.org/firefox/releases/
                     Some useful values are: 'latest', 'latest-10.0esr', 'latest-esr', 'latest-3.6', 'latest-beta'
                     LOCALE corresponds to directories at http://download-origin.cdn.mozilla.net/pub/mozilla.org/firefox/releases/$FIREFOX_BUILD/mac/
                     Examples include 'en-US', 'de', 'ja-JP-mac', 'sv-SE', and 'zh-TW'
                     No idea if all Firefox builds are available in all the same localizations, so you may need to verify that any particular
                     combination is offered.
Identifier:          com.github.autopkg.munki.firefox-rc-en_US
Munki import recipe: True
Has check phase:     True
Builds package:      False
Recipe file path:    /Users/cadmin/Library/AutoPkg/RecipeRepos/com.github.autopkg.recipes/Mozilla/Firefox.munki.recipe
Parent recipe(s):    /Users/cadmin/Library/AutoPkg/RecipeRepos/com.github.autopkg.recipes/Mozilla/Firefox.download.recipe
Input values:

    LOCALE = "en_US";
    "MUNKI_REPO_SUBDIR" = "apps/firefox";
    NAME = Firefox;
    RELEASE = latest;
    pkginfo =     {
        catalogs =         (
            testing
        );
        description = "Mozilla Firefox is a free and open source web browser.";
        "display_name" = "Mozilla Firefox";
        name = "%NAME%";
        "unattended_install" = 1;
    };
```

## Override file

Most of the time you will want to store your local changes in a file so that you only need to specify the recipe name when you want to run it, and it will automatically use your set of defined Input variables.

### Making an override

Use the `make-override` verb to generate a template override file (plist format by default), which will be saved to the currently-configured override search location:

```
autopkg make-override Firefox.munki
Override file saved to /Users/cadmin/Library/AutoPkg/RecipeOverrides/Firefox.munki.recipe.
```

Let's examine its contents:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Identifier</key>
    <string>local.munki.Firefox</string>
    <key>Input</key>
    <dict>
        <key>DISABLE_CODE_SIGNATURE_VERIFICATION</key>
        <false/>
        <key>LOCALE</key>
        <string>en-US</string>
        <key>MUNKI_REPO_SUBDIR</key>
        <string>apps/firefox</string>
        <key>NAME</key>
        <string>Firefox</string>
        <key>RELEASE</key>
        <string>latest</string>
        <key>pkginfo</key>
        <dict>
            <key>catalogs</key>
            <array>
                <string>testing</string>
            </array>
            <key>description</key>
            <string>Mozilla Firefox is a free and open source web browser.</string>
            <key>display_name</key>
            <string>Mozilla Firefox</string>
            <key>name</key>
            <string>%NAME%</string>
            <key>unattended_install</key>
            <true/>
        </dict>
    </dict>
    <key>ParentRecipe</key>
    <string>com.github.autopkg.munki.firefox-rc-en_US</string>
    <key>ParentRecipeTrustInfo</key>
    <dict>
        <key>non_core_processors</key>
        <dict>
            <key>MozillaURLProvider</key>
            <dict>
                <key>git_hash</key>
                <string>92758e3756ac9f090e69531b0821ebf1842c899c</string>
                <key>path</key>
                <string>~/Library/AutoPkg/RecipeRepos/com.github.autopkg.recipes/Mozilla/MozillaURLProvider.py</string>
                <key>sha256_hash</key>
                <string>9f9ae9a7416e59067ba92dde475b925595daa9ac436e82467e1b97bacbb6856b</string>
            </dict>
        </dict>
        <key>parent_recipes</key>
        <dict>
            <key>com.github.autopkg.download.firefox-rc-en_US</key>
            <dict>
                <key>git_hash</key>
                <string>10541f07e781358fc489c1ed615de9ce85ee95a5</string>
                <key>path</key>
                <string>~/Library/AutoPkg/RecipeRepos/com.github.autopkg.recipes/Mozilla/Firefox.download.recipe</string>
                <key>sha256_hash</key>
                <string>25f3d12e7586fb4970fb469b45a2b37f4aa0bc4a549ea93f082c77f1b4439d60</string>
            </dict>
            <key>com.github.autopkg.munki.firefox-rc-en_US</key>
            <dict>
                <key>git_hash</key>
                <string>10541f07e781358fc489c1ed615de9ce85ee95a5</string>
                <key>path</key>
                <string>~/Library/AutoPkg/RecipeRepos/com.github.autopkg.recipes/Mozilla/Firefox.munki.recipe</string>
                <key>sha256_hash</key>
                <string>59a32356ec309af8e562c5062f379adb95fb97e2a64c681f341521a7846c63d9</string>
            </dict>
        </dict>
    </dict>
</dict>
</plist>
```

### Input keys and merging

The `Input` key is a complete copy of that of the source recipe's, which you may modify to suit your needs. When a recipe is run, each key in the override's `Input` dict will be merged on top of the recipe's (hence the name "override").

You may _also_ wish to remove the override's `Input` keys altogether, and instead let AutoPkg use the values that are defined in the original recipe. For example, for recipes with a stable, known download URL, this URL may be present as an Input variable so that it is easily customizable. All URLs will eventually break and need to be fixed, however, and you may wish to leave it out of your override file entirely if you expect it to be fixed quickly by the recipe maintainer. In other words, if you wish, you may reduce your override's `Input` items to include _only the items you wish to change from the defaults_ set by the recipe.

The `ParentRecipe` key points AutoPkg to the identifier of the recipe for which this is an override. In fact, an override is no different from a child recipe in its structure and its logic as to how its contents inherit and override its parent's.

### Testing the override

To test the override, open the new override file that was saved to `Library/AutoPkg/RecipeOverrides/Firefox.munki.recipe` with a text editor, and change something. For example, we can change `RELEASE` to `latest-esr`. Save the changes. Now run `autopkg info Firefox.munki` again and look at what's changed (we're cutting out some redundant parts in this sample output below):

```
---
Identifier:          local.munki.Firefox
Munki import recipe: True
Has check phase:     True
Builds package:      False
Recipe file path:    /Users/cadmin/Library/AutoPkg/RecipeOverrides/Firefox.munki.recipe
Parent recipe(s):    /Users/cadmin/Library/AutoPkg/RecipeRepos/com.github.autopkg.recipes/Mozilla/Firefox.munki.recipe
                     /Users/cadmin/Library/AutoPkg/RecipeRepos/com.github.autopkg.recipes/Mozilla/Firefox.download.recipe
Input values:

    LOCALE = "en_US";
    "MUNKI_REPO_SUBDIR" = "apps/firefox";
    NAME = Firefox;
    RELEASE = "latest-esr";
---
```

Verify first that `RELEASE` is set to our overridden value.

More interestingly, notice that the Recipe file path has changed from its source recipe file in `RecipeRepos` to the path of our override. This is because an override is actually a child recipe, in exactly the same way that `Firefox.munki` is a child recipe of the `Firefox.download` recipe.


## Command-line: the -k/--key option

A second way to override any input variable is at the command line using the `--key` option:

    autopkg run \
      --key MUNKI_REPO_SUBDIR=some/custom/location \
      --key RELEASE=latest-esr \
      Firefox.munki

Any overrides given at the command line will always take precedence over those present in an override file. You might use this to re-run a recipe but retrieve an alternate beta release, specify a different `MUNKI_REPO` value for testing a recipe, etc.

Note that this option only reliably works for `<string>` input variables, as `--key` can only set strings. While AutoPkg _may_ successfully convert a string to other variable types, it could require a very specific syntax to do so (e.g., [FAIL_RECIPES_WITHOUT_TRUST_INFO](https://github.com/autopkg/autopkg/wiki/AutoPkg-and-recipe-parent-trust-info#making-trust-verification-more-strict)).

## Recipe override directories

Recipe overrides are saved to the recipe override directory.

1. The default recipe override directory is `~/Library/AutoPkg/RecipeOverrides`
1. You may set the RECIPE_OVERRIDE_DIRS [[preference|Preferences]] to an array of directories instead. All directories defined here will be searched when running recipes, but new overrides will be saved only to the first directory in the list.
1. You may also specify an alternate recipe override directory using the `--override-dir` option to `autopkg`
