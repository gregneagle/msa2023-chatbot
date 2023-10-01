_Documentation on munki:// links_

### Details

Managed Software Center supports a custom protocol: munki://

You can use this to link to specific pages and items within Managed Software Center, perhaps from an internal documentation page.

Some possibly useful links:

`munki://category-all`

Opens the main Software page:

![](https://github.com/munki/munki/wiki/images/managed_software_center.png)

`munki://categories`

Opens the Categories page.

`munki://developer-microsoft`

Opens Managed Software Center to a page listing all the items with developer "Microsoft":

![](https://github.com/munki/munki/wiki/images/msc_5_3_microsoft_items.png)

`munki://myitems`

Opens Managed Software Center to the My Items view.

![](https://github.com/munki/munki/wiki/images/msc_5_3_my_items.png)

`munki://updates`

Opens the application to the Updates view:

![](https://github.com/munki/munki/wiki/images/msc_5_3_updates.png)

`munki://detail-AdobeReaderDC`

Displays the detail page for an item named "AdobeReaderDC".

The link format is `munki://detail-[item name]`, where 'name' is the pkginfo 'name' key (and not the 'display_name').
Detail links are case sensitive.

![](https://github.com/munki/munki/wiki/images/msc_5_3_product_detail.png)

Links do not have to be crafted by hand, and can be copied directly from the Managed Software Center application user interface by right-clicking on the categories on the Software and Categories tabs (for category links), and on application icons or names (for application links) _except_ on the application detail view.

![](https://github.com/munki/munki/wiki/images/msc_copy_link.png)


#### Caveats

Like any URL, some characters may need to be URL-encoded. For example, replace spaces in links with `%20`. 

Except for `detail` links, links aren't case sensitive. They will however bring up a page with the same case as in the link. Thus, linking to munki://developer-graham%20gilbert rather than munki://developer-Graham%20Gilbert will work but be visually inconsistent with what Managed Software Center will show if just browsing to items developed by Graham Gilbert (with capital Gs).

(This wiki doesn't allow these munki:// protocol links to be clickable. Copy them and paste them into your browser's URL field or use the `open` command from your shell, ie. `open munki://detail-Firefox`)