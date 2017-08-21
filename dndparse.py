#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import sys, os, os.path
import string
from shutil import get_terminal_size as gts

from utils import *
from classes import *
from displays import *
from qprompt import *


clear()

# create a Dndeck object from the list of directories
deck = setup()
           
try:
    run = True
    while run:
        if deck.get_state == 0:
            hrule(width=gts().columns, char="~")
            response = ask_str("What keyword are you looking for?")
            if response == "quit":
                run = False
                continue
            deck.search(response)
        elif deck.get_state == 1:
            hrule(width=gts().columns, char="~")
            response = deck.show_menu()
            if response == 's':
                deck.set_state(0)
            else:
                display(int(response), deck.get_results)
                deck.set_state(0)
        elif deck.get_state == 2:
            hrule(width=gts().columns, char="~")
            display(1, deck.get_results)
            deck.set_state(0)

except KeyboardInterrupt:
    clear()
    print('Bye Bye!')