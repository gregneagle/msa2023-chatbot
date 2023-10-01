Normally, open-source software projects developed on GitHub include 'Releases' for new versions which include the corresponding dmg, pkg, and/or zip of the published new software version.  In these cases, it's incredibly easy to grab all pertinent information, including the software version number of the latest release and the download URL for the applicable asset, with the [`GitHubReleasesInfoProvider`](https://github.com/autopkg/autopkg/wiki/Processor-GitHubReleasesInfoProvider) processor.

However, some software developed on GitHub do _not_ have release downloads on GitHub, instead opting to host new software releases elsewhere.  In these cases, attempting to use the [`GitHubReleasesInfoProvider`](https://github.com/autopkg/autopkg/wiki/Processor-GitHubReleasesInfoProvider) processor will fail because there are no assets associated with the release.  Since the version number of the latest release is useful information to collect, and which can be used to parse the necessary software download elsewhere, there's a different way to collect this information from GitHub.

Using the [`URLTextSearcher`](https://github.com/autopkg/autopkg/wiki/Processor-URLTextSearcher) processor you can parse the latest version.  While the versioning scheme of software may vary, the below example & regex (`re_pattern`) will work for the majority of software on GitHub including those that use [semantic versioning](https://semver.org/) (ex. releases: `v10.2.1`; `5.0.30`):

```xml
<dict>
    <key>Comment</key>
    <string>Get latest release version number from GitHub</string>
    <key>Arguments</key>
    <dict>
        <key>re_pattern</key>
        <string>/releases/tag/v?([\d.]+)</string>
        <key>result_output_var_name</key>
        <string>version</string>
        <key>url</key>
        <string>https://github.com/<org>/<project>/releases/latest</string>
    </dict>
    <key>Processor</key>
    <string>URLTextSearcher</string>
</dict>
```

An example recipe where this is actively used for reference: https://github.com/autopkg/apizz-recipes/blob/master/TigerVNC/TigerVNC.download.recipe
