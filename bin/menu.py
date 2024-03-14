import secrets
from util.tools import async_input
class MainMenu:
    def __init__(self, pwnkitty):
        self.name = 'Main Menu'
        self.label = 'Main Menu'
        self.pwnkitty = pwnkitty
        self.type = 'menu'
        self.id = 'menu'

    async def init_menu(self):
        self.pwnkitty.session = self
        self.pwnkitty.command_parser.update_command_map()
        await self.get_input()

    async def get_input(self):
        while True:
            com = await async_input("\033[38;5;206m>:\033[0m")
            self.pwnkitty.session.issue_command(com)

    def issue_command(self, command):
        self.pwnkitty.command_parser.run_command(command)