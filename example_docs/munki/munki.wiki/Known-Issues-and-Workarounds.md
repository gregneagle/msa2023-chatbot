#### A collection of known issues and workarounds

##### Managed Software Center cosmetic issues under Yosemite

Managed Software Center has some cosmetic display issues in the toolbar under Yosemite. Some elements will sometimes draw without a background, and the available update count badge when displayed sometimes causes the Updates icon to be drawn scaled-down. See https://github.com/munki/munki/issues/378

##### curl, client certificates and Mavericks+

Starting with OS X Mavericks, the Apple-supplied curl uses Apple's SecureTransport instead of OpenSSL for its support of server and client certificates. See: https://www.afp548.com/2013/11/18/coping-with-curl-on-mavericks/

These issues affect Munki versions prior to 2.1. In Munki 2.1, the reliance on curl was removed.