import asyncio    
import secrets
import sys
from bin.modules import Modules, CommandModules, EventModules
from util.intro import play_intro
class MenuItem:
    def __init__(self, name, label, help_str, action):
        self.name = name
        self.label = label
        self.help_str = help_str
        self.action = action

    def execute(self):
            self.action(args)
        
class CommandParser:
    def __init__(self, server):
        self.server = server
        self.command_map = {}

        for m in server.commands.loaded:
            self.command_map[m.label] = m.action

    def run_command(self, command):
        arguments = command.split()
        comm = arguments[0]
        args = arguments[1:]
        self.command_map[comm](args)

class Settings:
    def __init__(self, lport=4444, lhost="0.0.0.0"):
        self.lport = lport
        self.lhost = lhost

class Client:
    def __init__(self, reader, writer, id):
        self.id = id
        self.reader = reader
        self.writer = writer
        self.messages = []
        self.ip_addr = writer.get_extra_info('peername')[0]
        self.label = None
        ## Machine information
        self.hostname = None
        self.os = None
        self.architecture = None
        self.Interfaces = None
        self.suid = None
        self.sudo = None
        self.users = None

    def __repr__(self):
        return f'{self.id}'

class Server:
    def __init__(self):
        self.sessions:dict[object] = {}
        self.session:object = None
        self.session_count = 0

        self.settings:object = Settings()
        self.modules:object = Modules(self)
        self.commands:object = CommandModules(self)
        self.ev_mods:object = EventModules(self)
        self.command_parser:object = CommandParser(self)

        self.__inbuffer = asyncio.Queue(maxsize=0)
        self.__outbuffer = asyncio.Queue(maxsize=0)

    async def close_conn(self, client:object):
        client.writer.close()
        await client.writer.wait_closed()

    async def send_data(self):
        '''grab a message from the outgoing data buffer. It should be a list comtaining
         the client writer and message data. split it apart and then send it''' 
        while True:
            data = await self.__outbuffer.get()
            client = data[0]
            message = data[1]

            try:
                client.writer.write((message + '\n').encode('utf-8'))
                await client.writer.drain()
            except ConnectionResetError:
                self.close_conn(client)
                print('Connection reset')

            except BrokenPipeError:
                self.close_conn(client)
                print('client removed')

            except ValueError as some_error:
                self.close_conn(client)
                print(ValueError)

            finally:
                self.__outbuffer.task_done()

    async def ainput(self, string: str) -> str:
        await asyncio.to_thread(sys.stdout.write, f'{string} ')
        return (await asyncio.to_thread(sys.stdin.readline)).rstrip('\n')

    async def create_message(self, targets=None):
        while True:
            msg = await self.ainput("")
            if msg.split()[0] in self.command_parser.command_map:
                self.command_parser.run_command(msg)
            elif not targets:
                self.__outbuffer.put_nowait((self.session,msg))
            else:
                for t in targets:
                    if t in self.sessions.keys():
                        self.__outbuffer.put_nowait((self.sessions[t], msg))

    async def recv_data(self, client):
        '''run a perpetual listener for data. when data is recieved 
        it gets placed into a buffer to be handled by the parse_data method'''
        while True:
            data = await client.reader.read(4096)
            if not data:
                break
            decoded_data = data.decode('utf-8')
            client.messages.append(decoded_data)
            print(client.messages[-1])

    async def client_handler(self, reader, writer):
        """create a client object and store it in the sessons dict."""
        client = Client(reader, writer, self.session_count)
        self.session_count += 1
        if not self.session:
            self.session = client
        self.sessions[str(client.id)] = client
        print(f'Client connected from: {client.ip_addr}')

        await asyncio.gather(self.recv_data(client), self.send_data(), self.create_message())

    async def start_listener(self):
        '''bind to specified port and ip address, and serve client_handler() to each connection'''
        lsocket = await asyncio.start_server(self.client_handler, self.settings.lhost, self.settings.lport)
        print(f"Listener OPEN on {self.settings.lhost}, {self.settings.lport}")
        async with lsocket:
            await lsocket.serve_forever()

async def main():
    play_intro()
    server = Server()
    await server.start_listener()

if __name__ == "__main__":
    asyncio.run(main())