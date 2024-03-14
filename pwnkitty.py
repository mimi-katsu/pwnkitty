from bin.pwnkitty import PwnKitty
from util.intro import play_intro
from util.tools import async_input
import asyncio

async def main():
    play_intro()

    pwnkitty = PwnKitty()
    await pwnkitty.menu.init_menu()
    print('Enter your command or "help" for more info')

if __name__=="__main__":
    asyncio.run(main())