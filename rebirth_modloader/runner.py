from subprocess import call
from sys import argv

def runGame():
    call(' '.join(argv[1:]))
