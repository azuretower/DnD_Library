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

rows, columns = os.popen('stty size', 'r').read().split()


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
        if deck.state == 0:
            hrule(width=term_width, char="~")
            response = cinput("What keyword are you looking for? ", colors.TEST)
            # response = input(colors.TEST + "What keyword are you looking for? " + colors.ENDC + colors.UNDERLINE)
            # print(colors.ENDC)
            if response == "quit":
                run = False
                continue
            elif response == "reload":
                # global deck
                deck = setup()
            deck.search(response)
            # deck.show_results
        elif deck.state == 1:
            hrule(width=term_width, char="~")
            response = deck.show_menu()
            # response = cinput('Enter number of item or enter 0 to search again or X to see results again: ', colors.TEST)
            if response == 'X' or response == 'x':
                deck.search(old_response)
            elif response == '' or response in string.ascii_letters:
                deck.state = 0
            elif int(response) == 0:
                deck.state = 0
            else:
                display(int(response), deck.get_results)
                deck.state = 0
        elif deck.state == 2:
            hrule(width=term_width, char="~")
            display(1, deck.get_results)
            deck.state = 0

except KeyboardInterrupt:
    clear()
    print('Bye Bye!')