import os
import fnmatch
import xml.etree.ElementTree as ET

class Dndeck:
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


        monsters = []
        objects = []
        for root in roots:
            for x in root:
                if x.tag.lower() == 'monster':
                    temp = Monster(x)
                    # print(temp.name + " " + temp.readable_size + " " + str(len(temp.traits)))
                    monsters.append(Monster(x))
                objects.append((x[0].text,x))

        self._list = objects
        self._old_term = ""
        self._results = []
        self.state = 0

    def search(self, keyword):
        found = []
        self._old_term = keyword
        for x in self._list:
            if keyword.lower() in x[0].lower():
                found.append((str(len(found) + 1) + ' ' + x[0],x[1]))
        self._results = found

        if len(self._results) is 0:
            print("No Results Found")
            self.state = 0
        elif len(self._results) is 1:
            self.state = 2
        else:
            self.state = 1

    @property
    def show_results(self):
        for x in self._results:
                print(x[0])

    @property
    def get_results(self):
        return self._results

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