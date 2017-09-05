import sys
from utils import clear
from utils import colors as c
from qprompt import *
from textwrap import TextWrapper
from shutil import get_terminal_size as gts


def display(num, results):
    clear()
    results[num - 1][1].display()

def displayNext(element):
    for el in element:
        if el.text:
            uprint('{}: {}'.format(el.tag.capitalize(),el.text))
        if el.getchildren() is not []:
            displayNext(el)

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)
