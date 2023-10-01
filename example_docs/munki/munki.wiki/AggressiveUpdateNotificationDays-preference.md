Munki 5's more aggressive update behaviors begin when one or more updates have been pending for more than 14 days by default.

Munki admins can control this behavior by setting the new AggressiveUpdateNotificationDays preference. This should be an integer representing the number of days after which pending updates should trigger the more aggressive behavior.

Set it to 0 to never trigger the aggressive behavior.
