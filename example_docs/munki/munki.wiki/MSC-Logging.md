_Logging user actions in Managed Software Center GUI_

### Introduction

One can enable exact logging of user actions in the Managed Software Center (MSC) GUI app. This can help to verify that various events within the GUI are occurring, e.g. 

- When did a user last see a popup notification to update?
- Did a user choose to install updates, or defer until later?
- Did the user see available Apple updates?
- Are available optional software choices being reviewed?

With MSU logging the Munki admin can determine these facts.

### Enable GUI Logging

By default logs regarding actions in the GUI are disabled. (The main GUI client used to be named Managed Software Update, so abbreviations in keys described hereafter retain the previous naming, similar to how launchd jobs use the original googlecode (RIP) hosting designation.) To enable GUI logging, set the key MSULogEnabled to True in [ManagedInstalls.plist](Preferences) on Munki clients:

```
sudo defaults write /Library/Preferences/ManagedInstalls MSULogEnabled -bool TRUE
```

Additional debug logging about internal actions in Managed Software Center can be obtained by setting another key:

```
sudo defaults write /Library/Preferences/ManagedInstalls MSUDebugLogEnabled -bool TRUE
```

### Log Location and Format

Logs are written to the directory:

`/Users/Shared/.com.googlecode.munki.ManagedSoftwareUpdate.logs/`

Multiple log files may exist in this directory. Each user who runs MSU will have 1 or more log files written.  By default the log filename will be "*username*.log", however if permissions problems occur additional log files will be written with random suffixes. This is done to avoid potential security problems due to the global writable nature of /Users/Shared/.

The log file consists of one text representation of a log event after another, separated by newlines.

  `float_timestamp INFO username : @@source:event@@ description`

e.g.
  `1300743459.788060 INFO user : @@MSU:appleupdates@@`

Note that log files are opened, written to, and closed upon each single log event write, even during one MSC application instance. Therefore external third party tools to roll or process logs should not have much problem with dangling open files, etc.

### Log Event Properties

Each log event has 4-5 properties:
- Timestamp at which the item was written
- Username of the logged in user
- Source of the event (source)
- Event name (event)
- Optional descriptive text (desc) to supply more detail.

The following table describes source/event pairs in more detail:

<table>
  <tr><th>source</th><th>event</th><th>desc</th><th>Description</th></tr>
  <tr><td>MSU</td><td>launched</td><td></td><td>MSU launched and presented the initial GUI window to interact with the user.</td></tr>
  <tr><td>MSU</td><td>exit_munkistatus</td><td></td><td>This MSU instance launched only to present a status window, and now it is exiting.</td></tr>
  <tr><td>MSU</td><td>exit_installwithnologout</td><td></td><td>MSU is now exiting after being told to install without logout.</td></tr>
  <tr><td>MSU</td><td>no_updates</td><td></td><td>MSU was started manually but no updates are available.</td></tr>
  <tr><td>MSU</td><td>cant_update</td><td>cannot contact server</td><td>Underlying munki cannot contact the server, therefore updates cannot occur (and MSU is reporting this).</td></tr>
  <tr><td>MSU</td><td>cant_update</td><td>failed preflight</td><td>Underlying munki tried to run managedsoftwareupdate, preflight failed, therefore updates cannot occur.</td></tr>
  <tr><td>MSU</td><td>conflicting_apps</td><td>(application names)</td><td>An application could not be installed because conflicting apps in (desc) are running.  The user was told to quit these apps.</td></tr>
  <tr><td>MSU</td><td>cannot_start</td><td></td><td>Total configuration problem preventing managedsoftwareupdate from running.</td></tr>
  <tr><td>MSU</td><td>appleupdates</td><td></td><td>Available Apple Software Update packages were presented to the user.</td></tr>
  <tr><td>user</td><td>cancelled</td><td></td><td>User was given the choice, after deciding to install packages, to optionally install with logout, or just stay logged in and perform the install.  Instead of picking an install action, the user hit "cancel" and did not complete the choice, thus aborting the install.</td></tr>
  <tr><td>user</td><td>exit_later_clicked</td><td></td><td>The user clicked the "later" button and deferred installation of available packages until next MSU run.</td></tr>
  <tr><td>user</td><td>install_with_logout</td><td></td><td>The user selected the "install and logout" option.</td></tr>
  <tr><td>user</td><td>install_without_logout</td><td></td><td>The user selected the "install without logout" option.</td></tr>
  <tr><td>user</td><td>quit</td><td></td><td>MSU is exiting after doing nothing, either because of errors (like MSU:cant_update) or because no updates were available to install.</td></tr>
  <tr><td>user</td><td>view_optional_software</td><td></td><td>User clicked the View Optional Software button.</td></tr>
</table>

### Log Growth Behavior

Once logs are enabled, the logs will be written to at any point where the MSC GUI generates an event. It is up to the Munki admin to process these logs in some way, and also to roll them away and/or clean them up. 

One potential place to perform log harvesting and cleanup would be in a preflight or postflight script.