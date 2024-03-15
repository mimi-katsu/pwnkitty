"""PwnKitty class definition"""

from bin.menu import MainMenu
from bin.modules import Modules, CommandModules, EventModules
from bin.commandparser import CommandParser

class PwnKitty:
    """This class provides shared access to and tracks all attributes of all module
    class instances spawned through operation of the software"""

    def __init__(self):
        #   Class attributes for tracking class objects and stats that comprise the
        #   main functionality of the software

        self.session:object = None

        self.session_count = 0

        self.sessions:dict[object] = {}

        self.listeners = {}

        #   Init the references to the module objects that provide functionality to
        #   the software

        self.modules =  Modules(self)

        self.commands = CommandModules(self)

        self.events = EventModules(self)

        self.menu = MainMenu(self)

        self.command_parser = CommandParser(self)

