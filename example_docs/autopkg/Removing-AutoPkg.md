1. Unload and remove the autopkg Launch Daemons:
```bash
  sudo launchctl unload /Library/LaunchDaemons/com.github.autopkg.autopkginstalld.plist
  sudo launchctl unload /Library/LaunchDaemons/com.github.autopkg.autopkgserver.plist
  sudo rm /Library/LaunchDaemons/com.github.autopkg.autopkg*
```
2. Remove symlinks in /usr/local
```bash
  sudo rm -r /usr/local/autopkg
  sudo rm /usr/local/bin/autopkg
```
3. Remove the /Library/AutoPkg folder
```bash
  sudo rm -r /Library/AutoPkg
```
4. Forget the autopkg installation receipt:
```bash
  sudo pkgutil --forget com.github.autopkg.autopkg
```
5. (Optional) remove all recipes and overrides:
```bash
  rm -r ~/Library/AutoPkg
```