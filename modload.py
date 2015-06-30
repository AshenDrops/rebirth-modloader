#!/bin/python3

from sys import argv
from zipfile import ZipFile
from unrar.rarfile import RarFile
from platform import system
from subprocess import call
from glob import glob
from shutil import rmtree
import os

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
    # elif filetype == '7z':
    #     lzmafile=Archive7z(open(zippath))
    #     if checkSafe(lzmafile):
    #         betterExtract(lzmafile, resources)
    else:
        rarfile=RarFile(zippath)
        if checkSafe(rarfile):
            betterExtract(rarfile, resources)

def getLaunchCodes():
    gamelaunch = 'steam://rungameid/250900'
    if system() == 'Darwin':
        path='idk'
    elif system() == 'Linux':
        path='/usr/bin/steam'
    elif system() == 'Windows':
        path='idk'

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

def cleanup(resources):
    print('Cleaning Up')
    for directory in glob(resources+'*/'):
        if not 'packed' in directory and not 'mods' in directory:
            print('Removed: ' + directory)
            rmtree(directory)
    for xmlfile in glob(resources+'*.xml'):
        os.remove(xmlfile)
        print('Removed: ' + xmlfile)

# def mergePlayers(file1, file2):


# def tryMerge(filename, file1, file2):
#     if filename == 'players.xml':
#         mergePlayers(file1, file2)


def betterExtract(zipfile, resources):
    for basename in zipfile.namelist():
        name = basename.replace('\\','/')
        print('Name: ' + name)
        shouldContinue = True
        if name.find('resources/') != -1 and name[-1] != '/':
            innerpath = name.split('resources/')[1].lower()
            joined = resources + innerpath
            if not system() == 'Windows':
                dirpath = '/'.join(joined.split('/')[:-1])
            else:
                joined=joined.replace('/', '\\')
                dirpath = '\\'.join(joined.split('\\')[:-1])
            if name.split('/')[-1].find('.') != -1:
                if not os.path.exists(dirpath):
                    os.makedirs(dirpath)
                if os.path.exists(joined):
                    print('Mod incompatibility likely at \''+joined+'\'')
                    # tryMerge
                with open(joined, 'wb') as wfile:
                    wfile.write(zipfile.read(basename))
                    print('Loaded: ' + joined)
            else:
                if not os.path.exists(joined):
                    os.makedirs(joined)

def loadMods(resources):
    for archive in glob(resources+'mods/*'):
        if '.zip' in archive or '.rar' in archive:
            safeExtract(archive, archive.split('.')[-1], resources)

def main():
    resources=getResources()
    if argv[1] != 'cleanup':
        loadMods(resources)
        call(' '.join(argv[1:]))
    cleanup(resources)

main()
