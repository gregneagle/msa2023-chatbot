#### Preferences supported by autopkg

The following preferences can be set to customize behavior of autopkg. All use the domain `com.github.autopkg`, so to set, for example, the cache directory to an alternate location:

`defaults write com.github.autopkg CACHE_DIR /path/to/cache/dir`

## Supported preferences

<table>
  <tr><th>Preference key</th><th>Type</th><th>Default</th><th>Description</th></tr>
  <tr><td>CACHE_DIR</td><td>String</td><td>~/Library/AutoPkg/Cache</td><td>Location for cached data such as downloads and unarchiving/packaging operations. Must be a volume that supports setting ownerships and permissions.</td></tr>
  <tr><td>MUNKI_REPO</td><td>String</td><td>(none)</td><td>Location where a Munki repository is mounted. `autopkg` does not handle mounting/unmounting this location for you.</td></tr>
  <tr><td>RECIPE_SEARCH_DIRS</td><td>String or array of strings</td><td>`[ '.', '~/Library/AutoPkg/Recipes', '/Library/AutoPkg/Recipes' ]`</td><td>Location(s) that are searched for recipes. If an array, they will be searched in order and the first recipe found will be used.</td></tr>
  <tr><td>RECIPE_OVERRIDE_DIRS</td><td>String or array of strings</td><td>`[ '~/Library/AutoPkg/RecipeOverrides' ]`</td><td>Same as `RECIPE_SEARCH_DIRS` but for override files.</td></tr>
<tr><td>RECIPE_REPO_DIR</td><td>String</td><td>~/Library/AutoPkg/RecipeRepos</td><td>Parent directory in which to store recipe repos added with `autopkg repo-add`.</td></tr>
<tr><td>GIT_PATH</td><td>String</td><td>(None)</td><td>Absolute path to a git binary to use for the various 'repo' subcommands using Git. This overrides the default behavior of using the first 'git' executable found in the PATH environment variable, falling back to `/usr/bin/git`.</td></tr>
<tr><td>GITHUB_TOKEN</td><td>String</td><td>(None)</td><td>GitHub personal access token (actual token, not a path to a file) for making GitHub requests without the usual rate limitation. <a href="https://github.com/autopkg/autopkg/wiki/FAQ#how-do-i-provide-a-github-personal-access-token-to-autopkg">Learn more</a>.</td></tr>
<tr><td>GITHUB_TOKEN_PATH</td><td>String</td><td>~/.autopkg_gh_token</td><td>Path to a file containing a GitHub personal access token for making GitHub requests without the usual rate limitation. <a href="https://github.com/autopkg/autopkg/wiki/FAQ#how-do-i-provide-a-github-personal-access-token-to-autopkg">Learn more</a>.</td></tr>
</table>

This is not a complete list. Processor input variables can be set as preferences this way. However keep in mind that if recipes or recipe overrides also set the same variable that those values will be what autopkg respects. You might want to read up on [recipe overrides](https://github.com/autopkg/autopkg/wiki/Recipe-Overrides) and [input variables](https://github.com/autopkg/autopkg/wiki/Input-Variables) to gain context about the interaction of variables, recipes and overrides.

# Using external preferences files

As of [AutoPkg 1.2](https://github.com/autopkg/autopkg/releases/tag/v1.2), it's possible to use an external Plist or JSON file for passing in preferences to AutoPkg, using the `--prefs` argument to each verb.

The external file must be a simple plist or JSON dictionary containing key/value pairs. They are treated identically as the macOS preference keys. AutoPkg will treat malformed preferences the same way it already does, which is to say that you may experience very unexpected results. AutoPkg expects this file to be writable, just like the macOS preferences. Operations that change the preferences, such as `autopkg repo-add` or `autopkg repo-delete` will attempt to write changes to this file, and failing to do so may result in unexpected behavior.

You may also pass in arbitrary keys just as if you had used `defaults write`, but they'll be ignored unless you have something that consumes them.

This does not replace or extend the behavior of overrides or passing in input variables using `-k`. It is only intended to allow AutoPkg to consume its preferences from a source other than the macOS preferences system.

## Converting existing preferences into an external file

The easiest way to test this is to simply copy your existing AutoPkg preferences plist somewhere else:
```
$ cp ~/Library/Preferences/com.github.autopkg.plist ~/autopkg_prefs.plist
$ defaults delete com.github.autopkg
$ autopkg repo-list --prefs ~/autopkg_prefs.plist
```

You may also use JSON to pass in the same data, if that format is easier to set up in your automation environment.
