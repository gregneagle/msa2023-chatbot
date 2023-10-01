_Support for displaying "Featured Items" in Managed Software Center_

## About Featured Items

Support for Featured Items in Managed Software Center is a new feature for Munki 3.

### Overview

Managed Software Center will display "Featured" items if there are any in the list of optional installs. If there are any "Featured" items, it replaces the "All Items" view.

### Implementation

Add a featured_items section to a manifest containing the items you wish to feature:
```xml
        <key>featured_items</key>
        <array>
            <string>Office2016</string>
            <string>Slack</string>
            <string>SuperSolitaire2017</string>
        </array>
```
Featured items must be available via optional_installs; in other words, adding an item to featured_items does not automatically make it an optional\_install -- it only makes it "Featured" _if_ it is an optional\_install. Yes, this means maintaining an item in two lists: optional\_installs to make it available as an optional install, and featured\_items to have it displayed with other featured items. But this allows one to feature different items for different groups.

![](https://github.com/munki/munki/wiki/images/MSC_Featured_Items.png)
