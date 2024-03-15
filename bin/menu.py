"""Menu Class Definition"""

from util.tools import async_input

class MainMenu:
    """This menu class object gets passed around and tracked similar 
        to any of the session object, (ReverseCLient, BindCLient, etc), 
        however it runs a perpetual loop for user input and passes that 
        to the current sessions "issue_command" method which will cause 
        it to be executed"""

    def __init__(self, pwnkitty):

        self.pwnkitty = pwnkitty

        self.name = 'Main Menu'

        self.label = 'Main Menu'

        self.type = 'menu'

        self.id = 'menu'

    async def init_menu(self):
        """run at startup to create entry to the main menu"""
        self.pwnkitty.session = self

        self.pwnkitty.command_parser.update_command_map()

        await self.get_input()

    async def get_input(self):
        """create an infinite loop that waits for input and passes it to the 
        issue_command func of the object stored in the current session attribute 
        of the pwnkitty class"""

        while True:

            com = await async_input("\033[38;5;206m>:\033[0m")

            if com:

                self.pwnkitty.session.issue_command(com)


    def issue_command(self, command):
        """Class unique version of issue_command(). sends it straight to the 
        command parser"""
        self.pwnkitty.command_parser.run_command(command)
