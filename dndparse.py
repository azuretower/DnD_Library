#!/usr/bin/env python3
import sys, os, os.path
import xml.etree.ElementTree as ET
from shutil import get_terminal_size as gts

from qprompt import *
from colorama import init

from utils import clear, get_files, format_input
from displays import *
from classes import DndLibrary

# sets up color support for windows
init()

clear()

# create a DndLibrary object from the list of directories

Library = DndLibrary(get_files())
Library.display_loaded_count()

try:
    run = True
    while run:
        if Library.get_state == 0:
            hrule(width=gts().columns, char="~")
            response = ask("What keyword are you looking for?", fmt=format_input, blk=True)
            if response.strip() in ':quit' and response.startswith(':'):
                run = False
                continue
            elif response.strip() in ':all' and response.startswith(':'):
                Library.reset_search_history
                Library.search('')
            elif response.strip() in ':reload' and response.startswith(':'):
                os.execv(__file__, sys.argv)
            elif response.strip() == ':roll' and response.startswith(':'):
                pass
            else:
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
