A core feature of Munki is keeping software up-to-date. Every time it runs, it compares the versions it has on the server against the versions installed on the local machine and updates any software at a lower version than it has on the server.

Munki's default behavior when an item on the local machine has a _higher_ version than that on the server is to leave it alone. This is great when you have users that for whatever reason need to test newer versions (or perhaps they are actually _developing_ the newer version of the software).

Munki doesn't have a built-in mechanism to downgrade software. Apple's installer (and installer packages) do not natively support that functionality. Installing an older version of a package over a newer install may or may not result in the desired outcome.

But it is possible to downgrade software using Munki. Here's one example of doing so:  
https://managingosx.wordpress.com/2018/03/15/using-munki-to-revert-or-downgrade-software/

Note that this is not, strictly speaking, "downgrading". It's really forcing a specific version. Machines with a lower version will be upgraded to this version; machines with a newer version will be downgraded to this version.