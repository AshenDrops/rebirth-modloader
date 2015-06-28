# rebirth-modloader
A Binding Of Isaac: Rebirth modloader

**Currently is not compatible with 7z files (or any files other than rar or zip for that matter)**

*Modloader requires Python. You can download it [here](https://www.python.org/downloads/). The version you download doesn't matter as modloader is compatible with both.*  
  * Make sure to check "Add Python <version> to PATH"
*Also requires rarfile -- I'm not 100% sure how you would install this on windows, but on OS X and Linux it's installed with `sudo pip install rarfile`*
  * On Windows if you checked "Add Python to PATH" the command `pip install rarfile` should work.

#Installation:  
* Download [modload.py](https://raw.githubusercontent.com/AshenDrops/rebirth-modloader/master/modload.py) (Right click > Save as)
* Place modload.py in your "resources" directory, found at
  * **Windows**: `C:\Program Files (x86)\Steam\SteamApps\common\The Binding of Isaac Rebirth\resources`
  * **OS X**: `<user>/Library/Application Support/Steam/SteamApps/common/The Binding of Isaac Rebirth/The Binding of Isaac Rebirth.app/Contents/Resources/resources`
    * You will have to right click "The Binding of Isaac Rebirth.app" and click "View Package Contents"
  * **Linux**: `~/.steam/steam/steamapps/common/The Binding of Isaac Rebirth/resources`
* Create "mods" folder inside "resources" folder
* Add any mod zip/rar files you want to it
  * You can create a shortcut/alias on your desktop for easy access by
    * **Windows**: Right click > Send to > Desktop (create shortcut)
    * **OS X**: Right click > Make Alias, then drag the alias to your desktop
    * **Linux**: Depends, but in terminal you can do it with `ln mods ~/Desktop/mods`
* Open Steam, then right click "The Binding of Isaac: Rebirth" and click "Properties", then "Set Launch Options" and set it to
  * **Windows**: `"C:\Program Files (x86)\Steam\SteamApps\common\The Binding of Isaac Rebirth\resources\modload.py" %command%`
  * **OS X**: `<user>/Library/Application\ Support/Steam/SteamApps/common/The\ Binding\ of\ Isaac\ Rebirth/The\ Binding\ of\ Isaac\ Rebirth.app/Contents/Resources/resources/modload.py %command%`
  * **Linux**: `~/.steam/steam/steamapps/common/The\ Binding\ of\ Isaac\ Rebirth/resources/modload.py %command%`
* Launch Rebirth and enjoy! You can swap the mods in the folder out at any time.
