#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import sys, os, os.path
import string
from shutil import get_terminal_size

from utils import *
from classes import *
from displays import *
from prompt import *

size = get_terminal_size()
term_width = size.columns


clear()

# set up variables
# fileLoc = []
# dir_path = os.path.dirname(os.path.realpath(__file__))
# fileLoc.append('/Users/Azure/Dropbox/D&D 5e/DnDAppFiles/Compendiums')
# fileLoc.append(dir_path + '/PersonalDnDAppFiles')

# # create a Dndeck object from the list of directories
# deck = Dndeck(fileLoc)
deck = setup()
           
try:
    run = True
    while run:
        if deck.get_state == 0:
            hrule(char="~")
            response = cinput("What keyword are you looking for? ", colors.TEST)
            if response == "quit":
                run = False
                continue
            deck.search(response)
        elif deck.get_state == 1:
            hrule(char="~")
            response = deck.show_menu()
            if response == 's':
                deck.set_state(0)
            else:
                display(int(response), deck.get_results)
                deck.set_state(0)
        elif deck.get_state == 2:
            hrule(char="~")
            display(1, deck.get_results)
            deck.set_state(0)

except KeyboardInterrupt:
    clear()
    print('Bye Bye!')