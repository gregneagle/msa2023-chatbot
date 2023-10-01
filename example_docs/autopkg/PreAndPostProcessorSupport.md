The preprocessor and postprocessor options (`--pre/--preprocessor` and `--post/--postprocessor`) are advanced options for `autopkg run` allowing you to customize recipe runs without manually adding processor steps to recipe files. Instead, processors are dynamically added to the beginning (`--pre`) or end (`--post`) of each recipe in the run list. This allows you to modify the behavior of a recipe ad-hoc, without duplicating entire recipes or heavily customizing overrides with additional `Process` steps.

These options take the name of a processor and can be specified multiple times to prepend or append processor steps in the order that the options are given.

There is no way to pass additional arguments to processors run in this context. If such a processor expects some input variable to be defined, they must be defined using either `--key` options in the same command invocation or as defaults in `com.github.autopkg`.

Processors run in this context function the same as regular processors. They have full read/write access to the environment available in `self.env`.

There is no support to defining these pre/postprocessors in an override or special file: they must always be explicitly given as options when running `autopkg run`. These options could be instead defined in a shell alias or wrapper script.

## Example

For example, you can run a recipe with a preprocessor specially crafted to change a variable that would not be possible to set in an override. This what is done by an example new processor, [MunkiSetDefaultCatalog](https://github.com/autopkg/autopkg/blob/master/Code/autopkglib/MunkiSetDefaultCatalog.py). Adding it as a preprocessor will attempt to modify the `catalogs` array in your recipe's `pkginfo` input variable if you have defined an alternate default catalog using `munkiimport --configure`.

```
autopkg run --pre MunkiSetDefaultCatalog AdobeFlashPlayer.munki
```

Running the above command, AutoPkg will add `MunkiSetDefaultCatalog` to the start of the `AdobeFlashPlayer.munki` recipe run.

Normally there is no way to override certain keys of a `pkginfo` input variable, as AutoPkg doesn't support dictionary or array merging of input variables in child recipes. This processor gets around this by modifying the contents of `pkginfo` at the beginning of the run, without any modifications to recipe/override files.

## Use cases

Some other possible use cases for pre/postprocessors:

* performing automated analysis of output files
* signing built packages from `.pkg` recipes
* copying recipe results to other customized locations
