_Tips on securing a Munki data repository_

### USING MUNKI WITH SSL CLIENT CERTIFICATES

#### INTRODUCTION

By default, Munki uses standard HTTP requests for transporting files, but like most web based transport, it can be secured using by HTTPS to encrypt communications with the web server. However, HTTPS only secures the contents of the data on the wire as it passes from host to host -- it does not have the facility to control which hosts or users can access a site.

If the data you choose to store in the Munki repo is considered sensitive or privileged, you will require a means of controlling exposure. To regulate access, Munki provides support for SSL Client Certificates to ensure only authorized clients utilize the Munki data.

#### REQUIREMENTS

This document assumes that you have already provisioned a web server for Munki, and are familiar with the basic tenets of Public Key Infrastructure and Apache HTTP Services. In addition, you should already have a web server with properly registered DNS for the host.

The examples and tools referenced in this document are based on the builtin Apache 2.2 httpd service in Mac OS X Server. Other web servers or Apache installations will be similar, but not in all cases.

To complete this demo, you will be required to download the provided materials.

 ==== [Click here to download the materials used in this demo.](https://github.com/munki/contrib/raw/master/UsingMunkiWithSSLClientCertificates-demo.zip) ====

Once you have downloaded the materials, unpack them, you can put them anywhere you like. When you have completed the initial setup, you will migrate the materials to a more appropriate location.

Disclaimer: The scripts provided in the materials folder are only intended to exemplify the basic operations required to secure and maintain a Munki+Apache repo. They should in no way be considered exhaustive or authoritative. If you to use these scripts in a production environment, you do so at your own risk.

*Note:* These scripts and configuration files might need to be adjusted in order to work on newer webserver versions such as Apache 2.4.x (and possibly newer versions of NGINX). At the bottom of this document there's a suggested fix for that.

#### CONTENTS

- Securing Apache
  - Certificates
    - Creating an OpenSSL Configuration
    - Creating a Certificate Authority
    - Creating a Server Certificate
    - Creating a Client Certificate
    - Revoking a Client Certificate
  - Installing the CA
  - Creating a Secure Virtual Host
    - Setup
- Configuring Munki to use SSL Certificates
- Troubleshooting

#### Securing Apache

To configure a secure Munki HTTPS repository, we will need to do two things: establish a Certificate Authority and create a Secure Virtual Host configuration for Apache to serve.

If you have not already done so, login to your server host and download the [demo materials](https://web.archive.org/web/20160123094601/http://munki.googlecode.com/files/UsingMunkiWithSSLClientCertificates-demo.zip). We will assume you to be working on the actual Munki web server for this portion of the demo.

NOTE: The certificates we are going to be generating are 1024 bits long. This is the lowest common denominator approach, instituted to avoid compatibility issues with Apache and like components.

##### Certificates

To setup the CA and other actions, we will use a series of scripts. These scripts use simple calls to the `/usr/bin/openssl` utility to batch configure many of the tedious operations required to perform these tasks. Those that have used `openssl` utility before know that it is largely interactive, and requires one to answer a great number of questions during execution.
		
- Creating an OpenSSL Configuration
	
	To expedite the setup, it is recommended that you create a custom OpenSSL configuration file to prepare some sane defaults during operation. Not only will this step save you some time later, but it will also ensure your answers remain consistent where they need to be.
	
1. In the unpacked materials folder, you will see a subfolder labeled `config`. Browse into that folder and begin by opening the `openssl.cnf` file in your text editor of choice. For more information about the `openssl.cnf` file, see the man page for `config`. Provided below are a list of default values you should edit before proceeding. You may need to add these keys in some cases:
    1. `default_days = 365` --> CRL Expiration period in days.
    1. `countryName_default = AU` --> Country Code. Two letters.
    1. `stateOrProvinceName_default` = Some-State --> Province/State. Not abbreviated.
    1. `localityName_default`	= Locality Name (eg, city) --> City
    1. `0.organizationName_default` = Internet Widgits Pty Ltd --> Company
    1. `organizationalUnitName_default` = Organizational Unit Name (eg, section) --> Department
    1. `commonName_default` = Common Name (eg, YOUR name) --> MUNKI_CA
       - This last default is singular. Unlike the rest of the defaults, *each certificate you create will have a unique CN*. I would suggest using a default indicated above.
    1. `emailAddress_default` = Email Address --> Administrator's Email
1. Once you have made the appropriate modifications to the openssl.cnf, you may save it and close the editor.

-----------

- Creating a Certificate Authority
	
	The easiest way to create a CA, is to use the supplied script `createCA.sh`. This script will create a self contained CA which you can migrate to a secure location later. We will not go into detail about the openssl demoCA structure here. If you need further information, consult Google or read the various man pages for the `openssl` utility.

1. Open Terminal.app and `cd` into the unpacked materials folder
    - Inside this directory you should see several folders listed: `bin`, `config`, `servers`, and `clients`.
1. Begin the setup by running the following command: `sudo ./bin/createCA.sh`
1. The first prompt you receive asks you to create a password.
    - This is for the CA's private key passphrase. Make it a good one, and remember it **always**. You will need to refer to this password time and again.
1. Next are a series of prompts for which you have already selected defaults by editing the `openssl.cnf` file.
    - You can select the default by simply hitting enter when prompted for a value.
1. Next we generate the Certificate Revocation List (CRL).
    - Enter the passphrase for the CA's private key. If you mess up, you will have to start over again or generate the CRL manually.
1. Setup is complete.
    - Inside your current working directory, you should have a new folder labeled `demoCA` which stores your PEM formatted `ca.crt` and `a.key`, as well as the other files need to manage your CA.
    - You are now ready to start signing certificate requests, and you will begin by signing the CSR for your server.
    - Do not close Terminal.app.

-----------

- Creating a Server Certificate
	
Creating a certificate for your server is a very similar process. We are going to use a script again, but there are two differences: We will remove the passphrase from the server's private key, and we need to select a specific CN for the server's certificate. 
	
Unlike the CA's key, we need to remove the passphrase from the server's private key because this certificate will be used in a non-interactive environment (httpd). Failure to do so would result in us having to type in the passphrase for the key each time we restarted the web service. 
	
The other difference is that we are going to use the server's fully qualified domain name (FQDN) for the CN portion of the server's certificate DN. Though this step is not strictly necessary in the present context, this will ensure that the certificate is uniquely identified with a particular host, in this case our server.
		
1. Begin by invoking the `newServer.sh` script, like this: `sudo ./bin/newServer.sh your.server.com`.
    - This script needs one argument -- the name of your server. It will verify this via DNS before continuing, so enter it properly.
1. The script will again ask you for a passphrase.
    - Do not worry about selecting a strong passphrase. You have to enter something, so use "xxxx" or something similar.
1. You will now be asked to remove the passphrase you just entered.
    - Enter the passphrase, and it will be removed from the key (this gives new meaning to the phrase "redundant security").
1. Next, you will use the defaults we set up to answer the questions, but **when prompted for the CN, use the FQDN of your Munki Server**.
    - You may also specify a different email address if so desired.
1. Two new questions here, `A challenge password []` and `An optional company name []:`.
    - Simply hit return to leave these attributes blank.
1. After the CSR is generated, we need to have the CA sign it to prove it's validity.
    - **You** are the CA, so when prompted to enter the passphrase, do so, and **choose yes and yes** respectively to `Sign the certificate? [y/n]` and `1 out of 1 certificate requests certified, commit? [y/n]`.
1. Once the above is complete, the script will install the server certificate and key under the `servers/<your.server.com>` directory for later use.
    - Server certificate creation is complete.
    - Do not close Terminal.app.

-----------

- Creating a Client Certificate
	
With our server certificate in hand, we are ready to create a client certificate/key pair that we can distribute to those we will grant access to the server. This step is identical to the previous in almost every way: 

*We still generate a private key*

*We still remove the passphrase*

*We still select a unique value for the CN*

*We still have the CA sign the CSR, but ...*

**Different Location**: In contrast to the server certificate, your end-product will be stored in `clients/<clientname>` -- that's easy enough to see, and makes sense too. 

**File Format**: Worthy of note, the `addClient.sh` script we are about to use will concatenate the certificate and private key into a single file that will make it more convenient to distribute.
	
1. Like before, invoke the script, using the full path and a single argument: `sudo ./bin/addClient.sh munki_client`
    - Note: The argument name is arbitrary, but if you want to use a client name with spaces, this script (and presumably the others) will not work.
    - This is a limitation of the script, primitive as it is. So, for the purposes of the demo, select a name that does not contain any spaces.
1. For instructions regarding selecting a passphrase, and it's subsequent removal, see steps 2 and 3 in the section above.
1. Again, we are going to be leveraging the defaults we setup (I am sure you are glad you did this now.), but **answer carefully when asked for a CN**.
    - **Enter the same name we provided as an argument to the script**: `munki_client`
1. Enter the CA private key password and we receive another familiar set of questions, `Sign the certificate? [y/n]` and `1 out of 1 certificate requests certified, commit? [y/n]`.
    - As before, leave them blank, and hit enter to continue.
1. At this stage, the script has all the information needed to generate a certificate/key pair combo file. It will do this without any further intervention. When it is complete you should find the file `clients/munki_client/munki_client.pem` is available to distribute to your client.
    - Client Certificate creation is complete.
    - Do not close Terminal.app.

-----------

- Revoking a Client Certificate
	
Before we continue with instructions for installing the CA, it is vital we touch on an important characteristic of leveraging PKI in this manner. What we are doing here is preparing to grant access to clients based solely on the possession of a certificate signed by our duly appointed Certificate Authority. Great! We only give the certs to people we trust so, no problem.
	
But, what if some black hat or maladjusted user absconds with the cert? Well, we could panic for little while and then resolve to wait for the certificate to expire, but that may take a long time... We could try and track down the hacker and make them give back the certificate and all the copies they made for their friends... Or maybe we just destroy the CA and start over... You get the picture. 
	
Enter the Certificate Revocation List. This is a list of all the certs that you have issued to clients, but you no longer wish to validate -- a blacklist of sorts. Good News: the `createCA.sh` script has already generated a CRL for you, all we need to do is get revoking.
	
Note: **DO NOT** revoke our previously created client cert unless you are willing to re-create it. We will need it later in the demo. If you choose, you can run through the setup for a separate client cert to try this script out.
	
1. To revoke a previously issued certificate, invoke: `sudo revokeCert.sh munki_client`
    - Where `munki_client` is the name of the certificate to revoke, without any file extension. (ie. If you created `clients/foobar` and distributed `foobar.pem`, you would send the argument `foobar`.)
    - Again, no spaces here. The scripts will choke.
1. When the script receives the argument, it will check to ensure you have first issued a certificate with that name before proceeding. If the client exeists, it will revoke the certificate and **restart the web server to force Apache to reload the CRL**.
    - Do not close Terminal.app.
	
-----------
	
#### Installing the CA

Once configured, your CA is ready to install, but where do you put it? Well, you can place it wherever you like as long the location is:

1. Secure
  - Choose a sensible location and ensure you apply appropriate permissions.
    - Suggested: `/private/etc` would be a good choice.
    - Permissions: The `createCA.sh` should apply appropriate permissions; see the script for further detail.
1. Accessible to Apache
    - Ensure that your CA is located in a place accessible to Apache, and has permissions appropriate to do so.

For the purposes of this demo, securely relocate the unpacked materials to the suggested location:
	
1. `cd /`
1. `sudo cp -R /path/to/unpacked/materials /private/etc/munki`
    - Do not close Terminal.app.

CHECK: When you are done, the `/private/etc/munki` directory should contain: `bin`, `clients`, `config`, `demoCA`, and `server`.
	
#### Creating a Secure Virtual Host

If you haven't noticed already, `/private/etc/munki/config` contains a boilerplate secure virtual host configuration for Apache: `munki.conf`. Also contained in the `config` directory is a separate archive: `munki-site.zip` -- this is the sample Munki repo that we will be using for the demo.

- Setup
	
We need to do three things here. The first thing is edit the virtual host configuration. Second, unpack the demo site. Again, this is based on Mac OS X Server default configurations. You can store the site anywhere you like, but we are going to be using a vanilla setup. The third thing we need to do is install the Apache virtual host.
	
NOTE: The virtual host configuration in the demo actually describes a secure virtual host, and a distinct "members-only" directory for the Munki repo. More on this below ...
		
1. Edit the Virtual Host Configuration
    - Grab a copy of the `munki.conf` and put it on your Desktop
    - Open the file in your editor of choice
        1. Edit the `ServerName` directive to match the FQDN of your server
        1. Edit the `ServerAdmin` directive to match the web admin's email address
        1. Edit the four SSL file directives to point to their appropriate files.
            - If you put the munki CA in `/private/etc`, then you will only need to edit the `SSLCertificateFile` and `SSLCertificateKeyFile` directives to match your server name.
        1. Edit the `SSLRequire` directive
            - The conditionals used in this directive are directly related to attributes of your client certificate's DN. Edit this carefully to match the applicable attributes. There is more information about this in the comments of the actual virtual host configuration file.
1. Setup the Site Folder
    - Open Terminal.app
    - `sudo cp /private/etc/munki/config/munki-site.zip /Library/WebServer/Documents`
    - `cd /Library/WebServer/Documents`
    - `sudo unzip /Library/WebServer/Documents/munki-site.zip`
    - `sudo chown -R root:admin /Library/WebServer/Documents/munki`
1. Setup the Virtual Host
    - Copy the `munki.conf` file to
    - `sudo cp ~/Desktop/munki.conf /private/etc/apache2/sites`
1. Restart the Web Server

This concludes the setup of our secure Munki repo. When the web services on your server are restarted, your secure site should be available at ...
	
https://your.server.com

Try it out in your browser. You should be prompted to download the server's public certificate and then be presented with an image. Likewise, the actual repository which lives one level down should also prompt you, but this time it will want *you* to supply the certificate ...

https://your.server.com/repo
	
If all went well, you should be prompted to supply a certificate. Don't worry about trying to install the certificate and testing it in your web browser. Web browsers can be irksome when dealing with client certs. We will do some testing in the next step.
	
If you do not achieve the expected results, or something went wrong, try running through the setup again or consult the Troubleshooting section at the end for this document for possible causes.

### Configuring Client to use SSL Certificates

The labour of setting up your secure web site is about to pay off. Configuring a Munki client to use certificate-based authentication couldn't be easier...

- Configuration
	
1. Install the Munki Package
    - You can download the latest Munki Mac OS X installer package [here](https://github.com/munki/munki/releases/latest).
1. Install the Client Certificate
    1. You will need to transport a copy of the client certificate `munki_client.pem` from the server's CA store to the intended client. Do this in any manner you see fit, (`scp` is a good choice) but place it on the Desktop for easy access.
    1. `sudo mkdir /Library/Managed\ Installs/certs`
    1. `sudo chmod 0700 /Library/Managed\ Installs/certs`
    1. `sudo mv ~/Desktop/munki_client.pem /Library/Managed\ Installs/certs/munki_client.pem`
    1. `sudo chmod 0600 /Library/Managed\ Installs/certs/munki_client.pem`
    1. `sudo chown -R root:wheel /Library/Managed\ Installs/certs`
1. Edit the ManagedInstalls.plist
    1. Open the preferences file in your editor of choice
        - If you do not already have a Munki preferences file see [configuration] for details.
    1. Edit the `ManifestURL` key to contain the URL for your server host
        - ie. https://your.server.com/repo/manifests
    1. Remove the value from the `ClientIdentifier` key
        - This key should be left *blank*
    1. Edit the `SoftwareRepoURL` key to contain the repo URL for your host
        - ie. https://your.server.com/repo
    1. Edit the boolean `UseClientCertificate` key so that is is *true*
        - Configuration of the client is complete.
        - Do not close Terminal.app.
	
With the Munki preferences file configured and the certificate/key combo file securely installed, we should no be able to access the secure repo.
				
- Test the Setup
		
1. `sudo /usr/local/munki/managedsoftwareupdate -v -v -v --checkonly`
    - Expected result? Your Munki client should be able to download its manifest from the secure repo.

### Troubleshooting

This documentation is only meant to provide a jumping off point for setting up an Apache/SSL config -- it is not exhaustive. Since it was written, much of the munki code has changed. The addition of curl now provides support for a fully implemented SSL setup and it works very well. I think the wiki page still provides a good overview of what is involved in getting the setup you are looking for (ie. The creation of a CA, Certs, etc.) but it cannot be expected to work out-of-thebox in every environment. The key to getting a functional secure setup is understanding the mechanics of an Apache/SSL configuration and being able to troubleshoot it.
 

*If you are having trouble using the virtual host config file provided in the demo materials (**many people have**), try creating your own basic secure setup using Mac OS X Server Admin. I would advise first getting your feet wet by simply getting communications between server and client using SSL, and not worrying about client certs.*

If you have correctly used the scripts in the demo materials to generate a CA and server certificate, you can use these in a stock Mac OS X Server setup. 

- At the Server...

1. Use Server Admin to import the server certificate and corresponding private key
1. Use Server Admin to create a new virtual host (Server Admin calls this a "Site")
1. Configure the new virtual host to use this key pair to encrypt the service
    - "Enable Secure Sockets Layer (SSL)"
1. Turn the service on
1. Open Safari so we can test the new virtual host
1. Enter the URL for your secure Apache host
    - Safari should prompt you about verifying the identity of the website; this is because the CA you created that signed the server's cert is not trusted.
    - This is OK and proves that the server's cert is active and the service is working
1. Close Safari
    - You now have a secure virtual host
1. Stop the Web service
1. Adjust the "Web Folder" path on your virtual host to point to your munki repo
    - Ensure you have the root correct
    - Make sure you save
1. Start the Web service
1. Use Safari and the enter the URL to your secure virtual host and test that you can access some of the munki repo resources.
    - If you can retrieve any of the manifests or catalogs, you are in business.

- At the Client...

1. Edit ManagedInstalls.plist and change the URLs for your ManifestURL and SoftwareRepoURL so that they specify "https://"
1. Now try running: sudo managedsoftwareupdate -vvv --checkonly
    - managedsoftwareupdate should complain
    - "ERROR: Error 60: SSL certificate problem, verify that the CA cert is OK. Details:"
    - this happens because the server cert's CA is not trusted; the same thing that happened with Safari
1. To correct this you can do one of two things:
    1. Import the CA certificate into the System.keychain 
    1. Add a SoftwareRepoCACertificate key to the ManagedInstalls.plist 
         I would advise solution B.
1. Solution B:
    - cd /Library/Managed\ Installs
    - sudo mkdir certs
    - sudo scp user@yourserver:/path_to_your_demoCA/demoCA/cacert.pem ./certs/cacert.pem
    - sudo defaults write /Library/Preferences/ManagedInstalls SoftwareRepoCACertificate "/Library/Managed Installs/certs/cacert.pem"
1. Try running: sudo managedsoftwareupdate -vvv --checkonly
    - This time it should work!

If you can get this far, you have one part of the setup done and using client certs is just around the corner. 

Hope this helps, 

-- Brian 

##### Fix for newer http(s) servers

_(fix by Francis Augusto Medeiros-Logeay)_

Some of newer https servers (we tested with Apache 2.4.x) require stronger certificate keys in order to work. Using the key/certificates generated by the use of the above instructions got us the following errors in Apache:

```
[Fri Oct 30 19:22:42.480679 2020] [ssl:error] [pid 2531017:tid 139839605290752] [client 129.240.203.197:54770] AH02039: Certificate Verification: Error (66): EE certificate key too weak
```

The fix that worked for us was to modify two things in some of the files provided here:

- In the file `config/openssl.cnf`, search for `default_bits` under the `[req]` section. Change its value from `1024` to `4096` (I suppose `2098` might work as well, here and below).
- In the file `bin/addClient.sh`, search for `1024` and replace it by `4096`.

Additionally, if you also use the `addServer.sh` script, search and replace `1024` by `4096`.

With that, Apache 2.4.x is happy and we can use our CA and client certificates again. 

### = Under Construction =

### References

http://www.modssl.org/docs/2.8/ssl_howto.html#auth-simple

http://httpd.apache.org/docs/2.0/

http://www.securityfocus.com/infocus/1823

http://developer.apple.com/internet/serverside/modssl.html

http://onlamp.com/onlamp/2008/03/04/step-by-step-configuring-ssl-under-apache.html

http://it.toolbox.com/blogs/securitymonkey/howto-securing-a-website-with-client-ssl-certificates-11500

http://www.afp548.com/articles/system/ldap-ssl.html

http://code.activestate.com/recipes/117004/

http://www.osmonov.com/2009/04/client-certificates-with-urllib2.html

http://www.threepillarsoftware.com/soap_client_auth

http://bugs.python.org/issue3466