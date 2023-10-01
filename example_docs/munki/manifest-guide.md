+++
date = "2016-07-11T19:01:08-04:00"
draft = false
title = "An opinionated guide to Munki manifests"

+++

I've been using [Munki](https://github.com/munki/munki) to manage Macs in enterprise environments for at least three years now, and frequently hang out in the #munki channel on the MacAdmins Slack. A few times a week there's someone new who comes in to ask about Munki, and inevitably, the question of how to structure manifests comes up. What follows is an opinionated list of "best practices" that you should follow as a Munki beginner.

### Manifests are just XML Property Lists
First, let's get this out of the way. There's nothing special about a manifest. It's a text file.
Here's what a typical manifest might look like:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>catalogs</key>
    <array>
        <string>production</string>
    </array>
    <key>included_manifests</key>
    <array>
        <string>labs-nh</string>
    </array>
</dict>
</plist>
```

Why is it important to know that manifests are just text files? It means that you can use `grep`/`sed`/`awk`/`python` or even search&replace in TextEdit to edit one or more of these.

### Create a unique manifest for each Mac in your ogranization
...and name the manifest with either the `serial_number` or `hostname` of the device that the manifest is intended for.

From the munki wiki:

| Key | Type | Default|
|-----|------|--------|
|ClientIdentifier	|string		| Identifier for munki client. Usually is the same as a manifest name on the munki server. If this is empty or undefined, Munki will attempt the following identifiers, in order: fully-qualified hostname, "short" hostname, serial number and finally, "site_default"|

Munki has pretty good default settings, and the usefulness of the above default cannot be overstated. Here's another way to say the same thing, which might make it clearer:
When Munki checks with the server, it will use the `ClientIdentifier` setting as the name of the maifest it's looking for.
You're probably thinking of setting it to `student` or `faculty` or `lab101`, but what if you didn't configure that setting at all?  
First thing the client will do is contact the server looking for FQDN, ex `my_hostname.mycopany.com`. If it doesn't find one, the client will then ask the server for the hostname, ex `my_hostname`. If it cannot find that, it will search for the device serial number, which could be something like `YM94209V4PC` or whatever the device serial number is. Finally, if it can't find any of the above, it will check for `site_default` (name this manifest exactly that -- `site_default`).

You might think that it's tedious to create 100-5000+ unique manifests, but it's not. You can `cp` in a loop in bash. Once you figure out what one student manifest looks like, you can [figure out how to duplicate ](http://unix.stackexchange.com/questions/10856/copy-multiple-files-and-append-to-end-of-filename) a thousand copies in a few minutes.  
I tend to also create some templates for myself like `student_template`, `faculty_template` etc that I duplicate whenever we get a new Mac.  
You should follow this advice, because it's much more tedious to figure out how to change your initial setup when you must have some unique settings for a specific device in a group.

### You can include a manifest inside a manifest
I told you that you must have a unique manifest for each device, which sounds like too much work. The truth is, that most of your "top level manifests"(the ones you make with the hostname or serial number) just have a list of `included_manifests` and a catalog. The included manifests, or "group manifests" have the actual list of applications which you want to manage. Let's see what this structure might look like:

```
C02K503BFS7J
└── lab-101
    └── labs-common
        └── common
```

In the example above, we have 4 nested manifest. The top level one, is the `C02K503BFS7J`, which has the catalog set to `production`. This manifest includes the `lab-101` manifest, which has some applications specific to that lab, and include `labs-common`, which in turn has a list of common software for all the labs. Finally, the `labs-common` includes a `common` manifest which is common across all my devices.

### Never set a catalog on group manifests
In the example above, *only* the `C02K503BFS7J` manifest should have a catalog set. All the included manifests, will source from that catalog.
This is not a best practice, but rather an often missed part of the documentation. If your included manifests have a catalog which is different from the top level one, you will have a bad time.

### Don't use munki-enroll
Remember, I said this would be an opinionated blog post. `munki-enroll` is a server/client tool which aims to automate some of the things I've described above. If you already know how it works, and know Munki well, then it might be useful to you. But, I see a lot of new users who are already confused about setting up Munki, get themselves deeper into trouble with this tool. My advice is to skip it until you're comfortable doing things on your own, and then evaluate it for yourself later on.

### Use a custom manifest for testing
Finally, a useful tip that I've only found out myself after about ~2 years of using Munki. Say you have some package in your repo that you would like to only install once, or only on a few machines, but don't want to add it to the production catalog. Maybe you're doing this to test how a package behaves with a particular CPU.

`managedsoftwareupdate` has a useful `  --id=ID               Alternate identifier for manifest retrieval` option.

```
sudo managedsoftwareupdate -vvv --checkonly --munkipkgsonly --id=testonly
```
This let's you add your package to a custom manifest like `testonly`, and then use it on the client to install that package just once, without changing any settings.

### Watch this video
[Getting Started with Munki - Greg Neagle](http://macdevops.ca/MDO2015/greg/NewStandardPlayer.html?plugin=HTML5)

Greg Neagle does a great intro to Munki and goes into details into `manifests`,`catalogs` and `pkgsinfos`. Munki will save you 1000s of hours over ARD, Casper or other poor software management tools you use, so this 30 minutes is definitely worth your time :)
