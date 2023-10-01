_Support for Notification Center notifications of pending software updates_

## About Notification Center Support

Notification Center is a new feature in Munki 3.

### Background/History

If you've been using Munki for some time, you might be wondering about this:

>https://github.com/munki/munki/wiki/FAQ#q-does-munki-support-notification-center-notifications  
Q: Does Munki support Notification Center notifications?

>A: No. Much work was done to add Notification Center support, until we discovered a fundamental issue: Notification Center notifications are completely under user control, and users can turn them off. Worse, the software posting the notifications doesn't even know/can't find out that the user has turned them off. One assumes that you, the admin, think it is important to notify users of pending updates and would like to ensure your users are notified. If so, Notification Center notifications are not a good mechanism to accomplish that. So rather than have two notification methods (Notification Center, which we can't rely upon, and Munki's current method of launching/activating Managed Software Center) we decided to just have the one, reasonably reliable notification method.

So what changed?

It occurred to me that if Munki started tracking the dates updates first became available, that we could change the notification behavior if one or more updates had been pending for "too long".  We could use Notification Center to notify about pending updates, but if the user had turned off notifications or is ignoring the notifications, after a few days we can "escalate" the notification by returning to the previous behavior of launching Managed Software Center.app.

### Implemented behavior

When Munki decides to notify the user of pending updates, instead of launching Managed Software Center.app, it launches munki-notifier.app, a new Cocoa application you can find inside MSC.app/Contents/Resources. This app then either posts a Notification Center notification or launches MSC.app as appropriate.

The default "escalation period" is three days. In other words, if any pending update has been available for over three days, munki-notifier will skip posting a Notification Center notification, and will instead launch MSC.app. Admins can customize this grace period by setting the ManagedInstalls preference "UseNotificationCenterDays" to the number of days Notification Center notifications should be attempted before switching to launching MSC.app.

If you would like to not use the Notification Center, and only use MSC.app, you can disable it by setting the value of `UseNotificationCenterDays` to `-1`.

### ManagedInstalls preferences

| Key | Type | Default | Description |
| --- | -------- | ------- | ----------- |
| UseNotificationCenterDays | integer | 3 | Number of days Notification Center notifications should be used before switching to launching Managed Software Center|

### Localized notifications

Notifications have been (possibly poorly) localized into all the languages supported by Managed Software Center.app. If you notice a poor localization, let me know or (better) file a PR. Localized strings are in the *.lproj folders here: 
https://github.com/munki/munki/tree/master/code/apps/munki-notifier/munki-notifier

There are currently only five strings to be localized. Some of these phrases were already localized for MSC.app, so I borrowed those. "Details" is commonly localized in several apps, so I borrowed those localizations. ""Software updates available" went through Google Translate, so I would not be shocked if some of those localizations are not great.

#### Examples:
English:
```
/* Multiple Updates message */
"%@ pending updates" = "%@ pending updates";

/* One Update message */
"1 pending update" = "1 pending update";

/* Details label */
"Details" = "Details";

/* Forced Install Date summary */
"One or more items must be installed by %@" = "One or more items must be installed by %@";

/* Software updates available message */
"Software updates available" = "Software updates available";
```

Swedish:
```
/* Multiple Update message */
"%@ pending updates" = "%@ uppdateringar väntar";

/* One Update message */
"1 pending update" = "1 uppdatering väntar";

/* Details label */
"Details" = "Detaljer";

/* Forced Install Date summary */
"One or more items must be installed by %@" = "Ett eller flera objekt måste installeras senast %@";

/* Software updates available message */
"Software updates available" = "Programuppdateringar finns";
```