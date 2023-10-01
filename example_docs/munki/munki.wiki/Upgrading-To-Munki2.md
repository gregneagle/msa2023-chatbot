### Introduction

Upgrading to Munki 2 is easy. You don't have to make any changes on your server if you don't want to.
Later, if you add Munki 2-specific data to your Munki server, any clients running Munki 1 will simply ignore the extra data. Munki (1) and Munki 2 clients can co-exist and use the same server.

### Details

- Start by upgrading a few clients with the Munki 2 tools. See here https://munkibuilds.org for the latest versions.
- Munki (1) can install the Munki 2 tools. Just import them as you would previous versions of Munki.
- If you use [AutoPkg](https://github.com/autopkg/autopkg) (and you should) add the autopkg/recipes repo and use the munkitools2.munki recipe to import the new tools into your Munki repo.
- Start importing icons into your Munki repo. See [[Product Icons|Product Icons]] for more info.
- Add category and developer info to your pkginfo files. Focus initially on items in optional_installs (if you have any).
