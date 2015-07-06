from zipfile import ZipFile
from unrar.rarfile import RarFile
from shutil import rmtree
from glob import glob
import os

from crosscompat import SLASH, RESPATH, WINDOWS

basefiles = [
    'achievements.xml',
    'ambush.xml',
    'babies.xml',
    'backdrops.xml',
    'bosscolors.xml',
    'bossportraits.xml',
    'challenges.xml',
    'costumes.xml',
    'cutscenes.xml',
    'entities2.xml',
    'fortunes.txt',
    'fxlayers.xml',
    'giantbook.xml',
    'itempools.xml',
    'items.xml',
    'music.xml',
    'nightmares.xml',
    'players.xml',
    'pocketitems.xml',
    'preload.xml',
    'rules.txt',
    'seeds.txt',
    'sounds.xml',
    'stages.xml',
    'font',
    'gfx',
    'music',
    'rooms',
    'sfx',
    'gfx'
]

class Loader:

    def __init__(self, path):
        if '.zip' in path:
            self.xfile = ZipFile(path)
        else: # Always going to be .rar -- see filelist.getMods
            self.xfile = RarFile(path)
        self.archiveformat = ''

    def howMany(self):
        return len(self.xfile.namelist())

    def checkSafe(self, name):
        if name[0] != '/' and not '..' in name:
            return True
        else:
            return False

    def getType(self):
        for basename in self.xfile.namelist():
            name = basename.replace('\\','/')
            if 'resources/' in name:
                self.archiveformat = 'resourcesdir'
                return
            else:
                split = name.split('/')
                for bfile in basefiles:
                    if bfile in split:
                        found = split.index(bfile)
                        if found == 0:
                            self.archiveformat = 'rootdir'
                            return
                        else:
                            self.archiveformat = 'nameddir'
                            self.dirname = split[found-1] + '/'
                            return
        self.archiveformat = 'notmod'

    def extract(self):
        for basename in self.xfile.namelist():
            name = basename.replace('\\','/')

            skip = False
            if self.archiveformat == 'resourcesdir' and 'resources/' in name:
                innerpath = name.split('resources/')[1]
            elif self.archiveformat == 'rootdir':
                innerpath = name
            elif self.archiveformat == 'nameddir' and self.dirname in name:
                innerpath = name.split(self.dirname)[1]
            elif self.archiveformat == 'notmod':
                print('Not a mod archive in a format I recognize.')
                return False
            else:
                skip = True

            if not self.checkSafe(name):
                print('"'+name+'" is considered to be unsafe.')
                skip = True

            if not skip:
                innerpath = innerpath.lower()
                joined = ( RESPATH + innerpath ).replace('\\','/')
                dirpath = '/'.join(joined.split('/')[:-1])

                if '.' in joined.split('/')[-1]:
                    isfile = True
                else:
                    isfile = False

                if WINDOWS:
                    for string in name, joined, dirpath:
                        string = string.replace('/','\\')

                print('Internal Path: '+name)
                print('Extraction Path: '+joined)

                if isfile:
                    if not os.path.exists(dirpath):
                        os.makedirs(dirpath)
                    if os.path.exists(joined):
                        print('Conflict at "' + joined + '"')

                    with open(joined, 'wb') as location:
                        location.write(self.xfile.read(basename))





    def load(self):
        if self.archiveformat == '':
            self.getType()
        self.extract()

class ModLoader:

    def prepMods(self):
        self.modfiles = []
        for path in self.mods:
            self.loaders.append(Loader(path))
        return self

    def __init__(self, mods):
        self.mods = mods
        self.loaders = []

    def howMany(self):
        accumulator = 0
        for loader in self.loaders:
            accumulator += loader.howMany()
        return accumulator

    def load(self):
        for loader in self.loaders:
            loader.load()
