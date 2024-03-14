import asyncio
import secrets
import sys
from util.client import ReverseClient
from util.tools import async_input
class TCPListener:
    def __init__(self, pwnkitty):
        self.id = secrets.token_hex(8)
        self.settings:object = self.Settings()
        self.pwnkitty = pwnkitty
        self.pwnkitty.obj_list.append(self)

        self.__inbuffer = asyncio.Queue(maxsize=0)
        self.outbuffer = asyncio.Queue(maxsize=0)


    name = 'TCP Reverse Shell listener'
    type = 'tcp-reverse'
    label = 'reverse'
    help_str = 'Create a listener to catch incoming reverse shells using TCP protocol'
    is_async = True
    def __repr__(self):
        return f'{self.id}:{self.type}:{self.settings.lhost}:{self.settings.lport}'

    class Settings:
        def __init__(self):

            self.lport = None
            self.lhost = None
            self.def_lhost = '127.0.0.1'
            self.def_lport = '1234'

    async def close_conn(self, client:object):
        client.writer.close()
        await client.writer.wait_closed()

    async def send_data(self):
        '''grab a message from the outgoing data buffer. It should be a list comtaining
         the client writer and message data. split it apart and then send it''' 
        while True:
            data = await self.outbuffer.get()
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
                self.outbuffer.task_done()

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
        client = ReverseClient(self.pwnkitty, reader, writer, self.pwnkitty.session_count, self.id)
        self.pwnkitty.session_count += 1
        if not self.pwnkitty.session:
            self.pwnkitty.session = client
            self.pwnkitty.command_parser.update_command_map()

        self.pwnkitty.sessions[str(client.id)] = client
        print(f'Client connected from: {client.info.ip_addr}')

        await asyncio.gather(self.recv_data(client), self.send_data())

    async def start_listener(self,args):
        '''Check arguments then bind to specified port and ip address, and serve client_handler() to each connection'''
        if not args:
            lhost = self.settings.def_lhost
            lport = self.settings.def_lport
        else:
            lhost = args[0]
            lport = args[1]
            self.settings.lhost = lhost
            self.settings.lport = lport

        try:
            print(f'Lhost: {lhost}, lport: {lport}')
            lsocket = await asyncio.start_server(self.client_handler, lhost, lport)
            print(f"Listener OPEN on {lhost}, {lport}")

            # add this listeners id to global dictionary to track it
            self.pwnkitty.listeners[self.id] = self
            async with lsocket:
                await lsocket.serve_forever()
        except OSError:
            print('Port is already in use')


    action = start_listener