#### Variables that are important to know about if writing recipes

Most AutoPkg recipes to date follow roughly this pattern:

1. Check some URL to determine what to download
1. Download it if not already cached
1. Optionally process the downloaded file
1. At some point by now, mark as being the end of the "check" phase
1. Import the result into a repository or build a package

The processors used to perform some of these tasks use several common variable names, listed below:

<table>
  <tr><th>Name</th><th>Description</th></tr>
  <tr><td>url</td><td>The URLDownloader processor will use this for the URL to download. Any custom processor that provides a download URL should use this.</td></tr>
  <tr><td>download_changed</td><td>URLDownloader sets this boolean to True if it determines that we do not have a previously-cached file of this download. `automunkiimport` uses this to report any new downloads for a run.</td></tr>
  <tr><td>pathname</td><td>URLDownloader uses this for the location of the downloaded file. You can refer to this for any post-processing steps in the recipe. You can set this as an input variable, otherwise it will be set automatically based on the tail of the URL.</td></tr>
  <tr><td>pkginfo</td><td>This is a "base" pkginfo dict that is used by MunkiImport and MunkiPkginfoMerger. MunkiImport will use it to copy any keys after running makepkginfo, and MunkiPkginfoMerger will use it as a base to merge to merge two pkginfo dicts.</td></tr>
  <tr><td>additional_pkginfo</td><td>This is what will be merged on top of the contents of `pkginfo` by MunkiPkginfoMerger. MunkiInstallsItemsCreator will set this, for example, as will some other application-specific processors to provide additional pkginfo keys such as `requires`, `minimum_os_version`, etc. Note that MunkiPkginfoMerger is the only recipe that performs something useful with this as input.</td></tr>
</table>