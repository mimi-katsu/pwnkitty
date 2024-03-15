"""Main entry to PwnKitty"""

import asyncio

from bin.pwnkitty import PwnKitty
from util.intro import play_intro

async def main():
    """Play intro, init modules, and then make entry to the program"""

    play_intro()

    pwnkitty = PwnKitty()

    await pwnkitty.menu.init_menu()

    print('Enter your command or "help" for more info')

if __name__=="__main__":
    asyncio.run(main())
