from bin.menu import MainMenu 
from bin.modules import Modules, CommandModules, EventModules
from bin.commandparser import CommandParser

class PwnKitty:
    def __init__(self):
        self.name = "PwnKitty"
        self.sessions:dict[object] = {}
        self.session:object = None
        self.session_count = 0
        self.listeners = {}
        self.modules =  Modules(self)
        self.commands = CommandModules(self)
        self.events = EventModules(self)
        self.menu = MainMenu(self)
        self.command_parser = CommandParser(self)