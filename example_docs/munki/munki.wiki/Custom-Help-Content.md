_Adding custom help for Managed Software Center_

### Details

Managed Software Center will check [Munki's preferences](Preferences) for a HelpURL key. If that key is present and the user chooses "Managed Software Center Help" from Managed Software Center's Help menu, that URL will be opened using the URL's default application. (In other words, http/https URLs will be opened by the user's default browser, etc.)

```
sudo defaults write /Library/Preferences/ManagedInstalls HelpURL http://webserver.my.org/msc_help.html
```

(or use MCX or a configuration profile, etc...)