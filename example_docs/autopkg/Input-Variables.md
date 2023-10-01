#### Input variables and conventions used

This is a list of keys and values given in the `Input` section of a recipe, which support being [overridden](Recipe-Overrides) by the admin. They are often strings, but aren't limited to any particular type. Note that only string types can be substituted using `%` signs (see [more on string substitution](Recipe-format#string-substitution)).

Here are some commonly-used Input variables:

<table>
  <tr><th>Key name</th><th>Applicable to kinds of recipe?</th><th>Description</th></tr>
  <tr><td>NAME</td><td>Any</td><td>A short name for the recipe. For Munki recipes, this should correspond to the 'name' key of the template pkginfo, or for Pkg recipes comprise part of the identifier.</td></tr>
  <tr><td>MUNKI_REPO_SUBDIR</td><td>Munki</td><td>corresponds to the subdirectory where the item should be imported. This will usually be overridden as Munki repos are organized according to the tastes of the admin/organization using Munki.</td></tr>
  <tr><td>pkginfo</td><td>Munki</td><td>This is a dict containing any "template" pkginfo data that should be used by Munki-related processors. This is the place to make any site-specific customizations to the pkginfo (catalogs, postinstall_scripts, unattended_install, etc.). The most sophisticated processors for certain recipes may still later merge in additional keys specific to the update.</td></tr>
</table>

## Casing conventions

Most Input variables should follow the all-upper-case naming convention. This is an indicator that the variable will be used in variable substitution, possibly in multiple places, later in the recipe.

### When to break the ALLCAPS convention

The reason the last one in the above table, `pkginfo`, is not upper-case, is because this is actually an input variable that can be passed to Munki-related processors. Most custom Input variables exist so that they can be passed to processors later using the string substitution system, like named arguments to a function. 'pkginfo' is a dict, however, so simple string substitution is not possible. Because Input variables ultimately exist in the same plist or yaml dictionary as variables used by processors, it is actually possible to set processor-specific variables here as well, and so this is what this is doing. A processor has no knowledge of how or at what stage the variable was set, and in the case of a Munki-related processor, it simply looks for a 'pkginfo' key if one exists.

Another example of this is for recipes that retrieve metadata from a [Sparkle](https://sparkle-project.org/) feed, and the special key `pkginfo_keys_to_copy_from_sparkle_feed`, which may be desired for certain Sparkle-driven recipes. See the [notes for the Sparkle processor](Processor-SparkleUpdateInfoProvider) for more details.
