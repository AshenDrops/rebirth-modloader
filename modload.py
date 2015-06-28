#!/bin/python

from sys import argv
from zipfile import ZipFile
from rarfile import RarFile
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
    if filetype == 'zip' or '7z':
       zipfile=ZipFile(zippath)
       if checkSafe(zipfile):
           betterExtract(zipfile, resources)
    elif filetype == 'rar':
        rarfile=RarFile(zippath)
        if checkSafe(rarfile):
            betterExtract(rarfile, resources)

def getResources():
    path=''
    if system() == 'Darwin':
        path=os.path.expanduser('~/Library/Application Support/Steam/SteamApps/common/The Binding of Isaac Rebirth/resources/')
    elif system() == 'Linux':
        path=os.path.expanduser('~/.steam/steam/steamapps/common/The Binding of Isaac Rebirth/resources/')
    elif system() == 'Windows':
        path='C:\\Program Files (x86)\\Steam\\SteamApps\\common\\The Binding of Isaac Rebirth\\resources\\'

    if os.path.exists(path):
        return path

def cleanup(resources):
    for directory in glob(resources+'*/'):
        if not 'packed' in directory and not 'mods' in directory:
            rmtree(directory)
    for xmlfile in glob(resources+'*.xml'):
        os.remove(xmlfile)

def betterExtract(zipfile, resources):
    for name in zipfile.namelist():
        print('Name: ' + name)
        if name.find('resources/') != -1 and name[-1] != '/':
            innerpath = name.split('resources/')[1].lower()
            print('innerpath: '+innerpath)
            print('resources: ' + resources)
            joined = resources + innerpath
            if not system() == 'Windows':
                dirpath = '/'.join(joined.split('/')[:-1])
            else:
                joined=joined.replace('/', '\\')
                dirpath = '\\'.join(joined.split('\\')[:-1])
            print('joined: ' + joined)
            print('dirpath: ' + dirpath)
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            if os.path.exists(joined):
                print('Mod incompatibility likely at \''+joined+'\'')
            with open(joined, 'wb') as wfile:
                wfile.write(zipfile.read(name))

def loadMods(resources):
    for archive in glob(resources+'mods/*'):
        if '.zip' in archive or '.rar' in archive or '.7z' in archive:
            safeExtract(archive, archive.split('.')[-1], resources)

def main():
    resources=getResources()
    loadMods(resources)
    call(argv[1])
    cleanup(resources)

# Testing crap
# cleanup(getResources())
# betterExtract(ZipFile('/home/ashlynn/gayhearts.zip'), getResources())
# betterExtract(ZipFile('/home/ashlynn/Downloads/splatoonedenhairstyles_1.0.zip'), getResources())
# betterExtract(ZipFile('/home/ashlynn/Downloads/fate--lapislazuli_1.0.zip'), getResources())
# loadMods(getResources())
main()
