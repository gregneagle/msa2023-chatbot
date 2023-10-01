> **NOTE: the GitHub search API has become unreliable of late.** If `autopkg search` does not find what you are looking for, or you get curl errors, consider using the GitHub website and just searching. Go to https://github.com/autopkg, and use the search field in the upper left, specifying you want to search the autopkg organization. You then may want to examine the "code" results of that search. For example: `https://github.com/search?q=org%3Aautopkg%20ThinLinc&type=code`

We encourage users who wish to share recipes they've written to [set up their own repo](Sharing-Recipes) within the [AutoPkg GitHub org](https://github.com/autopkg).

One can browse the website for recipes, but a much easier way to discover recipes is to use AutoPkg's `search` verb:

```bash
➜  autopkg search teamviewer

Name                               Repo/path
----                               ---------
TeamViewer.download.recipe         autopkg/hjuutilainen-recipes/TeamViewer/TeamViewer.download.recipe
TeamViewer.munki.recipe            autopkg/hjuutilainen-recipes/TeamViewer/TeamViewer.munki.recipe
TeamViewerQS.munki.recipe          autopkg/hjuutilainen-recipes/TeamViewer/TeamViewerQS.munki.recipe
TeamViewerQS.download.recipe       autopkg/hjuutilainen-recipes/TeamViewer/TeamViewerQS.download.recipe
```

This command is effectively running a custom [GitHub code search](https://help.github.com/articles/searching-code) with the following criteria: search only files with the file extension `.recipe`, within the user/org `autopkg`, and to search both file paths and contents. This is how the same search looks via the [GitHub website](https://github.com/search?q=teamviewer+user%3Aautopkg+path%3A%2A.recipe&type=Code&ref=advsearch&l=). 

Searching file contents in addition to paths tends to produce some inaccurate results, but file path searching alone is not fuzzy enough and tends to miss results. The `--path-only` option restricts searches to file paths only. Also, see the `--user` option to search a different GitHub user than the default `autopkg`.

A reminder that people are free to publish their recipes anywhere they wish (including private repos hosted locally or on GitHub) and AutoPkg's `repo-` commands will simply run the appropriate `git clone` and `git pull` commands.

## Improve Search Reliability with a GitHub Personal Access Token

The `autopkg search` command has been failing for some people with a HTTP request 401 error. The may be due to restrictions being set by GitHub. This can be improved by creating a GitHub personal access token (PAT). This is described here: [https://help.github.com/articles/creating-an-access-token-for-command-line-use/](https://help.github.com/articles/creating-an-access-token-for-command-line-use/). It is recommended to create a "classic" token and you don't need to give it any additional privileges.

Once you have created the token, add it to your AutoPkg preferences file. One way to do this is with the `defaults` command:

```bash
defaults write "$HOME/Library/Preferences/com.github.autopkg.plist" GITHUB_TOKEN YourTokenHere
```

Your `autopkg search` commands will now use this token every time.