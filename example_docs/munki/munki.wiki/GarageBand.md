### Deploying GarageBand with Munki
Deploying GarageBand itself is pretty straightforward however the Apple Loops element can cause issues if not done correctly.

#### Import GarageBand
GarageBand 10 is now a App Store application, please follow the guidelines for the importing GarageBand from the [[ App Store Apps | App-Store-Apps ]] page.

### Import Audio Content

In shared environments where users aren't admin users, you will want to deploy at least the mandatory Apple Loops so users are not prompted to install themselves on first launch. If you decide to skip installing these mandatory loops, GarageBand will download them on first launch. Followed by prompting an administrator for their authorization to start the installation of these packages.


#### Method 1

As of January 2017 this is the best practices solution as it mimics how the GarageBand application obtains the loops from Apple.

1. [@carlashley](https://github.com/carlashley/) currently hosts a script that will download the latest loops for you located [appleLoops](https://github.com/carlashley/appleLoops). Please see the repo README for more information.

1. Download the appleLoops repo:

    ```bash
    $ git clone https://github.com/carlashley/appleLoops.git
    $ cd appleLoops
    ```

1. Download the mandatory apple loops packages.

    ```bash
    $ ./appleloops --apps garageband -m --destination ~/Desktop/loops
    ```

1. Import these packages and set them as an `update_for` to your GarageBand application. These 'essential' 33 packages can be mass imported with a something like [@aysiu](https://github.com/aysiu)'s [BulkMunkiImport.sh](https://github.com/aysiu/munkiscripts/blob/master/BulkMunkiImport.sh).

**Note:** As of late 2017, the `appleLoops.py` tool added the capability to install the additional content without importing it into your munki repo. Refer to the [appleLoops Deployment wiki page](https://github.com/carlashley/appleLoops/wiki/Deployment) for more information.

#### Method 2

> ***
This method installs the "CoreContents" packages in order to avoid the GarageBand first run download. As of January 23rd, 2017 and GarageBand 10.1.5 this method still works but could become deprecated at anytime.
***


##### Import Apple Loops

1. Download the two CoreContents packages:
    * [GarageBandCoreContent2.pkg](http://audiocontentdownload.apple.com/lp10_ms3_content_2015/MAContent10_GarageBandCoreContent2.pkg)
    * [GarageBandCoreContent_v3.pkg](http://audiocontentdownload.apple.com/lp10_ms3_content_2013/MAContent10_GarageBandCoreContent_v3.pkg)

1. Now you will want to use munkiimport on the two packages.

    Requirements (for silent install):
    ```txt
    MAContent10_GarageBandCoreContent_v3.pkg
    MAContent10_GarageBandCoreContent2.pkg
    ```


1. The above CoreContent packages contain the same package identifier as such munki will, by default, only attempt to install the latest version (V3) however GarageBand 10.1.0 requires both. You will need to modify your pkginfo for the `MAContent10_GarageBandCoreContent_v3.pkg` package to require `MAContent10_GarageBandCoreContent2.pkg`. Sample snippets below:


    MAContent10_GarageBandCoreContent-2.0.0.0.1.1256150330.plist
    ```xml
    	<key>update_for</key>
    	<array>
    		<string>GarageBand</string>
    	</array>
    	<key>version</key>
    	<string>2.0.0.0.1.1256150330</string>
    ```

    MAContent10_GarageBandCoreContent-3.0.0.0.1.1256150330.plist
    ```xml
    	<key>requires</key>
    	<array>
    		<string>MAContent10_GarageBandCoreContent-2.0.0.0.1.1256150330</string>
    	</array>
    	<key>update_for</key>
    	<array>
    		<string>GarageBand</string>
    	</array>
    	<key>version</key>
    	<string>3.0.0.0.1.1256150330</string>
    ```

1. Optional Apple Loops packages can be set placed in your manifests `optional_installs` array or set as an `update_for` if you wish for them to be deployed as well.


Resource: [Download all of the GarageBand content loops](http://www.amsys.co.uk/2015/02/download-garageband-logic-pro-x-content-loops-deployment/)
