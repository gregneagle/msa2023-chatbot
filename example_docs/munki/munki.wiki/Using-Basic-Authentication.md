_How to restrict access to your munki repository using HTTP Basic Authentication_

### Introduction

If you're using munki to distribute licensed software, you'll want to restrict access to the repository. It's possible to use client certificates (as described in [Using Munki With SSL Client Certificates](https://github.com/munki/munki/wiki/Using%20Munki%20With%20SSL%20Client%20Certificates), but HTTP Basic Authentication is much easier to set up.


### Details

[HTTP Basic Authentication](http://en.wikipedia.org/wiki/Basic_access_authentication) ([RFC2617](http://tools.ietf.org/html/rfc2617)) is a very simple authentication scheme that simply sends a username and a password (separated by a colon and base64 encoded) in the headers of each HTTP request. If it's used over unencrypted HTTP it's insecure (as it's trivial to sniff the password on the network), but in combination with HTTPS and a signed server certificate it's reasonably secure.


#### Restricting Access to the Repository

#### Using Mac OS X Server 10.6

I will assume that you already have a repository set up that clients can connect to - if not, refer to the [10.6 Web Technologies Administration guide](http://images.apple.com/server/macosx/docs/Web_Tech_Admin_v10.6.pdf). I strongly recommend that you use SSL for your munki repository, with a signed server certificate. If you don't have one, refer to the [10.6 Getting Started guide](http://images.apple.com/server/macosx/docs/Getting_Started_v10.6.pdf).

Since you can't edit the Apache configuration files directly (well you can, but they will get overwritten by Server Admin), you have to enable [overrides](http://httpd.apache.org/docs/2.2/mod/core.html#allowoverride).

1. Launch Server Admin and connect to your server.
1. Select the Web service, and switch to the Sites tab.
1. Select the site that hosts your munki repository.
1. Select the Options tab, and enable Allow All Overrides.
  - NB: Your repository has to live under the Web Folder root, and not under an Alias. Overrides (.htaccess files) will not be enabled for folders under Aliases.
1. Click Save.

You then have to create a [.htaccess](http://httpd.apache.org/docs/2.2/howto/htaccess.html) file in the root of your munki repository:

1. Launch Terminal.app and cd to your repo_root.
1. Create a user that will be used to access the repository using htpasswd (here `munki` is used as an example):

    ```bash
    $ htpasswd -c .htpasswd munki
    New password: 
    Re-type new password: 
    Adding password for user munki
    ```

1. You can add more users to the `.htpasswd` file using `htpasswd .htpasswd ANOTHERUSER` if you don't want to use the same username and password for all clients.
1. Using vi, emacs, pico or nano, create a new file called `.htaccess` (including the leading dot, making the file hidden).
1. Enable basic authentication with:

    ```
    AuthType Basic
    AuthName "Munki Repository"
    AuthUserFile /path/to/your/munki/repo_root/.htpasswd
    Require valid-user
    ```

1. While you're at it, you might want to restrict access based on IP address as well:

    ```
    Order Deny,Allow
    Deny from all
    Allow from 192.168.0.0/16
    ```

1. Save the file and exit.


### Using an Apache Server

I will assume that you already have a repository set up that clients can connect to.

1. In the terminal, cd to your munki repo_root.
1. Create a user that will be used to access the repository using htpasswd (here `munki` is used as an example):

    ```bash
    $ htpasswd -c .htpasswd munki
    New password: 
    Re-type new password: 
    Adding password for user munki
    ```

1. You can add more users to the `.htpasswd` file using `htpasswd .htpasswd ANOTHERUSER` if you don't want to use the same username and password for all clients.
1. Open the Apache configuration file (typically `/etc/apache2/httpd.conf`) in a text editor (as root or using [sudo](http://en.wikipedia.org/wiki/Sudo)).
1. Find the `<Directory>` section for your munki repository, and after the existing configuration directives add:

    ```xml
      <Directory "/path/to/your/web/root">
          Options All +MultiViews -ExecCGI -Indexes -Includes  # Just an example
          AllowOverride None                                   # Just an example
          AuthType Basic
          AuthName "Munki Repository"
          AuthUserFile /path/to/your/munki/repo_root/.htpasswd
          Require valid-user
      </Directory>
    ```

1. While you're at it, you might want to restrict access based on IP address as well:

    ```
    Order Deny,Allow
    Deny from all
    Allow from 192.168.0.0/16
    ```

1. Save the file and exit.
 

#### Verify the Configuration

1. Verify that you get an authentication prompt if you try to view a catalog file in a web browser (e.g. `https://your.munki.server:8043/repo_root/catalogs/testing`).
1. Verify that you can authenticate as the user you created in step #2.
1. Verify that if you run `/usr/local/munki/managedsoftwareupdate --checkonly` on a client you get an error message saying that it can't access its manifest.


### Configuring the Clients to Use a Password

[HTTP Basic Authentication](http://en.wikipedia.org/wiki/Basic_access_authentication) consists of an extra `Authorization` header, which we can add to the ManagedInstalls.plist [[Preferences]] in the `AdditionalHttpHeaders` array. But first we have to [base64](http://en.wikipedia.org/wiki/Base64) encode the username and password:

```bash
munki-python -c 'import base64; print("Authorization: Basic %s" % base64.b64encode("USERNAME:PASSWORD".encode("UTF-8")).decode("UTF-8"))'
```

Substitute the username and password you created in the .htpasswd file in your repository in the above command.

The command will return a value similar to:

```bash
Authorization: Basic VVNFUk5BTUU6UEFTU1dPUkQ=
```

Add this key and value to [Munki's preferences](Preferences):

```bash
defaults write /Library/Preferences/ManagedInstalls AdditionalHttpHeaders -array "Authorization: Basic VVNFUk5BTUU6UEFTU1dPUkQ="
```

If you have multiple `AdditionalHttpHeaders` use -array-add, otherwise the whole array will be overwritten by the defaults command.

#### Protecting the Password From Local Users

As all users on a machine can read /Library/Preferences/ManagedInstalls.plist, they'll be able to read the password and access the repository. You can put the `AdditionalHttpHeaders` in root's preferences (`/private/var/root/Library/Preferences/ManagedInstalls.plist`) instead, which is only readable by administrators.

```bash
sudo defaults write ManagedInstalls AdditionalHttpHeaders -array "Authorization: Basic xxxxxxxxxxxxxxxxxxx"
```
is one way to write that value to root's preferences file. A script that is run by root with a line like:

```bash
/usr/bin/defaults write ManagedInstalls AdditionalHttpHeaders -array "Authorization: Basic xxxxxxxxxxxxxxxxxxx"
```
is another way to set that value. Avoid methods like:

```bash
defaults write /private/var/root/Library/Preferences/ManagedInstalls ...
```
as that may not cause the internal preferences cache to be updated right away.

#### Configuration Profile

The preference can also be included in a configuration profile using the key `AdditionalHttpHeaders` with an array of strings:

```
<key>AdditionalHttpHeaders</key>
<array>
	<string>Authorization: Basic VVNFUk5BTUU6UEFTU1dPUkQ=</string>
</array>
```

#### Verify the Client Configuration

1. Check that the client has the desired configuration by examining the output of `sudo managedsoftwareupdate --show-config`.
1. Verify that if you run `/usr/local/munki/managedsoftwareupdate --checkonly` on a client with the Authorization header configured that it successfully downloads the manifest and checks for updates.


### References

- [Munki's preferences](Preferences)
- http://en.wikipedia.org/wiki/Basic_access_authentication
- http://en.wikipedia.org/wiki/Base64
- http://tools.ietf.org/html/rfc2617
- http://httpd.apache.org/docs/2.2/howto/auth.html
- http://httpd.apache.org/docs/2.2/howto/access.html
- http://httpd.apache.org/docs/2.2/howto/htaccess.html
- http://httpd.apache.org/docs/2.2/mod/core.html#allowoverride
- http://images.apple.com/server/macosx/docs/Getting_Started_v10.6.pdf
- http://images.apple.com/server/macosx/docs/Web_Tech_Admin_v10.6.pdf
- http://images.apple.com/server/macosx/docs/Network_Services_Admin_v10.6.pdf