import asyncio    
import sys
async def async_input(string: str) -> str:
    inp = await asyncio.to_thread(input, string)
    return inp