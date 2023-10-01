Since in Munki 5, successful installation of Apple updates that require a restart now is much more dependent on user cooperation, Managed Software Center now provides additional "encouragement" and cues intended to help guide the user to do the right thing.

Updates that have been pending for more than two days now have an additional label showing how long they've been pending. Additional text may also appear near the top of this view. An example:

![](https://github.com/munki/munki/wiki/images/munki5-5.png)

If a user simply attempts to quit when in this state, they are prompted to install the Apple updates. If they elect to skip them (or cannot install them because of configuration profiles), the Apple updates are removed from view:

![](https://github.com/munki/munki/wiki/images/munki5-6.png)

If there are pending updates even older (the default age is 14 days), if the user attempts to quit, they are notified yet again:

![](https://github.com/munki/munki/wiki/images/munki5-7.png)

Note that the Quit button is disabled. After a five-second delay, it is enabled again:

![](https://github.com/munki/munki/wiki/images/munki5-8.png)

The timing of this more insistent alert is controlled by the [[AggressiveUpdateNotificationDays preference]].