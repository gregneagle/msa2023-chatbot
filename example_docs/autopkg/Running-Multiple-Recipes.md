## Options for running multiple recipes with AutoPkg

`autopkg` has a several mechanisms for running multiple recipes in a single command invocation.


### Multiple arguments

`autopkg run Firefox.munki TextWrangler.munki VLC.munki`


### Recipe lists

It can also take a `--recipe-list` option (or simply `-l`) pointing to a plain text file, with one recipe name per line. Lines in the text file beginning with a `#` will be treated as comments and ignored.

`autopkg run --recipe-list /path/to/recipe_list.txt`

In both cases, all downloads and imports will be performed in one operation and the summary will include all recipes:

    % autopkg run Firefox.munki BBEdit.munki VLC.munki
    Processing Firefox.munki...
    Processing BBEdit.munki...
    Processing VLC.munki...
    Processing MakeCatalogs.munki...

    The following new items were imported into Munki:
        Name     Version  Catalogs  Pkginfo Path                     Pkg Repo Path                  Icon Repo Path
        ----     -------  --------  ------------                     -------------                  --------------
        Firefox  86.0     testing   apps/firefox/Firefox-86.0.plist  apps/firefox/Firefox-86.0.dmg
        BBEdit   13.5.4   testing   apps/BBEdit/BBEdit-13.5.4.plist  apps/BBEdit/BBEdit-13.5.4.dmg
        VLC      3.0.12   testing   apps/VLC/VLC-3.0.12.plist        apps/VLC/VLC-3.0.12.dmg

You can also use the `list-recipes` verb to output a list of all recipes that were found:

`autopkg list-recipes > /path/to/list_of_all_recipes.txt`

### Plist recipe lists

AutoPkg can also accept a recipe list in a property list format when using the same `-l/--recipe-list` option, in which additional options limited to only this `autopkg run` may be stored for convenient re-use:

- [[pre/post-processors|PreAndPostProcessorSupport]]
- additional input variables that would normally be run using either the CLI `-k/--key` option (see [[Recipe-Overrides|Recipe-Overrides#command-line-the--k--key-option]]) or using a "global" preference value saved in the `com.github.autopkg` preference domain.

Here's an example of such a recipe list in property list format:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>postprocessors</key>
    <array>
        <string>io.github.hjuutilainen.VirusTotalAnalyzer/VirusTotalAnalyzer</string>
    </array>
    <key>recipes</key>
    <array>
        <string>AdobeAIR.munki</string>
        <string>AdobeFlashPlayer.munki</string>
        <string>AdobeReaderDC.munki</string>
        <string>Atom.munki</string>
        <string>BluejeansApp.munki</string>
        <string>MakeCatalogs.munki</string>
    </array>
    <key>VIRUSTOTAL_ALWAYS_REPORT</key>
    <false/>
    <key>VIRUSTOTAL_AUTO_SUBMIT</key>
    <true/>
</dict>
</plist>
```

When `autopkg run` is given this recipe list using the `-l` option, it will do the run using the additional postprocessor argument, and also set Input variables used for only this run (`VIRUSTOTAL_ALWAYS_REPORT` and `VIRUSTOTAL_AUTO_SUBMIT`, which are expected by the [VirusTotalAnalyzer processor](https://github.com/hjuutilainen/autopkg-virustotalanalyzer) to be set.

Using a plist recipe list file makes it possible to build a "run configuration" that contains options that might otherwise require a lengthy set of CLI arguments, and can support richer data types than simple strings for input variables.
