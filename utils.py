#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import fnmatch
import xml.etree.ElementTree as ET
from shutil import get_terminal_size
from textwrap import TextWrapper
from classes import *

def clear():
    os_name = os.name
    if os_name == "posix": # if OS is unix based this should work
        os.system('clear')
    elif os_name == "nt": # if OS is windows
        os.system('cls')
    else:
        pass
        

def setup():
    fileLoc = []
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fileLoc.append('/Users/Azure/Dropbox/DnD 5e/DnDAppFiles/Compendiums')
    fileLoc.append('/Users/Azure/Dropbox/DnD 5e/DnDAppFiles/Unearthed Arcana')
    fileLoc.append(dir_path + '/DnDAppFiles')

    # create a DndLibrary object from the list of directories
    return DndLibrary(fileLoc)


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    TEST = '\x1b[0;30;47m'
    heading = '\x1b[0;37;40m'

size = get_terminal_size()
wrapper = TextWrapper(width=size.columns)
