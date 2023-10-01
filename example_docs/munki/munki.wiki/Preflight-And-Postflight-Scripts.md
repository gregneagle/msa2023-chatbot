_Information about munki preflight and postflight scripts_

### Introduction

`managedsoftwareupdate` supports optional preflight and postflight scripts. A preflight script is executed before `managedsoftwareupdate` does the bulk of its work. A non-zero exit code causes `managedsoftwareupdate` to abort its run. A postflight script is executed just before `managedsoftwareupdate` exits. It's a good place to analyze the logs and report errors to a central location.


### Details

Both the preflight and postflight scripts must reside in the same directory as `managedsoftwareupdate`.

A preflight script must be named "preflight" and have no extension. It must be marked as executable. A non-zero exit code causes `managedsoftwareupdate` to exit.

A postflight script must be named "postflight" and have no extension. It must be marked as executable.

Both scripts are passed a single parameter - the "runtype". This allows the script to distinguish between the various "modes" in which `managedsoftwareupdate` runs.  These runtypes have not yet been formally defined, and may change in the future. Here are the current runtypes:

- auto - this corresponds to the periodic run of managedsoftwareupdate, currently controlled by /Library/LaunchDaemons/com.googlecode.munki.managedsoftwareupdate-check.plist

- logoutinstall - this runtype occurs when a user has chosen to install updates using Managed Software Center.app and is logging out and installing (because the items to be installed require a logout or restart). This always happens at the login window.

- checkandinstallatstartup - designed for the initial bootstrapping of a machine, this runtype causes munki to do a check (and install if needed) at startup. Triggered by the existence of /Users/Shared/.com.googlecode.munki.checkandinstallatstartup  This always happens at the login window.

- installwithnologout - user has chosen to install updates without logging out.

- manualcheck - user has launched Managed Software Center.app manually, and it is checking for updates.

- custom - None of the above.

Note that since the pre and postflight scripts are in the same directory as `managedsoftwareupdate`, if they are written in python, they can easily import any of the modules in munkilib, including munkistatus, which would allow the scripts to provide user feedback in a manner similar to the other Munki tools.

The postflight script is an ideal place to parse the logs from the current `managedsoftwareupdate` run and forward errors or warnings to a central location, via email or a web cgi, or perhaps code that adds records to a database.

### Reporting consoles

Reporting consoles like [Sal](https://github.com/salopensource/sal) and [MunkiReport-PHP](https://github.com/munkireport/munkireport-php/) make use of `managedsoftwareupdate` preflight and postflight scripts to upload client data to their respective databases.

### Examples

Here are two examples uses of preflight scripting with their own documentation on the wiki:
- [[Dynamic Client Configurations Via Preflight Scripting]]
- [[WPKG like Dynamic Manifests Without CGI]]

Here's an example of a script that emails warnings or errors to an administrator:

```python
#!/usr/bin/python
# encoding: utf-8
"""
managedsoftwareupdate postflight
    
Created by Greg Neagle on 2010-06-02.
"""
    
import sys
import os
    
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import formatdate
from email import Encoders
import plistlib
    
# Change the following as needed
mail_from = "root@myorg.org"
mail_to = ["admin@myorg.org"]
smtpserver = "smtp.myorg.org"
managed_installs_dir = "/Library/Managed Installs"
    
def send_mail(send_from, send_to, 
              subject, text, files=[], 
              server="localhost"):
    assert type(send_to)==list
    assert type(files)==list
    
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ", ".join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    
    msg.attach( MIMEText(text) )
    
    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(f,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 
                        'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)
    
    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()
    
    
def main():    
    report = os.path.join(managed_installs_dir, "ManagedInstallReport.plist")
    if os.path.exists(report):
        pl = plistlib.readPlist(report)
        errors = pl.get("Errors","")
        warnings = pl.get("Warnings","")
        if not (errors or warnings):
            return
    
        subject = ""
        body = "The following issues were reported:\n\n"
        if errors:
            subject = "[Managed Installs errors] on %s" % os.uname()[1]
            body = body + "Errors:\n%s\n\n" % "\n".join(errors)
        if warnings:
            if not subject:
                subject = "[Managed Installs warnings] on %s" % os.uname()[1]
            body = body + "Warnings:\n%s\n\n" % "\n".join(warnings)
    
        body = body + "A full report is attached.\n"
        attachments = [report]
    
        send_mail(mail_from, 
                  mail_to, 
                  subject, 
                  body, 
                  attachments,
                  smtpserver)
    
    
if __name__ == '__main__':
    main()
```