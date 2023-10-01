_Munki repository with Git version control_

### Introduction

This document is not intended as a git tutorial (you can find plenty of them online) but as a guide to setting up a version controlled munki repository with larger organizations in mind. Managing a munki repository with git version control provides some advantages over the traditional way of editing files in place. Just to name a few:
- You can go back in time
- Changes to the repo get documented through commits
- Many administrators can work on the repo at the same time
- A change in the repo is *not* immediately available to clients
- With distributed version control, you can easily checkout copies of the repository to different web servers or admin machines

One thing that I'd like to point out before even starting: Version control is not an alternative for backups. And backing up is not an alternative for version control. Use both.


#### Requirements

- Mac OS X admin computer(s) with munkitools and git installed
- Web server that hosts the munki repository and has git installed
- Optional, a second server to host the git repository

Suggested additions:
- Public-key authentication for SSH connections. This will definitely speed things up

In the following examples we are using a single Red Hat Enterprise Linux server for serving both the munki repository and the central git repository. Munki is served over HTTP and write access to git repositories is only done over SSH connections.


#### Installing git

OS X doesn't include git by default. To fix this, there are two easy methods:

1. If you are running 10.9 or later, just open Terminal.app and run `git`. You will get prompted to install the command line developer tools if they are not installed.
1. Download a pre-built installer package from the [Git website](http://git-scm.com/downloads)
 
After installing, configure your environment by telling git a bit about yourself (these are used in commits):

```
git config --global user.email john.doe@company.com
git config --global user.name "John Doe"
```

### Setting things up

First of all, decide where to host git repositories. This can be a directory on the munki server itself or a directory on a completely different server. In this document we are using the following:

- Server name: ```munki```
- Central git repository: ```munki:/var/git-repos/munki-test.git/```
- Munki virtual host: ```munki:/var/www/virtual.hosts/munki/```

#### Central git repository

Create a new empty shared git repository with the following commands:

```
mkdir /var/git-repos/munki-test.git/
chown root:your_admin_group /var/git-repos/munki-test.git/
chmod g+swx /var/git-repos/munki-test.git/
cd /var/git-repos/munki-test.git
git --bare init --shared=group
```

A bare git repository means that there is no working copy checked out. Also notice that when we used the ```--shared=group``` option when initializing the repo, our admin group was given a read/write access to the repository. This is what the newly created repository should look like:

```
$ ls -la
total 40
drwxrwsr-x 7 root your_admin_group 4096 Jan 13 12:49 .
drwxr-xr-x 5 root root             4096 Jan 13 12:47 ..
-rw-rw-r-- 1 root your_admin_group   23 Jan 13 12:49 HEAD
drwxrwsr-x 2 root your_admin_group 4096 Jan 13 12:49 branches
-rw-rw-r-- 1 root your_admin_group  126 Jan 13 12:49 config
-rw-rw-r-- 1 root your_admin_group   58 Jan 13 12:49 description
drwxrwsr-x 2 root your_admin_group 4096 Jan 13 12:49 hooks
drwxrwsr-x 2 root your_admin_group 4096 Jan 13 12:49 info
drwxrwsr-x 4 root your_admin_group 4096 Jan 13 12:49 objects
drwxrwsr-x 4 root your_admin_group 4096 Jan 13 12:49 refs
```


#### Munki virtual host

Next we're going to prepare some things for a second repository under /var/www/virtual.hosts/munki/repo/. This will be the munki repository that clients access with HTTP/HTTPS. We're choosing not to include the pkgs directory in git version control because of it's possibly large size. That means that you have to use some other means to copy the .dmg/.pkg files to your server (munki-import, rsync, scp or something else). Everything except the packages are kept under version control. The actual exclusion with .gitignore file is done on next step during the initial import.

Create the repo and repo/pkgs directories and give your admin group the ability to copy new packages.

```
mkdir /var/www/virtual.hosts/munki/repo/
cd /var/www/virtual.hosts/munki/repo/
mkdir pkgs
chown root:your_admin_group pkgs/
chmod g+w pkgs/
```

#### Adding content

Now, on your local admin mac, either create a new munki repository or go to an existing one and make an initial import with git.

1. Create an empty Git repository:

   ```
   cd /Users/Shared/munki/testrepo/
   git init
   ```

1. Create a ```.gitignore``` file to exclude a set of specific files. In this case disk images and packages are excluded. This ignore file will automatically go to our central repository so this is a "one-time" configuration.

   ```
   # Skip directories
   catalogs
   pkgs
   ```

   or

   ```
   # Skip all dmg files
   *.dmg
   # Skip all packages
   *.pkg
   *.mpkg
   ```

1. At this point you should add some content to the repo. Create pkginfo files, manifests and run makecatalogs...

1. Get a glimpse of what git sees in your repo

   ```
   git status
   ```

1. Import everything

   ```
   git add .
   ```

1. Create your first commit

   ```
   git commit -m "Initial import"
   ```

1. Push the contents of your local repo to the central git repository

   ```
   git push munki:/var/git-repos/munki-test.git --all
   ```

1. Clone the central repository to your virtual host

   ```
   ssh user@munki
   cd /var/www/virtual.hosts/munki/
   git clone /var/git-repos/munki-test.git repo
   ```

#### Providing access to other administrators

When you have a working central git repository, other administrators can simply do a git clone operation to get everything up and running.

```
git clone user@munki:/var/git-repos/munki-test.git
```

### Everyday workflow

When everything is set up correctly, working with munki+git should be something like this:

1. Check the central repository for any changes made by other administrators:

   ```
   git pull
   ```

1. Make your changes to manifests, pkginfos, catalogs, etc. and run makecatalogs if needed. Some useful commands for git:

   ```
   # Get the status of your local repo
   git status
   
   # Show commit history
   git log
   
   # What changes have I made?
   git diff
   git diff <file>
   ```

1. Commit your changes to your local repository:

   ```
   # Add a specific file
   git add <file>
   
   # or add everything
   git add .
   
   # Do a commit. This will open a commit message in your default $EDITOR. Write it, save and you're done.
   git commit -a
   ```

1. Push your changes to the central repository:

   ```
   git push
   ```

1. Finally, when you're ready to make the changes available to clients:

   ```
   ssh user@munki
   cd /var/www/virtual.hosts/munki/repo/
   git pull
   ```

### Tips & Tricks

#### Email notifications

You can configure your central git repository to send email notifications whenever someone makes a commit. This is usually a must-have when working with multiple administrators. The default git install includes a post-receive hook for this but you have to enable and configure it. Note that these changes are made on server side (your central git repository).

First, locate the `post-receive-email` script included with git. Usually it can be found from: `/usr/share/doc/git-core/contrib/hooks/post-receive-email`

The script can also be found online from :
[git.kernel.org / git.git / contrib / hooks / post-receive-email](http://git.kernel.org/?p=git/git.git;a=blob;f=contrib/hooks/post-receive-email;h=60cbab65d3f8230be3041a13fac2fd9f9b3018d5;hb=HEAD)

The following instructions are actually from the file itself.

Move to that folder and give the script execute rights (if it doesn't have them).

```
cd /usr/share/doc/git-core/contrib/hooks/
chmod a+x post-receive-email
```

Go to your central git repository and enable the post-receive hook.

```
cd /path/to/your/repository.git
ln -sf /usr/share/doc/git-core/contrib/hooks/post-receive-email hooks/post-receive
```

Configure your repository to send emails

```
cd /path/to/your/repository.git
echo "Name of Your Repository" > description
git config --add hooks.mailinglist yourmailinglist@example.com
git config --add hooks.emailprefix "[Munki] "
git config --add hooks.envelopesender sender@example.com
```

Now, if all went well. You should get an email every time someone does a "git push" from their local machines to the central repository.


#### Hiding the .git directory from clients

Because of git's distributed model, every git repository always includes the whole history. This is usually a good thing but if you don't want this to be freely readable by your clients over HTTP, you can deny access to it by using standard directory overrides in either .htaccess files or your main httpd.conf.

Add something like this:

```
<Directory "/var/www/virtual.hosts/munki/repo/.git">
    Order deny,allow
    Deny from all
</Directory>
```

Now, if someone tries to access http://munki/repo/.git/, all they get is "403 Forbidden".


#### Links

- [Git home page](http://git-scm.com/)
- [Pro Git Book](https://git-scm.com/book/en/v2)
- [Git Community Book](https://shafiul.github.io/gitbook/)
