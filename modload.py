#!/bin/python2

from sys import argv
from zipfile import ZipFile
from unrar.rarfile import RarFile
from platform import system
from subprocess import call
from glob import glob
from shutil import rmtree
import os

from filelist import ModSwapper

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

# Make sure nothing explodes
def safeExtract(zippath, filetype, resources):
    # Make sure file is safe to extact (no starting with / or having ".." in the filenames)
    def checkSafe(zipfile):
        for name in zipfile.namelist():
            if not name[0] == '/' and name.find('..') == -1:
                return True

    # Ugly switch
    if filetype == 'zip':
        zipfile=ZipFile(zippath)
        if checkSafe(zipfile):
            betterExtract(zipfile, resources)
    else:
        rarfile=RarFile(zippath)
        if checkSafe(rarfile):
            betterExtract(rarfile, resources)

# Probably 90% wrong
def getResources():
    path=''
    if system() == 'Darwin':
        path=os.path.expanduser('~/Library/Application Support/Steam/SteamApps/common/The Binding of Isaac Rebirth/The Binding of Isaac Rebirth.app/Contents/Resources/resources/')
    elif system() == 'Linux':
        path=os.path.expanduser('~/.steam/steam/steamapps/common/The Binding of Isaac Rebirth/resources/')
    elif system() == 'Windows':
        path='C:\\Program Files (x86)\\Steam\\SteamApps\\common\\The Binding of Isaac Rebirth\\resources\\'

    if os.path.exists(path):
        return path

# Removes every folder (besides packed and mods) and evert xml file in the resources directory
def cleanup(resources):
    print('Cleaning Up')
    for directory in glob(resources+'*/'):
        if not 'packed' in directory and not 'mods' in directory:
            print('Removed: ' + directory)
            rmtree(directory)
    for xmlfile in glob(resources+'*.xml'):
        os.remove(xmlfile)
        print('Removed: ' + xmlfile)

# Preliminary merging code. Probably should move this to another file
# def mergePlayers(file1, file2):


# def tryMerge(filename, file1, file2):
#     if filename == 'players.xml':
#         mergePlayers(file1, file2)

# Check to see if any of the files have resources in their path or if they're meant to be placed directly in resources
def spCheck(zipfile):
    retVal = True
    for basename in zipfile.namelist():
        name = basename.replace('\\','/')
        if 'resources/' in name:
            retVal = False
    return retVal

def checkBaseDir(zipfile):
    for basename in zipfile.namelist():
        name = basename.replace('\\','/')
        if 'resources/' in name:
            return ('', False)
        split = name.split('/')
        for filename in basefiles:
            if filename in split:
                index = split.index(filename)
                if index != -1 and index != 0:
                    return (split[index-1] + '/', True)
    return ('', False)

# This code is a mess. I should probably fix it but I'm not even sure where to start
def betterExtract(zipfile, resources):
    for basename in zipfile.namelist():
        name = basename.replace('\\','/')
        print('Name: ' + name)

        # Handling for if root dir is resources
        spContinue = spCheck(zipfile)

        # Handling for if differently named dir is resources
        basedir, basedirExists = checkBaseDir(zipfile)
        if basedirExists:
            spContinue = False

        if name[-1] != '/' and ( spContinue or name.find('resources/') != -1 or ( name.find(basedir) != -1 and basedirExists) ):
            # lowercases everything
            innerpath = name.lower()

            # splits path on resources or differently named resources
            if name.find('resources/') != -1:
                innerpath = name.split('resources/')[1].lower()
            elif name.find(basedir) != -1 and basedirExists:
                innerpath = name.split(basedir)[1].lower()

            joined = resources + innerpath

            # Converts / to \ on Windows and gets "dirpath" for dir creation if necessary
            if not system() == 'Windows':
                dirpath = '/'.join(joined.split('/')[:-1])
            else:
                joined=joined.replace('/', '\\')
                dirpath = '\\'.join(joined.split('\\')[:-1])

            # If it's got a dot in it assume it's a file. Not really a good way to do this but eh
            if name.split('/')[-1].find('.') != -1:
                if not os.path.exists(dirpath):
                    os.makedirs(dirpath)
                if os.path.exists(joined):
                    print('Conflict')
                    # tryMerge
                print('Joined: ' + joined)
                with open(joined, 'wb') as wfile:
                    wfile.write(zipfile.read(basename))
            else:
                # Exception because sometimes directories don't have a / after them especially in rar files
                if not os.path.exists(joined):
                    os.makedirs(joined)

# Callback from GUI interface
def callback(arr):
    resources = getResources()
    for mod in arr:
        print(resources+'mods/'+mod)
        safeExtract(resources+'mods/'+mod, mod.split('.')[-1], resources)
    call(' '.join(argv[1:]))

# Loads up that gui goodness
def loadMods(resources):
    arr = []
    for archive in glob(resources+'mods/*'):
        if '.zip' in archive or '.rar' in archive:
            arr.append(archive.split('/')[-1])
    # Good idea. Make it so refreshing in the gui is impossible.
    ModSwapper('Asterne\'s Modloader', arr, callback).main()

# Main
def main():
    resources=getResources()
    if argv[1] != 'cleanup':
        loadMods(resources)
    cleanup(resources)

if __name__ == '__main__':
    main()
