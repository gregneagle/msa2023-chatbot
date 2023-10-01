#### A brief "getting started" tutorial

Some parts of this short tutorial assume you have a working Munki repo configured that you can mount from your admin machine. Munki isn't strictly required to use AutoPkg - for example, it can simply build packages. If you aren't using Munki, there are additional processors you can add on to work with [Jamf Pro](https://github.com/grahampugh/jamf-upload/tree/main/JamfUploaderProcessors), LANrev, Filewave, SCCM, BigFix, and more. But Munki is free and open source, so we'll use it for this demonstration.

## Installation and configuration on macOS

AutoPkg is distributed as an installer package, and it's recommended to also install Git for the purpose of installing and updating community recipes. AutoPkg requires macOS 10.6 or later.

### Install AutoPkg

Install the [latest pkg release](https://github.com/autopkg/autopkg/releases/latest). This will also install and load a LaunchDaemon used by AutoPkg's packaging component. This allows AutoPkg to build packages without requiring root privileges.

### Install Git

Git is used by AutoPkg to add new community recipe repos, and to keep them up to date. One way to install Git is to install the Xcode Command Line tools. On Mavericks or higher, you can prompt the system to install them simply by typing the `git` command, or `xcode-select --install`. If you have installed Xcode, you already have Git. Git is also available via the [official Git installer package](https://git-scm.com/download/mac).

### Optional: configure for use with Munki

If we're using Munki, we must also define the `MUNKI_REPO` preference as the path where the Munki repository is mounted:

`defaults write com.github.autopkg MUNKI_REPO /path/to/munki_repo`

Also, ensure the latest [Munki tools](https://github.com/munki/munki/releases/latest) are installed.

### Install some recipes

    autopkg repo-add recipes

You'll see something like:

    Attempting git clone...
    Cloning into '/Users/gneagle/Library/AutoPkg/RecipeRepos/com.github.autopkg.recipes'...

    Adding /Users/gneagle/Library/AutoPkg/RecipeRepos/com.github.autopkg.recipes to RECIPE_SEARCH_DIRS...
    Recipe search path is: (
        ".",
        "~/Library/AutoPkg/Recipes",
        "/Library/AutoPkg/Recipes",
        "/Users/gneagle/Library/AutoPkg/RecipeRepos/com.github.autopkg.recipes"
    )

Now look at what recipes are available:

    autopkg list-recipes

You should see a list of available recipes:

    Adium.munki
    Adium.pkg
    AdobeAIR.pkg
    AdobeAcrobatPro9Update.munki
    AdobeAcrobatProXUpdate.munki
    AdobeAir.munki
    AdobeFlashPlayer.munki
    AdobeFlashPlayer.pkg

..and so on.

You can get info on a specific recipe:

    % autopkg info GoogleChrome.pkg
    Description:         Downloads latest Google Chrome disk image and builds a package.
    Munki import recipe: False
    Has check phase:     True
    Builds package:      True
    Recipe file path:    /Users/gneagle/Library/AutoPkg/RecipeRepos/com.github.autopkg.recipes/GoogleChrome/GoogleChrome.pkg.recipe
    Input values:

        "DOWNLOAD_URL" = "https://dl.google.com/chrome/mac/stable/GGRO/googlechrome.dmg";
        IDENTIFIER = "com.github.autopkg.pkg.googlechrome";
        NAME = GoogleChrome;

## Running a recipe

In our first example we'll run `autopkg` with a full path to a recipe. Note the `-v` verbosity flag, which will print out some useful progress information:

    % autopkg run -v ~/Library/AutoPkg/RecipeRepos/com.github.autopkg.recipes/GoogleChrome/GoogleChrome.pkg.recipe
    Processing /Users/gneagle/Library/AutoPkg/RecipeRepos/com.github.autopkg.recipes/GoogleChrome/GoogleChrome.pkg.recipe...
    WARNING: /Users/gneagle/Library/AutoPkg/RecipeRepos/com.github.autopkg.recipes/GoogleChrome/GoogleChrome.pkg.recipe is missing trust info and FAIL_RECIPES_WITHOUT_TRUST_INFO is not set. Proceeding...
    URLDownloader
    URLDownloader: Storing new Last-Modified header: Sat, 20 Feb 2021 06:12:11 GMT
    URLDownloader: Storing new ETag header: "870ab9"
    URLDownloader: Downloaded /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.pkg.googlechrome/downloads/GoogleChrome.dmg
    EndOfCheckPhase
    CodeSignatureVerifier
    CodeSignatureVerifier: Mounted disk image /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.pkg.googlechrome/downloads/GoogleChrome.dmg
    CodeSignatureVerifier: Verifying code signature...
    CodeSignatureVerifier: Deep verification enabled...
    CodeSignatureVerifier: Strict verification disabled...
    CodeSignatureVerifier: /private/tmp/dmg.a65dzP/Google Chrome.app: valid on disk
    CodeSignatureVerifier: /private/tmp/dmg.a65dzP/Google Chrome.app: satisfies its Designated Requirement
    CodeSignatureVerifier: /private/tmp/dmg.a65dzP/Google Chrome.app: explicit requirement satisfied
    CodeSignatureVerifier: Signature is valid
    AppDmgVersioner
    AppDmgVersioner: Mounted disk image /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.pkg.googlechrome/downloads/GoogleChrome.dmg
    AppDmgVersioner: BundleID: com.google.Chrome
    AppDmgVersioner: Version: 88.0.4324.192
    PkgRootCreator
    PkgRootCreator: Created /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.pkg.googlechrome/GoogleChrome
    PkgRootCreator: Created /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.pkg.googlechrome/GoogleChrome/Applications
    Copier
    Copier: Mounted disk image /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.pkg.googlechrome/downloads/GoogleChrome.dmg
    Copier: Copied /private/tmp/dmg.rrS4hS/Google Chrome.app to /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.pkg.googlechrome/GoogleChrome/Applications/Google Chrome.app
    PkgCreator
    PkgCreator: Connecting
    PkgCreator: Sending packaging request
    PkgCreator: Disconnecting
    Receipt written to /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.pkg.googlechrome/receipts/GoogleChrome.pkg-receipt-20210228-125144.plist

    The following new items were downloaded:
        Download Path
        -------------
        /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.pkg.googlechrome/downloads/GoogleChrome.dmg

    The following packages were built:
        Identifier         Version        Pkg Path
        ----------         -------        --------
        com.google.Chrome  88.0.4324.192  /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.pkg.googlechrome/GoogleChrome-88.0.4324.192.pkg

Each line of status above is prefixed with a "processor", which are a list of tasks to perform in the recipe. The GoogleChrome.pkg recipe is fairly simple:

1. `URLDownloader` downloads a file at a given URL, and also records available header information given by the web server.
1. `EndOfCheckPhase` is used only to mark the place in the recipe that constitutes a "check" without doing any further processing. This is used when the `--check` option is given to `autopkg`.
1. `AppDmgVersioner` peeks inside the disk image and extracts the BundleID and version from the application.
1. `PkgRootCreator` creates a root directory in which to stage our new package's contents.
1. `Copier` copies files from the disk image to the pkg root directory.
1. `PkgCreator` sends a packaging request to the autopkgserver, which builds a package for us.

The verbosity level can be increased to expose more internal data.

You may also notice warnings about missing trust info. Those warnings are only warnings and won't stop the AutoPkg recipe from running. That said, it is more secure to make a recipe override and update trust info for recipes. More details at [AutoPkg and recipe parent trust info](https://github.com/autopkg/autopkg/wiki/AutoPkg-and-recipe-parent-trust-info)

### Running a recipe by name

While you can provide a full path to a recipe to run it, you can also just use the recipe name that appears in the output of `autopkg list-recipes`, which is a more convenient way to specify a recipe to run. This time, let's run a Munki recipe.

    % autopkg run -v GoogleChrome.munki
    Processing GoogleChrome.munki...
    WARNING: GoogleChrome.munki is missing trust info and FAIL_RECIPES_WITHOUT_TRUST_INFO is not set. Proceeding...
    URLDownloader
    URLDownloader: Storing new Last-Modified header: Sat, 20 Feb 2021 06:12:11 GMT
    URLDownloader: Storing new ETag header: "870ab9"
    URLDownloader: Downloaded /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.munki.google-chrome/downloads/GoogleChrome.dmg
    EndOfCheckPhase
    CodeSignatureVerifier
    CodeSignatureVerifier: Mounted disk image /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.munki.google-chrome/downloads/GoogleChrome.dmg
    CodeSignatureVerifier: Verifying code signature...
    CodeSignatureVerifier: Deep verification enabled...
    CodeSignatureVerifier: Strict verification disabled...
    CodeSignatureVerifier: /private/tmp/dmg.5fYvik/Google Chrome.app: valid on disk
    CodeSignatureVerifier: /private/tmp/dmg.5fYvik/Google Chrome.app: satisfies its Designated Requirement
    CodeSignatureVerifier: /private/tmp/dmg.5fYvik/Google Chrome.app: explicit requirement satisfied
    CodeSignatureVerifier: Signature is valid
    MunkiImporter
    MunkiImporter: Using repo lib: AutoPkgLib
    MunkiImporter:         plugin: FileRepo
    MunkiImporter:           repo: /Users/Shared/munki_repo
    MunkiImporter: Copied pkginfo to: /Users/Shared/munki_repo/pkgsinfo/apps/GoogleChrome-88.0.4324.192.plist
    MunkiImporter:            pkg to: /Users/Shared/munki_repo/pkgs/apps/GoogleChrome-88.0.4324.192.dmg
    Receipt written to /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.munki.google-chrome/receipts/GoogleChrome-receipt-20210228-125436.plist

    The following new items were downloaded:
        Download Path
        -------------
        /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.munki.google-chrome/downloads/GoogleChrome.dmg

    The following new items were imported into Munki:
        Name          Version        Catalogs  Pkginfo Path                           Pkg Repo Path                        Icon Repo Path
        ----          -------        --------  ------------                           -------------                        --------------
        GoogleChrome  88.0.4324.192  testing   apps/GoogleChrome-88.0.4324.192.plist  apps/GoogleChrome-88.0.4324.192.dmg

This recipe does a few things differently from the GoogleChrome.pkg recipe.
Since Munki doesn't need Chrome to be repackaged, this recipe simply downloads the latest disk image and imports it into Munki. It does not, however, run `makecatalogs` (which, if you manage a Munki repo, you know is a very important step!) For now, we'll do that manually:

    /usr/local/munki/makecatalogs

Later we'll see how we can automate this step as well.

## Repeated runs and idempotence

Now, run the same command again: `autopkg run -v GoogleChrome.munki`

    % autopkg run -v GoogleChrome.munki
    Processing GoogleChrome.munki...
    WARNING: GoogleChrome.munki is missing trust info and FAIL_RECIPES_WITHOUT_TRUST_INFO is not set. Proceeding...
    URLDownloader
    URLDownloader: Item at URL is unchanged.
    URLDownloader: Using existing /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.munki.google-chrome/downloads/GoogleChrome.dmg
    EndOfCheckPhase
    CodeSignatureVerifier
    CodeSignatureVerifier: Mounted disk image /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.munki.google-chrome/downloads/GoogleChrome.dmg
    CodeSignatureVerifier: Verifying code signature...
    CodeSignatureVerifier: Deep verification enabled...
    CodeSignatureVerifier: Strict verification disabled...
    CodeSignatureVerifier: /private/tmp/dmg.PczqqM/Google Chrome.app: valid on disk
    CodeSignatureVerifier: /private/tmp/dmg.PczqqM/Google Chrome.app: satisfies its Designated Requirement
    CodeSignatureVerifier: /private/tmp/dmg.PczqqM/Google Chrome.app: explicit requirement satisfied
    CodeSignatureVerifier: Signature is valid
    MunkiImporter
    MunkiImporter: Using repo lib: AutoPkgLib
    MunkiImporter:         plugin: FileRepo
    MunkiImporter:           repo: /Users/Shared/munki_repo
    MunkiImporter: Item GoogleChrome.dmg already exists in the munki repo as pkgs/apps/GoogleChrome-88.0.4324.192.dmg.
    Receipt written to /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.munki.google-chrome/receipts/GoogleChrome-receipt-20210228-125856.plist

    Nothing downloaded, packaged or imported.

(If you don't see something similar to the above, you probably didn't run `makecatalogs` as directed above!)

Both the `URLDownloader` and `MunkiImporter` processors contain internal logic to be able to determine whether their task has already been completed, and that they don't need to re-download or re-import the items. To verify that this is the case, try the following:

1. Delete the newly-imported GoogleChrome pkginfo plist (and if you'd like, the dmg), run `makecatalogs`, and re-run `autopkg run -v GoogleChrome.munki`. It should verify that cached item is unchanged, but that it is missing from the Munki repo, and import it.
1. Delete the cached item found in the `~/Library/AutoPkg/Cache` directory, and re-run `autopkg run -v GoogleChrome.munki`. It should re-cache the file, and as long as the version in the Munki repo matches, it should not re-import.
1. Repeat 2., but give the `--check` option to `autopkg`. This will cause it to re-cache the file and report the download, but not proceed past the `EndOfCheckPhase` processor.

**Note:** The `MunkiImporter` processor also supports an input variable called `force_munkiimport`, that forces an import if it's set (to anything). This might be useful in testing modifications to recipes. This can be set temporarily using the `-k/--key` option, as in the example below. For info on this override method [here](https://github.com/autopkg/autopkg/wiki/Recipe-Overrides#command-line-the--k--key-option).

`autopkg run -k force_munkiimport=yes Recipe`

## Running multiple recipes

AutoPkg can run more than one recipe in a given session.

One of the recipes available in the [autopkg/recipes](https://github.com/autopkg/recipes) recipe repo is "MakeCatalogs.munki". It does what you'd expect, but it's behavior is more subtle than just running `makecatalogs`. By default, it checks the results of any recipes that were run in the same session and only does a `makecatalogs` if something new was imported into the Munki repo. So running this recipe by itself is generally not very useful:

    % autopkg run -v MakeCatalogs.munki
    Processing MakeCatalogs.munki...
    WARNING: MakeCatalogs.munki is missing trust info and FAIL_RECIPES_WITHOUT_TRUST_INFO is not set. Proceeding...
    MakeCatalogsProcessor
    MakeCatalogsProcessor: No need to rebuild catalogs.
    Receipt written to /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.munki.makecatalogs/receipts/MakeCatalogs-receipt-20210228-130125.plist

    Nothing downloaded, packaged or imported.

But if you add this recipe to the end of a run of other recipes that do import something, it does the right thing:

    % autopkg run -v Firefox.munki Thunderbird.munki MakeCatalogs.munki
    Processing Firefox.munki...
    MozillaURLProvider
    MozillaURLProvider: Found URL https://download.mozilla.org/?product=firefox-latest-ssl&os=osx&lang=en-US
    URLDownloader
    URLDownloader: Item at URL is unchanged.
    URLDownloader: Using existing /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.munki.firefox-rc-en_US/downloads/Firefox.dmg
    EndOfCheckPhase
    CodeSignatureVerifier
    CodeSignatureVerifier: Mounted disk image /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.munki.firefox-rc-en_US/downloads/Firefox.dmg
    CodeSignatureVerifier: Using path '/private/tmp/dmg.DVKWrS/Firefox.app' matched from globbed '/private/tmp/dmg.DVKWrS/Firefox*.app'.
    CodeSignatureVerifier: Verifying code signature...
    CodeSignatureVerifier: Deep verification enabled...
    CodeSignatureVerifier: Strict verification not defined. Using codesign defaults...
    CodeSignatureVerifier: /private/tmp/dmg.DVKWrS/Firefox.app: valid on disk
    CodeSignatureVerifier: /private/tmp/dmg.DVKWrS/Firefox.app: satisfies its Designated Requirement
    CodeSignatureVerifier: /private/tmp/dmg.DVKWrS/Firefox.app: explicit requirement satisfied
    CodeSignatureVerifier: Signature is valid
    MunkiImporter
    MunkiImporter: Using repo lib: AutoPkgLib
    MunkiImporter:         plugin: FileRepo
    MunkiImporter:           repo: /Users/Shared/munki_repo
    MunkiImporter: Copied pkginfo to: /Users/Shared/munki_repo/pkgsinfo/apps/firefox/Firefox-86.0.plist
    MunkiImporter:            pkg to: /Users/Shared/munki_repo/pkgs/apps/firefox/Firefox-86.0.dmg
    Receipt written to /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.munki.firefox-rc-en_US/receipts/Firefox-receipt-20210228-130439.plist
    Processing Thunderbird.munki...
    WARNING: Thunderbird.munki is missing trust info and FAIL_RECIPES_WITHOUT_TRUST_INFO is not set. Proceeding...
    MozillaURLProvider
    MozillaURLProvider: Found URL https://download.mozilla.org/?product=thunderbird-latest-ssl&os=osx&lang=en-US
    URLDownloader
    URLDownloader: Item at URL is unchanged.
    URLDownloader: Using existing /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.munki.thunderbird/downloads/Thunderbird.dmg
    EndOfCheckPhase
    CodeSignatureVerifier
    CodeSignatureVerifier: Mounted disk image /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.munki.thunderbird/downloads/Thunderbird.dmg
    CodeSignatureVerifier: Verifying code signature...
    CodeSignatureVerifier: Deep verification enabled...
    CodeSignatureVerifier: Strict verification not defined. Using codesign defaults...
    CodeSignatureVerifier: /private/tmp/dmg.spicFe/Thunderbird.app: valid on disk
    CodeSignatureVerifier: /private/tmp/dmg.spicFe/Thunderbird.app: satisfies its Designated Requirement
    CodeSignatureVerifier: /private/tmp/dmg.spicFe/Thunderbird.app: explicit requirement satisfied
    CodeSignatureVerifier: Signature is valid
    MunkiImporter
    MunkiImporter: Using repo lib: AutoPkgLib
    MunkiImporter:         plugin: FileRepo
    MunkiImporter:           repo: /Users/Shared/munki_repo
    MunkiImporter: Copied pkginfo to: /Users/Shared/munki_repo/pkgsinfo/apps/thunderbird/Thunderbird-78.8.0.plist
    MunkiImporter:            pkg to: /Users/Shared/munki_repo/pkgs/apps/thunderbird/Thunderbird-78.8.0.dmg
    Receipt written to /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.munki.thunderbird/receipts/Thunderbird-receipt-20210228-130457.plist
    Processing MakeCatalogs.munki...
    WARNING: MakeCatalogs.munki is missing trust info and FAIL_RECIPES_WITHOUT_TRUST_INFO is not set. Proceeding...
    MakeCatalogsProcessor
    MakeCatalogsProcessor: Munki catalogs rebuilt!
    Receipt written to /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.munki.makecatalogs/receipts/MakeCatalogs-receipt-20210228-130500.plist

    The following new items were imported into Munki:
        Name         Version  Catalogs  Pkginfo Path                               Pkg Repo Path                            Icon Repo Path
        ----         -------  --------  ------------                               -------------                            --------------
        Firefox      86.0     testing   apps/firefox/Firefox-86.0.plist            apps/firefox/Firefox-86.0.dmg
        Thunderbird  78.8.0   testing   apps/thunderbird/Thunderbird-78.8.0.plist  apps/thunderbird/Thunderbird-78.8.0.dmg

You can see it downloaded and imported Firefox, then Thunderbird, then rebuilt the Munki catalogs.
If we run these recipes again, we see it skips the tasks that are not needed:

    % autopkg run -v Firefox.munki Thunderbird.munki MakeCatalogs.munki
    Processing Firefox.munki...
    MozillaURLProvider
    MozillaURLProvider: Found URL https://download.mozilla.org/?product=firefox-latest-ssl&os=osx&lang=en-US
    URLDownloader
    URLDownloader: Item at URL is unchanged.
    URLDownloader: Using existing /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.munki.firefox-rc-en_US/downloads/Firefox.dmg
    EndOfCheckPhase
    CodeSignatureVerifier
    CodeSignatureVerifier: Mounted disk image /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.munki.firefox-rc-en_US/downloads/Firefox.dmg
    CodeSignatureVerifier: Using path '/private/tmp/dmg.3hJzxP/Firefox.app' matched from globbed '/private/tmp/dmg.3hJzxP/Firefox*.app'.
    CodeSignatureVerifier: Verifying code signature...
    CodeSignatureVerifier: Deep verification enabled...
    CodeSignatureVerifier: Strict verification not defined. Using codesign defaults...
    CodeSignatureVerifier: /private/tmp/dmg.3hJzxP/Firefox.app: valid on disk
    CodeSignatureVerifier: /private/tmp/dmg.3hJzxP/Firefox.app: satisfies its Designated Requirement
    CodeSignatureVerifier: /private/tmp/dmg.3hJzxP/Firefox.app: explicit requirement satisfied
    CodeSignatureVerifier: Signature is valid
    MunkiImporter
    MunkiImporter: Using repo lib: AutoPkgLib
    MunkiImporter:         plugin: FileRepo
    MunkiImporter:           repo: /Users/Shared/munki_repo
    MunkiImporter: Item Firefox.dmg already exists in the munki repo as pkgs/apps/firefox/Firefox-86.0.dmg.
    Receipt written to /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.munki.firefox-rc-en_US/receipts/Firefox-receipt-20210228-130655.plist
    Processing Thunderbird.munki...
    WARNING: Thunderbird.munki is missing trust info and FAIL_RECIPES_WITHOUT_TRUST_INFO is not set. Proceeding...
    MozillaURLProvider
    MozillaURLProvider: Found URL https://download.mozilla.org/?product=thunderbird-latest-ssl&os=osx&lang=en-US
    URLDownloader
    URLDownloader: Item at URL is unchanged.
    URLDownloader: Using existing /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.munki.thunderbird/downloads/Thunderbird.dmg
    EndOfCheckPhase
    CodeSignatureVerifier
    CodeSignatureVerifier: Mounted disk image /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.munki.thunderbird/downloads/Thunderbird.dmg
    CodeSignatureVerifier: Verifying code signature...
    CodeSignatureVerifier: Deep verification enabled...
    CodeSignatureVerifier: Strict verification not defined. Using codesign defaults...
    CodeSignatureVerifier: /private/tmp/dmg.9lZgtt/Thunderbird.app: valid on disk
    CodeSignatureVerifier: /private/tmp/dmg.9lZgtt/Thunderbird.app: satisfies its Designated Requirement
    CodeSignatureVerifier: /private/tmp/dmg.9lZgtt/Thunderbird.app: explicit requirement satisfied
    CodeSignatureVerifier: Signature is valid
    MunkiImporter
    MunkiImporter: Using repo lib: AutoPkgLib
    MunkiImporter:         plugin: FileRepo
    MunkiImporter:           repo: /Users/Shared/munki_repo
    MunkiImporter: Item Thunderbird.dmg already exists in the munki repo as pkgs/apps/thunderbird/Thunderbird-78.8.0.dmg.
    Receipt written to /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.munki.thunderbird/receipts/Thunderbird-receipt-20210228-130713.plist
    Processing MakeCatalogs.munki...
    WARNING: MakeCatalogs.munki is missing trust info and FAIL_RECIPES_WITHOUT_TRUST_INFO is not set. Proceeding...
    MakeCatalogsProcessor
    MakeCatalogsProcessor: No need to rebuild catalogs.
    Receipt written to /Users/gneagle/Library/AutoPkg/Cache/com.github.autopkg.munki.makecatalogs/receipts/MakeCatalogs-receipt-20210228-130715.plist

    Nothing downloaded, packaged or imported.

This behavior keeps autopkg from re-importing the same items over and over into the Munki repo and from running `makecatalogs` unnecessarily.

You can also run a list of recipes at once by using the `--recipe-list` parameter, and giving the path to a text file which contains a single recipe on each line:

    % autopkg run -v --recipe-list Recipes.txt

A valid text file would be:

    Firefox.munki
    Thunderbird.munki
    MakeCatalogs.munki

## What's next?

Recipes include defaults for their input variables, but it's generally assumed that any recipe used in production will need to have some things overridden. For example, no two Munki repos follow exactly the same directory structure, so Munki recipes will likely want to at least override the destination subdirectory for the pkg/pkginfo files. Visit the [Recipe Overrides](https://github.com/autopkg/autopkg/wiki/Recipe-Overrides) page to learn more.
