AutoPkg is packaged using an [AutoPkg recipe](https://github.com/autopkg/recipes/blob/master/AutoPkg/AutoPkgGitMaster.pkg.recipe), which uses as its source a zipball downloaded from the tip of GitHub master branch.

The process below is now automated with a [script](https://github.com/autopkg/autopkg/blob/master/Scripts/make_new_release.py), but still follows the same steps. Releases should be normally be done using this release script as opposed to manually.

**NOTE**: Prior to beginning these steps, ensure you have run through the AutoPkg [[unit tests|Running Unit Tests]] successfully.

## Updating the wiki before a new release

The wiki documentation should be updated for every release, and there is a [script](https://github.com/autopkg/autopkg/blob/master/Scripts/generate_processor_docs.py) that will do this. It pulls the version from the same AutoPkg checkout and puts this in the commit note, so it is best to update the wiki immediately _before_ running the release build script steps below.

## Releasing a new package with the script

These are the steps to make a new release. The Github token must be generated from https://github.com/settings/tokens. It's recommended you save it somewhere.

1. Update the CHANGELOG.md. The header should end in `...HEAD) (Unreleased)`.
2. Commit the CHANGELOG.md and push to master.
3. `cd Scripts`
4. `./make_new_release.py --next-version X --token Y --dry-run`

Always use a dry-run to test out the entire process first, because if it fails partway through for any reason, recovering from an incomplete push is a painful process.

## Manual release steps
For reference, a package release should be done by taking the following steps (assuming we're releasing version `1.2.3`):

1. Ensure all commits for the final release have been pushed to GitHub.
1. Ensure your working directory is completely clean.
1. Ensure `CHANGELOG.md` contains summaries of changes, fixes, features, etc. Add the release date to the header with the current version being released.
1. Commit and tag the new version:
```bash
git add CHANGELOG.md
git commit -m "v1.2.3"
git tag v1.2.3
git push
git push --tags
```
1. Bootstrap the install to ensure we're using the current pkgserver code for the PkgCreator step of the recipe we'll be running:
```bash
sudo Scripts/install.sh
```
1. Ensure the `AutoPkgGitMaster.pkg` recipe is available and up to date:
```bash
Code/autopkg repo-add https://github.com/autopkg/recipes
```
1. Run the packaging recipe:
```bash
Code/autopkg run AutoPkgGitMaster.pkg
```
1. Verify the package contents:
```bash
lsbom $(pkgutil --bom /path/to/built/autopkg-1.2.3.pkg)
```
1. Visit the [tags page](https://github.com/autopkg/autopkg/tags) and draft a new release for the new tag. Attach the newly-built package and copy/paste the notes for this version from the changelog.
1. Commit an increment to the version files (for example incrementing to `1.2.4`):
```bash
/usr/libexec/PlistBuddy -c 'Set :Version 1.2.4' Code/autopkglib/version.plist
```
1. Update `CHANGELOG.md` to add "### 1.2.4 (Unreleased)" at the top.
1. Commit and push the incremented version:
```bash
git add Code/autopkglib/version.plist CHANGELOG.md
git commit -m "Bumping version for development."
git push
```

## Recovering from a partial release

If the release script fails to run completely, recovering takes a few steps.

1. Revert the Release commit.
2. Delete the remote tag, where X.Y.Z is the version:
 ```
 git tag -d v.X.Y.Z
 git push origin :refs/tags/vX.Y.Z
 ```