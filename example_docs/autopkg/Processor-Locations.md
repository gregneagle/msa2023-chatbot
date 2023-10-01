# Processor Locations

AutoPkg processors may be located in several places for use by recipes.

### AutoPkg core processors
These ship with AutoPkg and are available to every recipe. They can be listed using the `list-processors` verb:
```
➜ autopkg list-processors

AppDmgVersioner
BrewCaskInfoProvider
CodeSignatureVerifier
Copier
DmgCreator
...
```

In discussion, people commonly refer to these as the “core processors.”

### Recipe processors

Anyone may write their own processor code and place it in a `ProcessorName.py` file, where `ProcessorName` is the name of the processor, in a directory alongside one or more recipes. Recipes can refer to this processor in a Process step's `Processor` key just as they do with core processors. Any processors loaded here will take precedence over core processors.

Both core and recipe processors are defined in a recipe's Process item simply by name:

```xml
<key>Process</key>
<array>
    <dict>
        <key>Processor</key>
        <string>MunkiImporter</string>
    </dict>
</array>
```

In discussion, people commonly call these “custom processors.”

### Shared recipe processors

As of AutoPkg 0.4.0, it is possible to refer to a recipe processor from any other recipe, as long as that recipe is also in the search path. This is done by defining the processor in a way that includes the recipe identifier that will be used to "find" the processor:

```xml
<key>Process</key>
<array>
    <dict>
        <key>Processor</key>
        <string>com.github.user.SpecialMunkiImporter/SpecialMunkiImporter</string>
    </dict>
</array>
```

As long as a recipe with the identifier `com.github.user.SpecialMunkiImporter` exists in the search path for an `autopkg run`, the `SpecialMunkiImporter` processor will be found and loaded.

This functionality makes it possible for an author to write a general-purpose processor that can be used by other recipe authors, without them needing to maintain their own copy of the processor along with all their recipes.

It may be desirable for such a processor to have a "stub" recipe written alongside it, so that this can be used as a generic namespace with which to find the recipe. A "stub" recipe is not required, however -- you can use the identifier of any recipe that is in the same directory as the processor you wish to use.

See [here](https://github.com/autopkg/recipes/tree/master/SampleSharedProcessor) for an example of such a processor and stub recipe. Some noteworthy processors outside of the ones provided with the core autopkg tools are listed [here](https://github.com/autopkg/autopkg/wiki/Noteworthy-Processors). 

In discussion, such general-purpose custom processors are commonly referred to as “shared processors.”