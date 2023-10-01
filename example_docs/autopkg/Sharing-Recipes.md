So you've written your own recipes and want to share them? AutoPkg uses the [Boxen](https://github.com/boxen/our-boxen#sharing-boxen-modules) model to make it easy for people to add their repos to a common location. The AutoPkg GitHub organization will duplicate your repo and give you full access to the repo, and this means everyone's shared recipe repos will be listed under the AutoPkg org's [GitHub page](https://github.com/autopkg). The repo is still yours, you own the issues and pull requests, and are free to document the recipes as you wish. Note that this repo is a full standalone repo rather than a fork, because of differences with how [GitHub code search](https://help.github.com/en/github/searching-for-information-on-github/searching-code#considerations-for-code-search) works using forks.

## Preparing your recipes to share

Please first check the following in your own repo:

- That your recipes all have unique identifiers that follow the [identifier naming convention](Recipe-Writing-Guidelines#identifiers).
- That your repo doesn't contain any duplicate copies of recipes/processors from another repo. Your repo should contain your own recipes/processors only, not be a fork or copy of an existing repo like [autopkg/recipes](https://github.com/autopkg/recipes).
- Browse through the other [Recipe Writing Guidelines](https://github.com/autopkg/autopkg/wiki/Recipe-Writing-Guidelines) to ensure you're familiar with our shared conventions.
- It's an excellent idea to enable [two-factor authentication](https://github.com/settings/security) on your GitHub.com account, if you haven't already.

## Migrating your repo to the AutoPkg org:

Once your recipes are ready, here's how to get your own repo in the AutoPkg org:

1. [Submit an issue](https://github.com/autopkg/autopkg/issues/new) requesting that we add/fork your repo. Please include the URL of the repo you wish us to fork!
1. We'll duplicate the repo, give it a name like "username-recipes," and give you full write access to the repo. Indicate whether you'd like a different name for the recipes (for example, if your repo has a specific collection or "category" of software).
1. Leave your original repo around, but update its README to give the new repo location and a warning that the recipes in the old repo will either go away or no longer be updated at their original location. There's no reason to keep the recipes around at the old location, and people using your old recipe repos will need to update their repos in AutoPkg with the new location.
1. If your old repo was added to AutoPkg using `repo-add`, then the simplest way to switch to using the new location is to `repo-delete` it and `repo-add` the new one:

    ```
    autopkg repo-delete mygithubuser/my-old-recipes-repo
    autopkg repo-add autopkg/my-new-recipes-repo
    ```

## Repo maintenance expectations

As an author/maintainer of a repository of recipes in the AutoPkg org, your recipes will appear in `autopkg search` results, making them easy to find and use. Along with this increased visibility comes higher expectations for following code standards, fixing issues, and being receptive to pull requests. Here are a few guidelines we'd like recipe authors and maintainers to keep in mind.

- **Use linting**

    Syntax errors in recipe files can generate errors for people running AutoPkg recipes, _even if the recipe with the error is not the one being run_. Therefore, make sure the recipes in your repo pass a linting check. Here is a simple check you can use on plist recipes:
    ```
    find ~/path/to/your_repo -iname "*.recipe" -exec plutil -lint "{}" '+'
    ```
    For more advanced linting, there are [pre-commit](https://pre-commit.com/) hooks that validate AutoPkg recipes here: https://github.com/homebysix/pre-commit-macadmin

- **Avoid duplicating existing recipes**

    Your recipes will appear in search results, and it can be confusing to people getting started with AutoPkg to see multiple recipes with the same name. Therefore, please see if there's a recipe that does what you want in an existing repo before uploading a new one of your own. If an existing recipe can be easily modified to do what you want (e.g. adding code signature verification to a download recipe, as seen [here](https://github.com/autopkg/keeleysam-recipes/pull/87/files)), consider submitting a pull request to its author instead of creating a new recipe.

- **Try to repair broken recipes**

    Over time, it's common for recipes to require tweaking and adjustments to continue functioning as expected. For example, software developers may change the download format of their software, or newer versions of the software may be hosted from a different download URL. The community is very understanding of these challenges, while also appreciating recipe authors' best-effort to keep recipes running smoothly.

- **Be open to pull requests**

    As with many open source projects, your repository will likely receive pull requests (or "PRs") from fellow AutoPkg users and from AutoPkg org admins. These PRs are a crucial way that recipes are kept working and widely useful. As the owner of your recipes, you have final say in which changes you accept and which you deny, but try not to let PRs go months without any response at all.

## Recipe deprecation

When software developers cease development on an app, it's no longer necessary to maintain an AutoPkg recipe for that app. In those situations, you may want to add the [DeprecationWarning](https://github.com/autopkg/autopkg/wiki/Processor-DeprecationWarning) processor to your recipes.

It's typically only necessary to add the DeprecationWarning processor to the first recipe in a chain of recipes, which is often the "download" recipe. See [here](https://github.com/autopkg/homebysix-recipes/blob/284484e233065b6298795e51656bb7941255f3c4/YellowMug/EasyCrop.download.recipe#L22-L25) for an example.

## Transferring recipe ownership

Occasionally, recipe authors decide not to continue maintaining recipes for a specific app, either because they no longer need to deploy the app themselves, or because the app's recipes require too much time to maintain. In these situations, we suggest the following:

1. Reach out to the AutoPkg community to see whether anybody is interested in taking over your recipes for the app. Two good places to do this are in the [autopkg-discuss group](https://groups.google.com/forum/#!forum/autopkg-discuss) and in the [\#autopkg Slack channel](https://macadmins.slack.com/archives/C056155B4).

2. If somebody steps forward to take ownership, ask them to copy your recipe into their own repo in the AutoPkg org, making sure to change the recipe identifiers to match their own GitHub username instead of yours.

3. Add a DeprecationWarning processor to your copies of the app's recipes, with a message pointing people to the new recipes. See [this recipe](https://github.com/autopkg/gregneagle-recipes/blob/c33fea66670e0a048b0a9c0c7f4c284155d6c691/Bluejeans/BluejeansApp.install.recipe#L20-L28) for an example.

4. After a reasonable period of time, delete the app's recipes from your repository. You decide what is reasonable, but allow a minimum of 1 month for recipe users to see the deprecation message.

**Note**: Please think twice before simply deleting a recipe from your repo that you no longer use, because others may still be depending on it. The deprecation and ownership transfer processes above will make the transition as smooth as possible for everybody.

## Executive decisions

One benefit of AutoPkg's system of shared repositories is some degree of central oversight. The [owners of the AutoPkg organization](https://github.com/orgs/autopkg/people?utf8=✓&query=role%3Aowner) reserve the right to take action without warning on shared repositories. This may include merging pull requests on the repo owner's behalf, modifying recipes/processors to resolve community-reported errors, and consolidation of recipes/processors that serve identical functions. In very rare cases, the AutoPkg org owners may choose to remove entire repositories if deemed necessary.

## No warranty

The inclusion of any recipe, processor, or other file in a shared repository on the AutoPkg org does not constitute an endorsement by the AutoPkg owners or maintainers, and no guarantee of quality is given.
