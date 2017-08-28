#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import sys, os, os.path
import string
from shutil import get_terminal_size as gts
from colorama import init

from utils import clear, get_files
from displays import *
from qprompt import *
from classes import DndLibrary

# sets up color support for windows
init()

clear()

# create a DndLibrary object from the list of directories

Library = DndLibrary(get_files())
           
try:
    run = True
    while run:
        if Library.get_state == 0:
            hrule(width=gts().columns, char="~")
            response = ask_str("What keyword are you looking for?")
            if response == ":quit":
                run = False
                continue
            Library.search(response)
        elif Library.get_state == 1:
            hrule(width=gts().columns, char="~")
            response = Library.show_menu()
            if response == 's':
                Library.set_state(0)
            else:
                display(int(response), Library.get_results)
                Library.set_state(0)
        elif Library.get_state == 2:
            hrule(width=gts().columns, char="~")
            display(1, Library.get_results)
            Library.set_state(0)

except KeyboardInterrupt:
    clear()
    print('Bye Bye!')
useless = False
this should cause a conflit