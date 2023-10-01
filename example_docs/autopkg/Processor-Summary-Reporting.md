As of AutoPkg 0.5.0, processors can define their own "summary results" that will be printed in a human-friendly summary at the end of `autopkg run`. Previous to 0.5.0, several core processors like PkgCreator and MunkiImporter did this, but it was not possible for processors to define this themselves (it was hardcoded in AutoPkg itself).

Sample summary output at the end of `autopkg run Firefox.munki OracleJava8.munki`:

```
The following packages were built:
    Identifier               Version  Pkg Path                                                                             
    ----------               -------  --------                                                                             
    org.mozilla.firefox.pkg  39.0     /Users/tim/Library/AutoPkg/Cache/com.github.autopkg.pkg.Firefox_EN/Firefox-39.0.pkg  

The following packages were copied:
    Pkg Path                                                                                       
    --------                                                                                       
    /Users/tim/Library/AutoPkg/Cache/com.github.autopkg.pkg.OracleJava8/OracleJava8-1.8.51.16.pkg  

The following new items were downloaded:
    Download Path                                                                                  
    -------------                                                                                  
    /Users/tim/Library/AutoPkg/Cache/com.github.autopkg.pkg.Firefox_EN/downloads/Firefox.dmg       
    /Users/tim/Library/AutoPkg/Cache/com.github.autopkg.pkg.OracleJava8/downloads/OracleJava8.dmg  
```

The first summary section ("The following packages were built") was printed using data made available in the PkgCreator processor. This is possible because PkgCreator defines a dictionary output variable that ends in `_summary_result`, with a specific structure. An example of this format can be found [here](https://github.com/autopkg/autopkg/blob/3534794cf28e2274fd221852fd7b1f8da923e62f/Code/autopkglib/PkgCreator.py#L193-L201). There are three keys within this dict:

* `summary_text`: String with the header text.
* `report_fields`: A list of the fields in the order that they should appear as columns.
* `data`: A dictionary containing each of the fields (from `report_fields`) as keys, with strings as their values.

Alternatively, it's possible to define a simpler structure if you have only a single field to report. See [URLDownloader](https://github.com/autopkg/autopkg/blob/3534794cf28e2274fd221852fd7b1f8da923e62f/Code/autopkglib/URLDownloader.py#L212-L215) as an example.

It's also recommended for a processor to first clear an already-existing `_summary_result` key (that which is used by _this_ processor) from `env` that might exist already from another instance of this processor that may have run earlier in a recipe. An [example](https://github.com/autopkg/autopkg/blob/3534794cf28e2274fd221852fd7b1f8da923e62f/Code/autopkglib/PkgCreator.py#L112-L114), again from PkgCreator.

In order for this summary result to show up, you will need to declare it as an output variable in your processor:

```
    output_variables = {
        "example_summary_result": {
            "description": "Summary of useful results."
        }
    }
```