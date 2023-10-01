### Introduction

Upgrading to Munki 5 is easy. You don't have to make any changes on your server if you are currently supporting clients running Munki 3 or Munki 4.

### Details

- Start by upgrading your admin workstation to Munki 5.
- Next, upgrade a few clients with the Munki 5 tools. See [here](https://github.com/munki/munki/releases) for the latest versions.
- Older versions of Munki can install the Munki 5 tools. Just import them as you would previous versions of Munki. See [[Updating Munki Tools]].
- If you use [AutoPkg](https://github.com/autopkg/autopkg) (and you should) add the autopkg/recipes repo and use the munkitools5.munki recipe to import the new tools into your Munki repo.
