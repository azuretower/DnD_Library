import sys
from utils import clear, cprint
from utils import colors as c
from qprompt import *
from textwrap import TextWrapper
from shutil import get_terminal_size as gts

#implement wrap in the future https://docs.python.org/2/library/textwrap.html


def display(num, results):
    clear()
    result = results[num - 1][1]
    if result.tag == 'monster':
        displayMonster(result)
        # results[num - 1][2].display()
    else:
        displayNext(result)

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

def displayMonster(element):
    hrule(width=gts().columns, char="#")
    element_list = []
    for el in element:
        element_list.append((el.tag,el))

    stat_list = ['str', 'dex', 'con', 'int', 'wis']
    for el in element_list:
        if el[0] == 'size':
            if el[1].text.lower() == 's':
                print('{}: {} |'.format(el[0].capitalize(),"Small"), end=' ')
            elif el[1].text.lower() == 'm':
                print('{}: {} |'.format(el[0].capitalize(),"Medium"), end=' ')
            elif el[1].text.lower() == 'l':
                print('{}: {} |'.format(el[0].capitalize(),"Large"), end=' ')
            elif el[1].text.lower() == 'h':
                print('{}: {} |'.format(el[0].capitalize(),"Huge"), end=' ')
            elif el[1].text.lower() == 'g':
                print('{}: {} |'.format(el[0].capitalize(),"Gargantuan"), end=' ')

        elif el[0] in stat_list or el[0] == 'ac' or el[0] == 'hp':
            print('{}: {} |'.format(el[0].capitalize(),el[1].text), end=' ')

        elif el[0] == 'trait' or el[0] == 'action' or el[0] == 'legendary':
            pass

        else:
            print('{}: {}'.format(el[0].capitalize(),el[1].text))

    # findall trait, action, lengedary and print them
    traits = element.findall('trait')
    if traits:
        print(c.heading + "==========Traits==========" + c.ENDC)
        for trait in traits:
            name = trait.find('name')
            descriptions = trait.findall('text')
            print('  {} {}'.format('-',name.text.capitalize()))
            for description in descriptions:
                if description.text != None:
                    print('    {}{}\n'.format('',description.text))

    actions = element.findall('action')
    if actions:
        print("==========Actions==========")
        for action in actions:
            attack = action.find('attack')
            descriptions = action.findall('text')
            name = action.find('name')
            if attack != None:
                print('  {} {}'.format('-',attack.text.capitalize()))
                for description in descriptions:
                    if description.text != None:
                        print('    {}{}\n'.format('',description.text))
            else:
                print('  {} {}'.format('-',name.text.capitalize()))
                for description in descriptions:
                    if description.text != None:
                        print('    {}{}\n'.format('',description.text))

    legendary_actions = element.findall('legendary')
    if legendary_actions:
        print("==========Legendary Actions==========")
        for action in legendary_actions:
            attack = action.find('attack')
            descriptions = action.findall('text')
            name = action.find('name')
            if attack:
                print('  {} {}'.format('-',attack.text.capitalize()))
                for description in descriptions:
                    if description.text != None:
                        print('    {}{}\n'.format('',description.text))
            else:
                print('  {} {}'.format('-',name.text.capitalize()))
                for description in descriptions:
                    if description.text != None:
                        print('    {}{}\n'.format('',description.text))
