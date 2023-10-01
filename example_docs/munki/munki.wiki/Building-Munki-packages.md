### Building a Munki Installer Package

Milestone releases of the Munki tools are made available here: https://github.com/munki/munki/releases

### Building it yourself

You can also build a Munki installer package yourself.

#### Requirements

* Xcode -- the current release and build scripts are known to work under Xcode 12. Using other versions of Xcode might lead to unexpected (or at least different!) results. Building older versions of Munki might require older versions of Xcode (typically whatever version of Xcode was current when that version of Munki was current).
* git (which you get for "free" when you install Xcode...)

#### Catalina(+) note
New privacy protections introduced in Catalina might cause parts of the build process to fail mysteriously if your local git clone of the Munki code is in a directory affected by these protections (for example, ~/Desktop, ~/Documents, ~/Downloads, or a network volume). /Users/Shared is a writeable space on most Macs that is not (currently) affected by these new privacy protections. (A common failure symptom caused by this is inability to read `code/client/munkilib/version.plist`)

#### Procedure

In a directory you can write to and that is not affected by macOS privacy protections (for example, /Users/Shared), run:

`git clone https://github.com/munki/munki`
This will create a new "munki" directory containing the latest git repo. 
**Do NOT download the zip or tar'd release, as that would not have the git directories that versioning logic is based on.**

Change into the directory:

`cd munki`

Run the build script:

`./code/tools/make_munki_mpkg.sh`

Provide your password when requested (certain steps require sudo).

If the script runs successfully, it will tell you where to find the Installer package:

`Distribution package created at /Users/Shared/munki-git/munki/munkitools-3.0.0.3333.pkg.`

#### Building other versions of Munki

You can also build other versions of Munki using the `make_munki_mpkg_from_git.sh` script.

`./code/tools/make_munki_mpkg_from_git.sh -b <tagname>` will build a Munki release pointed to by the tag name. `% git tag` will show you the available tags.

You may need an older version of Xcode to successfully build the applications included with older versions of Munki, and/or access to older OS X SDKs. Almost certainly this is not worth the effort and you should stick with a pre-built package from the Releases section.

`./code/tools/make_munki_mpkg_from_git.sh -b BRANCHNAME` will build Munki based on the code in BRANCHNAME.

`./code/tools/make_munki_mpkg_from_git.sh -b TAGNAME` will build Munki based on the code at TAGNAME.

`./code/tools/make_munki_mpkg_from_git.sh -r GIT_REVISION_HASH` will build Munki based on the code in a particular Git commit (revision).

#### More info on the build scripts

Both `make_munki_mpkg.sh` and `make_munki_mpkg_from_git.sh` support the `-h` option for help on the various options.
