#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import fnmatch
import xml.etree.ElementTree as ET
from shutil import get_terminal_size
from textwrap import TextWrapper
import re
from functools import partial

def clear():
    os_name = os.name
    if os_name == "posix": # if OS is unix based this should work
        os.system('clear')
    elif os_name == "nt": # if OS is windows
        os.system('cls')
    else:
        pass
        

def get_files():
    fileLoc = []
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fileLoc.append('/Users/Azure/Dropbox/DnD 5e/DnDAppFiles/Compendiums')
    fileLoc.append('/Users/Azure/Dropbox/DnD 5e/DnDAppFiles/Unearthed Arcana')
    fileLoc.append(dir_path + '/DnDAppFiles')

    # create a DndLibrary object from the list of directories
    return fileLoc
        

class colors:
    REVERSE = '\033[7m'
    UNDERLINE = '\033[4m'
    BOLD = '\033[1m'
    NORMAL = '\033[0m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    UNDERLINE = '\033[4m'
    TEST = '\x1b[0;30;47m'
    heading = '\x1b[0;37;40m'

def format_input(input_str):
    answer = input_str
    
    return answer

# functions to find and decorate strings 
def decorate_factory(patt, pre, post):
    def _subber(m):
        return pre + m.group(0) + post
    return partial(re.compile(patt, re.IGNORECASE).sub, _subber)

roll_regex = '\d+[d]\d+'
decorate_dice_rolls = decorate_factory(roll_regex, colors.BOLD , colors.NORMAL)

attack_regex = '\+ *\d+ *\+?'
decorate_attack_rolls = decorate_factory(attack_regex, colors.BOLD , colors.NORMAL)

higher_levels_regex = 'at *higher *levels:?'
decorate_higher_levels = decorate_factory(higher_levels_regex, colors.UNDERLINE + colors.BOLD, colors.NORMAL)

skills_regex = '(strength|dexterity|constitution|intelligence|wisdom|charisma)\s*((saving\s*throw)|(check))?'
decorate_skills = decorate_factory(skills_regex, colors.BOLD, colors.NORMAL)

dc_regex = 'dc \d+'
decorate_DCs = decorate_factory(dc_regex, colors.BOLD, colors.NORMAL)

# override print function to include styles
def spell_decorator(func):
    def wrapped_func(*args,**kwargs):
        d = decorate_dice_rolls(*args,**kwargs)
        d = decorate_higher_levels(d)
        d = decorate_skills(d)
        d = decorate_DCs(d)
        return func(d)
    return wrapped_func

s_print = spell_decorator(print)

def monster_decorator(func):
    def wrapped_func(*args,**kwargs):
        d = decorate_dice_rolls(*args,**kwargs)
        d = decorate_attack_rolls(d)
        d = decorate_skills(d)
        d = decorate_DCs(d)
        return func(d)
    return wrapped_func

m_print = monster_decorator(print)
