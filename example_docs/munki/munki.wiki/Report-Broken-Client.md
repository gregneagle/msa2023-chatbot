### Introduction

This optional functionality provides Munki admins a way to get notified of clients in the field that are broken. Admins can choose to post a report to any existing report server or simply email themselves by simply placing an executable script named "report_broken_clients" in the munkitools root (/usr/local/munki) ala PreflightAndPostflightScripts.

### Details

Currently the only "broken" case that is if /usr/bin/python does not contain the Apple provided Objective-C Python bindings.  This could happen if the user of the machine installs a non-Apple provided version of Python over the top of /usr/bin/python.

managedsoftwareupdate simply tries to import an ObjC-backed Python module and calls the "report_broken_client" script if it fails to import.

At the point of this error, it's unknown what the managedsoftware runtype was, so the script is simply passed "custom".

In the future there may be more failure cases, in which case the script may be passed different information.

#### report_broken_clients script

Much like preflight and postflight scripts, this script must be executable and only writable by root:wheel otherwise it will not be executed.  Also, it can be written in any language supported by the OS X system it's executed on.