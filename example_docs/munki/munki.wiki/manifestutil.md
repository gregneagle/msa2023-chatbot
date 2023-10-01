_Documentation for manifestutil_

### Introduction

`/usr/local/munki/manifestutil` can help you create and edit client manifests. It supports a variety of options, but its biggest strength is when run with no options. It then runs as an interactive shell with tab-completion for the subcommands, options, and even package names, catalog names, and section names:

### Details

#### Configuration

`manifestutil` shares configuration information with `munkiimport`, so if you've configured `munkiimport` you should not need to configure `manifestutil` in order to use it. If you haven't configured either `munkiimport` or `manifestutil`:

```bash
% /usr/local/munki/manifestutil --configure
Repo URL (example: afp://munki.example.com/repo): file:///Users/Shared/munki_repo
```

You need to provide a URL to the munki repo. file://, smb:// and afp:// URLs are supported; other URL schemes may be supported with the use of repo plugins.


### Usage

    /usr/local/munki/manifestutil 
    Entering interactive mode... (type "help" for commands)
    help
    Available sub-commands:
    	add-catalog
    	add-included-manifest
    	add-pkg
    	configure
    	copy-manifest
    	display-manifest
    	exit
    	find
    	help
    	list-catalog-items
    	list-catalogs
    	list-manifests
    	new-manifest
    	remove-catalog
    	remove-included-manifest
    	remove-pkg
    	version
    add-pkg
    Usage: add-pkg PKGNAME --manifest MANIFESTNAME [--section SECTIONNAME]
    add-pkg AdobePhotoshopCS5 --manifest allure --section managed_uninstalls

In the above command I typed `add-p[AdobeP[tab](tab]) --m[all[tab](tab]) --s[managed_un[tab](tab])`

The tab-completion is very useful when adding package names to a manifest -- you can use tab-completion to get a list of names:

    remove-pkg Adobe[tab][tab]
    AdobeAfterEffectsCS5       AdobeCS4DesignStandard     AdobeCS4MasterCollection   AdobeFlashProCS5.5         
    AdobeInDesignCS5           AdobeLightroom3            AdobeMasterCollectionCS5   AdobeProductionPremiumCS5  
    AdobeReaderX               AdobePhotoshopCS5          

and manifests:

    remove-pkg AdobePhotoshopCS5 --manifest al[tab][tab]
    aleta        allure       allure-test  alturas 

and sections:

    remove-pkg AdobePhotoshopCS5 --manifest allure --section [tab][tab]
    managed_installs    managed_uninstalls  managed_updates     optional_installs

Which helped me write this command:

    remove-pkg AdobePhotoshopCS5 --manifest allure --section managed_uninstalls
    Removed AdobePhotoshopCS5 from section managed_uninstalls of manifest allure.

The find command can find every manifest that has a certain package, and you can optionally restrict the search to a specific section:

    find AdobePhotoshopCS5 --section managed_installs
    agree: AdobePhotoshopCS5
    aleta: AdobePhotoshopCS5
    [snip]
    voodoo: AdobePhotoshopCS5
    willie: AdobePhotoshopCS5
    zircon: AdobePhotoshopCS5
    groups/TalDevL122Lab: AdobePhotoshopCS5
    127 items found.
    
    find AdobePhotoshopCS5 --section managed_uninstalls
    greenbo: AdobePhotoshopCS5
    1 items found.
    display-manifest greenbo
    catalogs:
        production
    included_manifests:
        groups/DisneyStandardConfiguration
    managed_installs:
        PhotoshopCS4
        ExpressionMedia2
        FinalDraft8
        WacomTablet
    managed_uninstalls:
        AdobePhotoshopCS5