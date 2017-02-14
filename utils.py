#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import fnmatch
import xml.etree.ElementTree as ET
from shutil import get_terminal_size
from textwrap import TextWrapper
from classes import *

def clear():
    os.system('clear')

def setup():
    fileLoc = []
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fileLoc.append('/Users/Azure/Dropbox/D&D 5e/DnDAppFiles/Compendiums')
    fileLoc.append(dir_path + '/PersonalDnDAppFiles')

    # create a Dndeck object from the list of directories
    return Dndeck(fileLoc)


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

def cprint(text, color=colors.ENDC):
    print(wrapper.wrap(color + text + colors.ENDC))

def cinput(text, color=colors.ENDC):
    return input(color + text + colors.ENDC)

# def setup(directories):

#     roots = []
#     matches = []
#     # find all the .xml files in the directories in fileLoc
#     for loc in directories:
#         for root, dirnames, filenames in os.walk(loc):
#             for filename in fnmatch.filter(filenames, '*.xml'):
#                 matches.append(os.path.join(root, filename))

#     # open each file and parse the xml
#     for x, file in enumerate(matches):
#         if "Full Compendium" not in file:
#             print(file)
#             tree = ET.parse(file)
#             root = tree.getroot()
#             roots.append(root)


#     monsters = []
#     objects = []
#     for root in roots:
#         for x in root:
#             if x.tag.lower() == 'monster':
#                 temp = Monster(x)
#                 # print(temp.name + " " + temp.readable_size + " " + str(len(temp.traits)))
#                 monsters.append(Monster(x))
#             objects.append((x[0].text,x))
#     return objects