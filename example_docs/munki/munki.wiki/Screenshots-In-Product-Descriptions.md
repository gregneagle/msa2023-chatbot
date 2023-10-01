_Including images/graphics/screenshots in Product descriptions_

### Introduction

Since you can include a subset of HTML in product descriptions, you can include IMG tags.
Together with a web server (like, say, your Munki server...) you can add images like screenshots to your product descriptions.

### Details

To add image content to a product description:

- Create your artwork in a web-friendly format (jpg, gif, png are good suggestions.) Images lay out best if they are no more than 560px wide.
- Copy to a web server. (If your Munki repo does not require authentication/authorization, create an artwork folder in your Munki repo, and copy it there. Otherwise, you might need to find or configure a "public" web server for this task; or perhaps you can configure your web server so that the artwork folder does not need authorization.)
- Add an IMG tag to your product description. Make sure you escape the HTML for inclusion inside plist XML. This generally means changing "<" to `&lt;`, ">" to `&gt;` and "&" to `&amp;`.

An example description:

    	<key>description</key>
    	<string>Mozilla Firefox is a free and open source web browser.
    &lt;br&gt;&lt;br&gt;
    &lt;img src="http://munkiserver/repo/artwork/Firefox_screenshot_01.png"&gt;</string>

![](https://github.com/munki/munki/wiki/images/screen_shots_in_descriptions.png)

Note that this artwork will not be cached for offline viewing; if your web server is not available when the description is viewed, a broken image placeholder will be displayed instead.

![](https://github.com/munki/munki/wiki/images/screen_shot_with_broken_link.png)