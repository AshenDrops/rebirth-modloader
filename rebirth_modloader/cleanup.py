from glob import glob
from shutil import rmtree
from os import remove

from crosscompat import RESPATH

def clean():
    resources = RESPATH.replace('\\','/')
    for directory in glob(resources+'*'+'/'):
        if not 'packed/' in directory:
            print('Removing: '+directory)
            rmtree(directory)
    for xmlfile in glob(resources+'*.xml'):
        print('Removing: '+xmlfile)
        remove(xmlfile)
    for animations_b in glob(resources+'*.b'):
        print('Removing: '+animations_b)
        remove(animations_b)
