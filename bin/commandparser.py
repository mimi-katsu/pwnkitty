import asyncio

class CommandParser:
    def __init__(self, pwnkitty):
        self.pwnkitty = pwnkitty
        self.command_map = {}

    def run_command(self, command):
        if command:
            arguments = command.split()
            comm = arguments[0]
            args = arguments[1:]
            if comm in self.command_map.keys():
                if self.command_map[comm].is_async:
                    asyncio.create_task(self.command_map[comm].action((args)))
                else:
                    self.command_map[comm].action((args))

    def update_command_map(self):
        self.command_map = {}
        for c in self.pwnkitty.commands.loaded:
            if self.pwnkitty.session.type in c.types:
                self.command_map[c.label] = c

        if self.pwnkitty.session.type == 'menu':
            for c in self.pwnkitty.modules.loaded:
                self.command_map[c.label] = c