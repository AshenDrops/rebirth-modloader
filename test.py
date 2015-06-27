from zipfile import ZipFile
from rarfile import RarFile
from platform import system
from subprocess import call
from glob import glob
import os

# Make sure nothing explodes
def safeExtract(zippath, filetype):
    # Make sure file is safe to extact (no starting with / or having ".." in the filenames)
    def checkSafe(zipfile):
        for name in mod.namelist():
            if not name[0] == '/' and name.find('..') == -1:
                return True
    
    # Ugly switch
    if filetype == 'zip' or '7z':
       zipfile=ZipFile(zippath)
       if checkSafe(zipfile):
           zipfile.extractall()
    elif filetype == 'rar':
        rarfile=RarFile(zippath)
        if checkSafe(rarfile):
            rarfile.extractall()

def getResources():
    if system() == 'Darwin':
        return os.path.expanduser('~/Library/Application Support/Steam/SteamApps/common/The Binding of Isaac Rebirth/resources')
    elif system() == 'Linux':
        return os.path.expanduser('~/.steam/steam/steamapps/common/The Binding of Isaac Rebirth/resources')
    elif system() == 'Windows':
        return 'C:\Program Files (x86)\Steam\steamapps\common\The Binding of Isaac Rebirth\resources'

def cleanup(resources):
    os.chdir(path=resources)
    for directory in glob('*/'):
        print(directory)

cleanup(getResources())
