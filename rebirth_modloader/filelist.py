from glob import glob

from crosscompat import SLASH, CONFIGPATH

def getMods():
    mods = []
    globber = CONFIGPATH+'rebirth_modloader'+SLASH+'mods'+SLASH+'*'
    print(globber)
    for archive in glob(globber):
        if '.zip' in archive or '.rar' in archive:
            mods.append(archive)
    return mods
