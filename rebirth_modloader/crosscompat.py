from platform import system
from os.path import expanduser, exists
from os import environ

WINDOWS = False
if system() == 'Linux':
    SLASH = '/'
    RESPATH = expanduser('~/.steam/steam/steamapps/common/The Binding of Isaac Rebirth/resources/')
    if 'XDG_DATA_HOME' in environ:
        CONFIGPATH = environ['XDG_DATA_HOME']
    else:
        CONFIGPATH = expanduser('~/.local/share/')
elif system() == 'Darwin':
    SLASH = '/'
    RESPATH = expanduser('~/Library/Application Support/Steam/SteamApps/common/The Binding of Isaac Rebirth/The Binding of Isaac Rebirth.app/Contents/Resources/resources/')
    CONFIGPATH = expanduser('~/Library/Application Support/')
elif system() == 'Windows':
    SLASH = '\\'
    RESPATH = 'C:\\Program Files (x86)\\Steam\\SteamApps\\common\\The Binding of Isaac Rebirth\\resources\\'
    CONFIGPATH = 'C:\\Program Files (x86)\\'
    WINDOWS = True
else:
    print('Not a recognized system. Quitting to avoid errors.')
    exit()

