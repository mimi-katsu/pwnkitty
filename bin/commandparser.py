import asyncio

class CommandParser:
    def __init__(self, pwnkitty):
        self.pwnkitty:object = pwnkitty
        self.command_map:dict = {}

    def run_command(self, command:str):
        if command:
            arguments = command.split()
            comm = arguments[0]
            args = arguments[1:]
            if comm in self.command_map.keys():
                if self.command_map[comm].is_async:
                    obj = self.command_map[comm](self.pwnkitty)
                    asyncio.create_task(obj.action((args)))
                else:
                    self.command_map[comm].action((args))
                    
    def update_command_map(self):
        """load all appropriate commands for the given session (based on session types) into the 
        command map to allow for execution. If the current session is the menu, add the main modules 
        as well"""
        #   Clear the current command map.
        self.command_map = {}
        for c in self.pwnkitty.commands.loaded:
            #   If the current session type ('client', 'menu', etc) is in the command classes 
            #   self.types attribute, make that command available during the current session.
            if self.pwnkitty.session.type in c.types:
                self.command_map[c.label] = c

        if self.pwnkitty.session.type == 'menu':
            #   Make modules available for execution when current session is the main menu.
            for c in self.pwnkitty.modules.loaded:
                self.command_map[c.label] = c