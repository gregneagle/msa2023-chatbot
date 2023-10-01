### Introduction

Upgrading to Munki 4 is easy. You don't have to make any changes on your server if you are currently supporting clients running Munki 3.

### Details

- Start by upgrading your admin workstation to Munki 4.
- Next, upgrade a few clients with the Munki 4 tools. See [here](https://github.com/munki/munki/releases) for the latest versions.
- Munki (3) can install the Munki 4 tools. Just import them as you would previous versions of Munki. See [[Updating Munki Tools]].
- If you use [AutoPkg](https://github.com/autopkg/autopkg) (and you should) add the autopkg/recipes repo and use the munkitools4.munki recipe to import the new tools into your Munki repo.

