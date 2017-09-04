import os
import re
import fnmatch
from textwrap import TextWrapper
import xml.etree.ElementTree as ET
from shutil import get_terminal_size as gts

import qprompt

from utils import colors, clear
from utils import s_print, m_print
from subclasses import Attribute
from displays import displayNext

c = colors
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
                roots.append((root,file))

        # make each xml entry into an object
        self.monsters = []
        self.items = []
        self.spells = []
        self.character_classes = []
        self.races = []
        self.feats = []
        self.backgrounds = []
        self.generic_entries = []
        objects = []
        for root in roots:
            for x in root[0]:
                if x.tag.lower() == 'monster':
                    self.monsters.append(Monster(x, file))
                elif x.tag.lower() == 'item':
                    self.items.append(Item(x, file))
                elif x.tag.lower() == 'spell':
                    self.spells.append(Spell(x, file))
                elif x.tag.lower() == 'class':
                    self.character_classes.append(CharacterClass(x, file))
                elif x.tag.lower() == 'race':
                    self.races.append(Race(x, file))
                elif x.tag.lower() == 'feat':
                    self.feats.append(Feat(x, file))
                elif x.tag.lower() == 'background':
                    self.backgrounds.append(Background(x, file))
                else:
                    self.generic_entries.append(GenericEntry(x, file))

        self.monsters.sort()
        self.items.sort()
        self.spells.sort()
        self.character_classes.sort()
        self.races.sort()
        self.feats.sort()
        self.backgrounds.sort()
        self.generic_entries.sort()

        objects.extend(map(lambda mon : (mon.name, mon), self.monsters))
        objects.extend(map(lambda item : (item.name, item), self.items))
        objects.extend(map(lambda spell : (spell.name, spell), self.spells))
        objects.extend(map(lambda char_class : (char_class.name, char_class), self.character_classes))
        objects.extend(map(lambda race : (race.name, race), self.races))
        objects.extend(map(lambda feat : (feat.name, feat), self.feats))
        objects.extend(map(lambda backg : (backg.name, backg), self.backgrounds))
        objects.extend(map(lambda gen : (gen.name, gen), self.generic_entries))

        self._list = objects
        self._old_term = ""
        self._results = []
        self._state = 0

    def display_loaded_count(self):
        print(f"Monsters Loaded: {len(self.monsters)}")
        print(f"Items Loaded: {len(self.items)}")
        print(f"Spells Loaded: {len(self.spells)}")
        print(f"Classes Loaded: {len(self.character_classes)}")
        print(f"Races Loaded: {len(self.races)}")
        print(f"Feats Loaded: {len(self.feats)}")
        print(f"Backgrounds Loaded: {len(self.backgrounds)}")
        print(f"Other Loaded: {len(self.generic_entries)}")

    def search(self, keyword):
        found = []
        if keyword == '':
            keyword = self._old_term
        else:
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
    def reset_search_history(self):
        self._old_term = ''

    @property
    def show_results(self):
        for num, x in enumerate(self._results):
            print(x[0])

    def _type_abbreviation(self, entry):
        entry_type = entry.element.tag.lower()
        short_type = ""
        if entry_type == 'monster':
            short_type = 'Mons'
        elif entry_type == 'item':
            short_type = 'Item'
        elif entry_type == 'spell':
            short_type = 'Spel'
        elif entry_type == 'class':
            short_type = 'Clas'
        elif entry_type == 'race':
            short_type = 'Race'
        elif entry_type == 'feat':
            short_type = 'Feat'
        elif entry_type == 'background':
            short_type = 'Back'
        else:
            short_type = entry_type

        return short_type

    def show_menu(self):
        clear()
        menu = qprompt.Menu()
        for num, x in enumerate(self._results):
            menu.add(str(num + 1), f"{self._type_abbreviation(x[1])} - {x[0]}")
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
        

class Attribute:
    """Attribute is only used with Monster class"""
    def __init__(self, e):
        self.type = e.tag
        self.name = e.find('name').text
        self.attack = e.find('attack').text if e.find('attack') != None else 'None'
        self.description = []
        lines = e.findall('text')
        for line in lines:
            if line.text != None:
                self.description.append(line.text)

    def display(self):
        wrapper = TextWrapper(width=gts().columns - 2, initial_indent="    ", subsequent_indent="    ")
        if self.attack != 'None':
            attack_split = self.attack.split("|")
            name_line = f"{self.name}"
            if attack_split[1].strip() != '':
                name_line += f" +{attack_split[1].strip()}"
            if attack_split[2].strip() != '':
                name_line += f" ({attack_split[2].strip()})"
        else:
            name_line = self.name
        description_lines = ""
        for line in self.description:
            description_lines += wrapper.fill(line) + "\n"

        m_print(f"- {name_line}")
        m_print(description_lines)


class Monster:
    """Monster initializes from a xml element 'e'"""
    def __init__(self, e, file=None):
        self.element = e
        self.origin_file = file
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
        self.saves = e.find('save').text if e.find('save') != None and e.find('save').text != None else 'None'
        self.skills = e.find('skill').text if e.find('skill') != None and e.find('skill').text != None else 'None'
        self.resistances = e.find('resist').text if e.find('resist') != None and e.find('resist').text != None else 'None'
        self.vulnerabilities = e.find('vulnerable').text if e.find('vulnerable') != None and e.find('vulnerable').text != None else 'None'
        self.damage_immunities = e.find('immune').text if e.find('immune') != None and e.find('immune').text != None else 'None'
        self.condition_immunites = e.find('conditionImmune').text if e.find('conditionImmune') != None and e.find('conditionImmune').text != None else 'None'
        self.senses = e.find('senses').text if e.find('senses') != None and e.find('senses').text != None else 'None'
        self.passive_perception = e.find('passive').text if e.find('passive') != None and e.find('passive').text != None else 'None'
        self.languages = e.find('languages').text if e.find('languages') != None and e.find('languages').text != None else 'None'
        self.cr = e.find('cr').text
        self.spells = e.find('spells').text if e.find('spells') != None and e.find('spells').text != None else 'None'

        self.traits = []
        traits_list = e.findall('trait')
        for trait in traits_list:
            self.traits.append(Attribute(trait))

        self.actions = []
        actions_list = e.findall('action')
        for action in actions_list:
            self.actions.append(Attribute(action))

        self.reactions = []
        reactions_list = e.findall('reaction')
        for reaction in reactions_list:
            self.reactions.append(Attribute(reaction))

        self.legendary_actions = []
        legendary_actions_list = e.findall('legendary')
        for legendary_action in legendary_actions_list:
            self.legendary_actions.append(Attribute(legendary_action))

    def __lt__(self, other):
        return self.name < other.name

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
        if self.saves != 'None':
            print(f"Saving Throws: {self.saves}")
        if self.skills != 'None':
            print(f"Skills: {self.skills}")
        if self.resistances != 'None':
            print(f"Resistances: {self.resistances}")
        if self.vulnerabilities != 'None':
            print(f"Vulnerabilities: {self.vulnerabilities}")
        if self.damage_immunities != 'None':
            print(f"Damage Immunites: {self.damage_immunities}")
        if self.condition_immunites != 'None':
            print(f"Condition Immunites: {self.condition_immunites}")
        if self.senses != 'None':
            print(f"Senses: {self.senses}, passive Perception {self.passive_perception}")
        else:
            print(f"Senses: passive Perception {self.passive_perception}")
        print(f"Languages: {self.languages}")
        print(f"Challenge: {self.cr}")

        if len(self.traits) > 0:
            print("\n==========Traits==========")
            for trait in self.traits:
                trait.display()

            wrapper = TextWrapper(width=gts().columns - 2, initial_indent="    ", subsequent_indent="    ")
            if self.spells != 'None':
                wrapped_spells_list = wrapper.fill(self.spells)
                print("- Spells List")
                print(wrapped_spells_list + "\n")

        if len(self.actions) > 0:
            print("==========Actions==========")
            for action in self.actions:
                action.display()

        if len(self.reactions) > 0:
            print("==========Reactions==========")
            for reaction in self.reactions:
                reaction.display()

        if len(self.legendary_actions) > 0:
            print("==========Legendary Actions==========")
            for legendary_action in self.legendary_actions:
                legendary_action.display()


class Item:
    """docstring for Item"""
    def __init__(self, e, file=None):
        self.element = e
        self.origin_file = file
        self.name = e.find('name').text

    def __lt__(self, other):
        return self.name < other.name

    def display(self):
        displayNext(self.element)


class Spell:
    """docstring for Spell class"""
    def __init__(self, e, file=None):
        self.element = e
        self.origin_file = file
        self.name = e.find('name').text
        self.level = e.find('level').text
        self.school = e.find('school').text if e.find('school') != None and e.find('school').text != None else 'None'
        self.ritual = e.find('ritual').text if e.find('ritual') != None and e.find('ritual').text != None else 'None'
        self.casting_time = e.find('time').text if e.find('time') != None and e.find('time').text != None else 'None'
        self.range = e.find('range').text if e.find('range') != None and e.find('range').text != None else 'None'
        self.component_string = e.find('components').text if e.find('components') != None and e.find('components').text != None else 'None'
        self.duration_string = e.find('duration').text if e.find('duration') != None and e.find('duration').text != None else 'None'
        self.classes_string = e.find('classes').text if e.find('classes') != None and e.find('classes').text != None else 'None'

        self.description = []
        lines = e.findall('text')
        for line in lines:
            if line.text != None:
                self.description.append(line.text)

        rolls = e.findall('roll') if e.findall('roll') != [] and e.findall('roll')[0].text != None else []
        self.rolls = []
        for roll in rolls:
            if roll.text != None:
                self.rolls.append(roll.text)

        # parseing component_string so it can be more easly searched later
        self.materials = 'None'
        self.verbal_component = 'None'
        self.somatic_component = 'None'
        self.material_component = 'None'
        if self.component_string != 'None':
            vsm = self.component_string
            if '(' in self.component_string and ')' in self.component_string:
                s = self.component_string
                materials_with_perens = s[s.find("("):s.find(")")+1]
                # self.materials will not have perens around it
                self.materials = s[s.find("(")+1:s.find(")")]
                vsm = s.replace(materials_with_perens, "")

            if 'v' in vsm.lower():
                self.verbal_component = 'V'
            if 's' in vsm.lower():
                self.somatic_component = 'S'
            if 'm' in vsm.lower():
                self.material_component = 'M'

    def __lt__(self, other):
        return self.name < other.name

    @property
    def readable_school(self):
        school = ''
        if self.school.lower() == 'a':
            school = 'Abjuration'
        elif self.school.lower() == 'c':
            school = 'Conjuration'
        elif self.school.lower() == 'd':
            school = 'Divination'
        elif self.school.lower() == 'en':
            school = 'Enchantment'
        elif self.school.lower() == 'ev':
            school = 'Evocation'
        elif self.school.lower() == 'I':
            school == 'Illusion'
        elif self.school.lower() == 'N':
            school = 'Necromancy'
        elif self.school.lower() == 'T':
            school = 'Transmutation'
        else:
            school = self.school

        return school


    @property
    def readable_level(self):
        level = ''
        if self.level == '0':
            level = 'Cantrip'
        elif self.level == '1':
            level = '1st Level'
        elif self.level == '2':
            level = '2nd Level'
        elif self.level == '3':
            level = '3rd Level'
        elif int(self.level) >= 4:
            level = f"{self.level}th Level"
        else:
            level = self.level

        return level


    def display(self):
        print = s_print
        wrapper = TextWrapper(width=gts().columns - 2, initial_indent="", subsequent_indent="")
        print(self.name)
        if self.level == '0':
            print(f"{self.readable_school} {self.readable_level}")
        else:
            if self.ritual != 'None':
                print(f"{self.readable_level} {self.readable_school} (ritual)")
            else:
                print(f"{self.readable_level} {self.readable_school}")
        if self. casting_time != 'None':
            print(f"Casting Time: {self.casting_time}")
        if self.range != 'None':
            print(f"Range: {self.range}")
        if self.component_string != 'None':
            wrapper.width = gts().columns - 14
            wrapper.subsequent_indent = '            '
            wrapped_components = wrapper.fill(self.component_string)
            print(f"Components: {wrapped_components}")
        if self.duration_string != 'None':
            print(f"Duration: {self.duration_string}")
        if self.classes_string != 'None':
            wrapper.width = gts().columns - 10
            wrapper.subsequent_indent = '          '
            wrapped_classes = wrapper.fill(self.classes_string)
            print(f"Classes: {wrapped_classes}")
        if self.rolls != []:
            joined_rolls = " | ".join(self.rolls)
            print(f"Rolls: {joined_rolls}")

        wrapper.width = gts().columns -2
        wrapper.subsequent_indent = ''
        description_lines = ""
        for i, line in enumerate(self.description):
            wrapped_line = wrapper.fill(line) + "\n"
            description_lines += wrapped_line
            if i + 1 != len(self.description):
                description_lines += '\n'

        print('\n==========Description==========')
        print(f"{description_lines}")


class CharacterClass:
    """docstring for CharacterClass"""
    def __init__(self, e, file=None):
        self.element = e
        self.origin_file = file
        self.name = e.find('name').text

    def __lt__(self, other):
        return self.name < other.name

    def display(self):
        displayNext(self.element)


class Race:
    """docstring for Race"""
    def __init__(self, e, file=None):
        self.element = e
        self.origin_file = file
        self.name = e.find('name').text

    def __lt__(self, other):
        return self.name < other.name

    def display(self):
        displayNext(self.element)


class Feat:
    """docstring for Feat"""
    def __init__(self, e, file=None):
        self.element = e
        self.origin_file = file
        self.name = e.find('name').text
        self.prerequisite = e.find('prerequisite').text if e.find('prerequisite') != None and e.find('prerequisite').text != None else 'None'
        self.modifier = e.find('modifier').text if e.find('modifier') != None and e.find('modifier').text != None else 'None'
        self.description = []
        lines = e.findall('text')
        for line in lines:
            if line.text == None:
                self.description.append('\n')
            else:
                self.description.append(line.text)

    def __lt__(self, other):
        return self.name < other.name

    def display(self):
        wrapper = TextWrapper(width=gts().columns - 2, initial_indent="  ", subsequent_indent="  ")
        print(self.name)
        if self.prerequisite != 'None':
            print(f"Prerequisite: {self.prerequisite}")
        if self.modifier != 'None':
            print(f"Modifier: {self.modifier}")
        description_lines = ''
        for line in self.description:
            wrapped_line = wrapper.fill(line) + '\n'
            description_lines += wrapped_line

        print('\n==========Description==========\n')
        print(description_lines)


class Background:
    """docstring for Background"""
    def __init__(self, e, file=None):
        self.element = e
        self.origin_file = file
        self.name = e.find('name').text

    def __lt__(self, other):
        return self.name < other.name

    def display(self):
        displayNext(self.element)
        
            
class GenericEntry:
    """docstring for GenericEntry"""
    def __init__(self, e, file=None):
        self.element = e
        self.origin_file = file
        self.name = e.find('name').text

    def __lt__(self, other):
        return self.name < other.name

    def display(self):
        displayNext(self.element)
