from textwrap import TextWrapper
from shutil import get_terminal_size as gts

from utils import m_print, wrap_lines

class GenericTrait:
    """docstring for Trait"""
    def __init__(self, e):
        self.type = e.tag
        self.name = e.find('name').text
        self.description = []
        lines = e.findall('text')
        for line in lines:
            if line.text == None:
                self.description.append('\n')
            else:
                self.description.append(line.text)

    def __repr__(self):
        return f"Class: {self.__class__.__name__} Name: {self.name}"

    def display(self):
        wrapper = TextWrapper(width=gts().columns - 2, initial_indent="", subsequent_indent="")
        print(self.name)
        print(wrap_lines(wrapper, self.description))


class Trait(GenericTrait):
    """docstring for BGTrait"""
    def __init__(self, e):
        super().__init__(e)

    def display(self):
        wrapper = TextWrapper(width=gts().columns - 2, initial_indent="    ", subsequent_indent="    ")
        print(f"- {self.name}")
        print(f"{wrap_lines(wrapper, self.description)}")
        

class Attribute(GenericTrait):
    """docstring for Attribute

    For use with the Monster class"""
    def __init__(self, e):
        super().__init__(e)
        self.attack = e.find('attack').text if e.find('attack') != None else 'None'

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