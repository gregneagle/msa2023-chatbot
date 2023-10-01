_Definition of common munki terms._

#### Catalog

A list of items available on the server, created by the makecatalogs tool.  There can be multiple catalogs.  Stored in the "catalogs" directory on the munki server.

#### Info File (or PkgInfo File)

A plist file that describes an installer item.  Stored in the "pkgsinfo" directory on the munki server.  Contains, among other things, a list of catalogs the installer item appears in.  All installer items are automatically included in the "all" catalog.

#### Installer Item

Piece of software to be installed.  May be be either a flat Apple package (.pkg), or a disk image (.dmg).  Stored in the "pkgs" directory, or sub-directories there of, on the munki server. (Flat packages, introduced with OS X 10.5, are packages in the form of a single file. "Bundle-style" packages are actually directories, and must be encapsulated in a disk image. This has the effect of converting them into a single file, making them easier to download from a web server.)

#### Manifest

Describes what software a client should have installed or uninstalled.  Stored in the "manifests" directory on the munki server.