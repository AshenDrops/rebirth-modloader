from subprocess import call
from sys import argv

def runGame():
    if(argv[1] != 'ssr-glinject'):
        call(' '.join(argv[1:]))
    else:
        call(['ssr-glinject',' '.join(argv[2:])])
