# rebirth-modloader
A Binding Of Isaac: Rebirth modloader

#Installation:  
* Download modload.py
* Place modload.py in your "The Binding of Isaac" directory.
  * Windows: `C:\Program Files (x86)\Steam\SteamApps\common\The Binding of Isaac Rebirth\resources`
  * OS X: `<user>/Library/Application Support/Steam/SteamApps/common/The Binding of Isaac Rebirth/The Binding of Isaac Rebirth.app/Contents/Resources/resources`
    * You will have to right click `The Binding of Isaac Rebirth.app` and click `View Package Contents`
  * Linux: `~/.steam/steam/steamapps/common/The Binding of Isaac Rebirth/resources`
* Create `mods` folder inside `resources` folder
* Add any mod zip/rar files you want to it
  * You can create a shortcut/alias on your desktop for easy access by
    * Windows: Right click > Send to > Desktop (create shortcut)
    * OS X: Right click > Make Alias, then drag the alias to your desktop
    * Linux: Depends, but in terminal you can do it with `ln mods ~/Desktop/mods`
* Open Steam, then right click "The Binding of Isaac: Rebirth" and click "Properties", then "Set Launch Options" and set it to
  * Windows: `"C:\Program Files (x86)\Steam\SteamApps\common\The Binding of Isaac Rebirth\resources\modload.py" %command%`
  * OS X: `<user>/Library/Application\ Support/Steam/SteamApps/common/The\ Binding\ of\ Isaac\ Rebirth/The\ Binding\ of\ Isaac\ Rebirth.app/Contents/Resources/resources/modload.py %command%`
  * Linux: `~/.steam/steam/steamapps/common/The\ Binding\ of\ Isaac\ Rebirth/resources/modload.py %command%`
* Launch Rebirth and enjoy! You can swap the mods in the folder out at any time.
