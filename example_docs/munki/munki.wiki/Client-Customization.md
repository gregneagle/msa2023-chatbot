### Introduction

Managed Software Center can be customized for your organization. Further, you can customize it per site, workgroup, or even user. Customization requires some familiarity with basic web development tools and techniques.


### Details

Most of what Managed Software Center displays is within a WebKit WKWebView. The views are generated dynamically, combining HTML templates with live data and static resources (images, CSS, JavaScript).

The default templates are in `Managed Software Center.app/Contents/Resources/templates/` and the static assets are in `Managed Software Center.app/Contents/Resources/WebResources/`

One approach to customization would be to replace some of these files and (optionally) add additional files to these directories. You'd have to be certain to re-do your modifications each time Managed Software Center.app was updated, so that might be a tedious method of customization.

Instead, you can create one or more zip archives of your desired customization files and make them available at a URL, typically in your Munki repo. `managedsoftwareupdate` will attempt to download any client customization resources when it runs; Managed Software Center.app will use any custom resources downloaded by `managedsoftwareupdate`.

#### Enable the HTML Web Inspector

For debugging you can activate the Web Inspector in the Managed Software Center.

Enter this in Terminal:
`defaults write com.googlecode.munki.ManagedSoftwareCenter developerExtrasEnabled -bool YES`

Now open MSC.app. Go to the product page you are debugging. Control-click inside the WebView and choose "Inspect Element" from the pop-up menu. You'll get a Safari-style Web Inspector to debug the HTML.

#### Customization overview

While you *can* customize anything in `Managed Software Center.app/Contents/Resources/templates/`, the most common customizations (and the only ones officially supported) are for these template files:

- `showcase_template.html` -- controls the banner images and any links
- `sidebar_template.html` -- the right-side sidebar displayed in the main Software view
- `footer_template.html` -- the page footer

While it is possible to customize any of the other template files, it's possible (or even likely) that a future release of Managed Software Center.app will include changes to the default/included versions of these template files. This could lead to unexpected/undesired behavior if you did not also update your versions of the customized files. Therefore, when you make your archive of customized files, include ONLY those files you actually customize. Do not include any other template files.

#### Showcase banner images requirements

When customizing the showcase_template.html, you will typically want to provide your own banner images.

Banner images may be any format that WebKit can display natively; png might be a good choice.
Images should be 1158x200 (or at least look good when resized to that resolution). Since the main window can be resized, you should test the images to make sure they don't hide any important information when the window is sized smaller than 1158 pixels wide. (The window can be as small as 1000px wide, so the displayed part of the image will be even smaller than that: it's approximately 960px wide on Mavericks, but exact measurements might vary on different OS versions.)

If you provide custom banner images, even if they share the same names as the stock/default images, you must also provide a customized showcase_template.html to refer to the custom images, which will be at a different _path_ from the stock images.

#### showcase_template.html example

Here's an example of a customized showcase_template.html. Note that this is a copy of the file at `Managed Software Center.app/Contents/Resources/templates/showcase_template.html`. **The JavaScript at the beginning of the file is left unchanged** (though you could change it if you wanted different behaviors).  In this example, we are only customizing the actual images shown and what they link to.

```html
<script type="text/javascript">
var currentSlide = 0, playing = 1

function slides(){
    return document.querySelectorAll('div.stage>img')
}

function showSlide(slideNumber){
    theSlides = slides()
    for (c=0; c<theSlides.length; c++) {
        theSlides[c].style.opacity="0";
    }
    theSlides[slideNumber].style.opacity="1";
}

function showNextSlide(){
    if (playing) {
        currentSlide = (currentSlide > slides().length-2) ? 0 : currentSlide + 1;
        showSlide(currentSlide);
    }
}

function stageClicked() {
    var slide = slides()[currentSlide];
    var target = slide.getAttribute('target');
    var link = slide.getAttribute('href')
    if (target == '_blank') {
        if ('AppController' in window) {
            // MSC < version 5 with WebView
            window.AppController.openExternalLink_(link);
        } else {
            // MSC version 5+ with WKWebView
            window.webkit.messageHandlers.openExternalLink.postMessage(link);
        }
    } else {
        window.location.href = link;
    }
}

window.onload=function(){
    showSlide(0);
    if (slides().length > 1) {
        setInterval(showNextSlide, 7500);
    }
}
</script>

<div class="showcase">
    <div class="stage" onClick='stageClicked();'>
        <img target="_blank" href="http://www.apple.com" alt="Apple" src="custom/resources/Apple.png" />
        <img href="munki://detail-GoogleChrome.html"  alt="Google Chrome" src="custom/resources/Chrome.png" />
        <img href="munki://developer-Google.html" alt="Google Applications" src="custom/resources/Google.png" />
    </div>
</div>
```

We have three images, `"custom/resources/Apple.png"`, `"custom/resources/Chrome.png"`, and `"custom/resources/Google.png"`. These will be in our archive of custom files. You could, if you wished, link to a full (external) http URL for these images, but Managed Software Center.app would display broken image link placeholders if it can't reach those URLs (for example, if the images are hosted on an internal web server not available when a user is at home or out of the office).

There are two optional attributes that can be added to each `img` element: `target` and `href`. `href` is a link -- it can point to any full or relative URL. if `target="_blank"`, the URL will be forwarded to the user's default browser; otherwise Managed Software Center.app will attempt to display the contents of the URL.

Notice the special links for the second and third images. These are URLs internal to Managed Software Center.app to cause it to display specific content. `"munki://detail-GoogleChrome.html"` links to the detail view for GoogleChrome; `"munki://developer-Google.html"` shows all items whose developer is "Google". More documentation on these internal links will be available in the future.

#### sidebar_template.html example

> **NOTE:** Managed Software Center prior to version 5.3 (included with Munki 5.2) displayed a sidebar of links on the right side of the window. With Managed Software Center 5.2, these links are now displayed in a strip below the banner images. The html template continues to be called "sidebar_template.html".

Here's an example of a customized sidebar_template.html showing some of the possibilities:

```html
<div class="sidebar">
    <div class="chart titled-box quick-links">
        <h2>Quick Links</h2>
        <div class="content">
            <ol class="list">
                <li class="link user-link"><a href="#">Welcome</a></li>
                <li class="link user-link"><a href="#">Support</a></li>
                <li class="separator"><hr/></li>
                <li class="popup">
                    <div class="select links">
                        <label>
                            <span></span>
                            <select id="category-selector" onchange="category_select()">
                                ${category_items}
                            </select>
                        </label>
                    </div>
                </li>
                <li class="link"><a target="_blank" href="http://google.com">Search Google</a></li>
                <li class="link"><a target="_blank" href="http://bing.com">Search Bing</a></li>
                <li class="separator"><hr/></li>
                <li class="link"><a target="_blank" href="https://www.apple.com/macos/monterey/features/">What's new in macOS Monterey</a></li>
                <li class="link"><a target="_blank" href="https://www.apple.com">Apple</a></li>
            </ol>
        </div>
    </div>
</div>
```

The customized "sidebar" (now more of a "link bar") would look like this:

![](https://github.com/munki/munki/wiki/images/customized_sidebar.png)

#### footer_template.html example

Finally, an example of a customized footer_template.html:

```html
<div class="bottom-links">
    <ul class="list" role="presentation">
        <li><a target="_blank" href="http://www.apple.com">Apple</a></li>
        <li><a target="_blank" href="http://www.google.com">Google</a></li>
        <li><a href="updates.html">Updates</a></li>
    </ul>
</div>
```

### Creating the client customization archive

The archive of client customization files has a specific format. 
Create two directories: "templates" and "resources". Place all your customized template files in "templates"; custom images, css and JavaScript (or anything else referred to in your customized templates) should go in "resources".

**I recommend that you use the command-line `zip` tool to create the actual archive. Using the Finder's *Compress "foo"* contextual menu will not create archives with the expected layout.**

Assuming you are in the directory containing your templates and resources directories:

```bash
zip -r site_default.zip resources/ templates/
```

`-r` tells zip to add the resources and templates directories recursively to the archive named site_default.zip (without the '-r' flag, you'll get only empty directories in the archive!).

To verify the contents of an archive you've created, use 
```bash
unzip -l site_default.zip
```
You'll see a listing of the archive contents. It should look similar to this:

```
Archive:  /Library/Managed Installs/client_resources/custom.zip
  Length     Date   Time    Name
 --------    ----   ----    ----
        0  04-28-16 12:53   resources/
   104982  03-10-16 13:27   resources/branding.png
   232535  09-22-14 14:29   resources/branding1.png
    61665  09-26-14 08:57   resources/branding2.png
        0  07-24-14 12:48   templates/
      281  09-22-14 15:51   templates/footer_template.html
     1580  04-28-16 13:02   templates/showcase_template.html
     1628  03-09-16 14:00   templates/sidebar_template.html
```

A sample archive is here: https://github.com/munki/contrib/raw/master/site_default.zip

### Making client customization archives available to clients

`managedsoftwareupdate` as part of its update check, attempts to download client customization resources. Typically, you can make these available from your Munki repo by creating a "client_resources" directory at the top level of the repo. If you want to make these available at a different URL, you can set Munki's **ClientResourceURL** to an alternate base URL. (This follows the pattern of ManifestURL, CatalogURL and PackageURL as alternate base URLs.)

If Munki's **ClientResourcesFilename** preference is defined, this filename will be used (appending ".zip") if needed; otherwise `managedsoftwareupdate` will request an archive with the same name as the primary manifest (plus ".zip"), falling back to "site_default.zip".

Requests will be of the form "http://munki/repo/client_resources/site_default.zip". If no client customization resources are found, the default resources within Managed Software Update.app will be used.

### Behind the scenes

Client customization resources are downloaded to Munki's data directory; typically `/Library/Managed Installs`, in a `client_resources` subdirectory, with the filename `custom.zip` -- no matter the name of the remote file at the URL.

On launch, Managed Software Center.app checks for the existence of this file. If it exists, it's checked to see if it has the expected layout (top-level "resources" and "templates" directories), and if so, these directories are expanded into `~/Library/Caches/com.googlecode.munki.ManagedSoftwareCenter/html`, which is where Managed Software Center.app finds all of its HTML/CSS/JavaScript, etc resources.

You can open these same files (the ones in `~/Library/Caches/com.googlecode.munki.ManagedSoftwareCenter/html`) in Safari (and use Safari's web inspector, etc) to debug if things aren't behaving as you'd expect.

### Managed Software Center 5/Munki 3.6 notes

Munki 3.6 includes a brand-new version of Managed Software Center, rewritten in Swift. It also swaps out the old (and deprecated) WebKit WebView with the new WebKit WKWebView.

One of the consequences of this change is that all of the JavaScript integration between the (WK)WebView and the rest of the app has changed.

This can affect any HTML template customization you may have done for Managed Software Center.

This sort of change is one of the reasons that you should avoid customizing html templates other than showcase_template.html, sidebar_template.html, and footer_template.html. 

But even if your customizations are limited to those files, you may have to update your showcase_template.html customizations to work with the changes in Managed Software Center version 5.

Specifically there are changes to the javascript embedded in the default showcase_template.html, and even more specifically the "stageClicked()" function has changed to deal with the changes in MSC.app 5:

```javascript
function stageClicked() {
    var slide = slides()[currentSlide];
    var target = slide.getAttribute('target');
    var link = slide.getAttribute('href')
    if (target == '_blank') {
        if ('AppController' in window) {
            // MSC < version 5 with WebView
            window.AppController.openExternalLink_(link);
        } else {
            // MSC version 5+ with WKWebView
            window.webkit.messageHandlers.openExternalLink.postMessage(link);
        }
    } else {
        window.location.href = link;
    }
}
```

Note the conditional branching to deal with different object/method calls for MSC 4 and MSC 5.

If you have made customizations to any of the other HTML templates, it's likely you'll find broken button functionality and other undesired behavior. You'll need to either update your customizations or remove them.