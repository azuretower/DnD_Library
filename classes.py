import os
import fnmatch
import xml.etree.ElementTree as ET
import qprompt
from utils import *

# cprint('look at me', colors.WARNING)

class DndLibrary:
    def __init__(self, directories):
        roots = []
        matches = []
        # find all the .xml files in the directories in fileLoc
        for loc in directories:
            for root, dirnames, filenames in os.walk(loc):
                for filename in fnmatch.filter(filenames, '*.xml'):
                    matches.append(os.path.join(root, filename))

        # open each file and parse the xml
        for x, file in enumerate(matches):
            if "Full Compendium" not in file:
                print(file)
                tree = ET.parse(file)
                root = tree.getroot()
                roots.append(root)


        # make each xml entry into an object
        monsters = []
        objects = []
        for root in roots:
            for x in root:
                if x.tag.lower() == 'monster':
                    mon = Monster(x)
                    # print(mon.name + " " + mon.readable_size + " " + str(len(mon.traits)))
                    monsters.append(mon)
                    objects.append((x[0].text,x,mon))
                else:
                    objects.append((x[0].text,x))

        self._list = objects
        self._old_term = ""
        self._results = []
        self._state = 0

    def search(self, keyword):
        found = []
        self._old_term = keyword
        for x in self._list:
            if keyword.lower() in x[0].lower():
                found.append((x))
        self._results = found

        if len(self._results) is 0:
            print("No Results Found")
            self._state = 0
        elif len(self._results) is 1:
            self._state = 2
        else:
            self._state = 1

    @property
    def show_results(self):
        for num, x in enumerate(self._results):
            print(x[0])

    def show_menu(self):
        menu = qprompt.Menu()
        for num, x in enumerate(self._results):
            menu.add(str(num + 1), x[0])
        menu.add('s', 'Return to search bar')
        choice = menu.show(header='==Results==')
        return choice

    @property
    def get_results(self):
        return self._results

    @property
    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    def clear_results(self):
        self._results = []
        

class Ability:
    def __init__(self, e):
        self.type = e.tag
        self.name = e.find('name').text
        self.attack = e.find('attack').text if e.find('attack') != None else "none"
        self.description = ''
        lines = e.findall('text')
        for line in lines:
            if line.text != None:
                self.description += line.text + "\n"


class Monster:
    def __init__(self, e):
        self.name = e.find('name').text
        self.size = e.find('size').text
        self.type = e.find('type').text
        self.alignment = e.find('alignment').text
        self.ac = e.find('ac').text
        self.hp = e.find('hp').text
        self.speed = e.find('speed').text
        self.strength = e.find('str').text
        self.dexterity = e.find('dex').text
        self.constitution = e.find('con').text
        self.intelligence = e.find('int').text
        self.wisdom = e.find('wis').text
        self.charisma = e.find('cha').text
        self.saves = e.find('save').text if e.find('save') != None else 'none'
        self.skills = e.find('skill').text if e.find('skill') != None else 'none'
        self.resistances = e.find('resistance').text if e.find('resistance') != None else 'none'
        self.passive_perception = e.find('passive').text if e.find('passive') != None else 'none'
        self.languages = e.find('languages').text if e.find('languages') != None else 'none'
        self.cr = e.find('cr').text
        self.spells = e.find('spells').text if e.find('spells') != None else 'none'

        self.traits = []
        traits_list = e.findall('trait')
        for trait in traits_list:
            self.traits.append(Ability(trait))

    @property
    def readable_size(self):
        if self.size.lower() == 't':
            return "Tiny"
        elif self.size.lower() == 's':
            return "Small"
        elif self.size.lower() == 'm':
            return "Medium"
        elif self.size.lower() == 'l':
            return "Large"
        elif self.size.lower() == 'h':
            return "Huge"
        elif self.size.lower() == 'g':
            return "Gargantuan"

    @property
    def stats(self):
        def find_mod(score):
            modifier = int((int(score) - 10) / 2)
            if modifier >= 0:
                modifier_str = str(f"+{modifier}")
            else:
                modifier_str =  str(f"{modifier}")
            return modifier_str

        def spacing(mod_string):
            spaces = ""
            if len(mod_string) == 6:
                spaces = " "
            elif len(mod_string) == 7:
                spaces = "  "
            else:
                spaces = "   "

            return spaces

        str_mod = "{} ({})".format(self.strength, find_mod(self.strength))
        dex_mod = "{} ({})".format(self.dexterity, find_mod(self.dexterity))
        con_mod = "{} ({})".format(self.constitution, find_mod(self.constitution))
        int_mod = "{} ({})".format(self.intelligence, find_mod(self.intelligence))
        wis_mod = "{} ({})".format(self.wisdom, find_mod(self.wisdom))
        cha_mod = "{} ({})".format(self.charisma, find_mod(self.charisma))
        stat_string = "|   STR {}|   DEX {}|   CON {}|   INT {}|   WIS {}|   CHA {}|\n".format(
                      spacing(str_mod), spacing(dex_mod), spacing(con_mod), 
                      spacing(int_mod), spacing(wis_mod), spacing(cha_mod))
        stat_string2 = f"| {str_mod} | {dex_mod} | {con_mod} | {int_mod} | {wis_mod} | {cha_mod} |"

        return stat_string + stat_string2

    def display(self):
        print(self.name)
        print(self.readable_size + " " + self.type.split(',')[0] + " | " + self.alignment)
        print(f"AC: {self.ac}")
        print(f"HP: {self.hp}")
        print(f"Speed: {self.speed}")
        print(self.stats)
        if self.saves != 'none':
            print(self.saves)
        if self.skills != 'none':
            print(self.skills)
        if self.resistances != 'none':
            print(self.resistances)
        print(f"Passive Perception {self.passive_perception}")
        print(self.languages)
        print(f"Challenge: {self.cr}")
        if self.spells != 'none':
            print(self.spells)