import asyncio
import secrets
import sys
from util.client import Client
from util.tools import async_input
class TCPListener:
    def __init__(self, pwnkitty):
        self.pwnkitty = pwnkitty
        self.id = secrets.token_hex(8)
        self.name = 'TCP Reverse Shell listener'
        self.label = 'reverse'
        self.help_str = 'Create a listener to catch incoming reverse shells using TCP protocol'
        self.action = self.start_listener
        self.is_async = True
        self.settings:object = self.Settings()
        self.__inbuffer = asyncio.Queue(maxsize=0)
        self.outbuffer = asyncio.Queue(maxsize=0)
        self.pwnkitty.listeners[self.id] = self
    class Settings:
        def __init__(self, lport=4444, lhost="0.0.0.0"):
            self.lport = lport
            self.lhost = lhost

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

    # async def create_message(self, targets=None):
    #     while True:
    #         msg = await async_input(">:")
    #         if msg:
    #             if msg.split()[0] in self.pwnkitty.command_parser.command_map.keys():
    #                 self.pwnkitty.command_parser.run_command(msg)
    #             elif not targets and self.pwnkitty.session.type != 'menu':
    #                 self.outbuffer.put_nowait((self.pwnkitty.session,msg))
    #             else:
    #                 for t in targets:
    #                     if t in self.sessions.keys():
    #                         self.outbuffer.put_nowait((self.pwnkitty.sessions[t], msg))

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
        client = Client(self.pwnkitty, reader, writer, self.pwnkitty.session_count, self.id)
        self.pwnkitty.session_count += 1
        if not self.pwnkitty.session:
            self.pwnkitty.session = client
            self.pwnkitty.command_parser.update_command_map()

        self.pwnkitty.sessions[str(client.id)] = client
        print(f'Client connected from: {client.ip_addr}')

        await asyncio.gather(self.recv_data(client), self.send_data())

    async def start_listener(self, _):
        '''bind to specified port and ip address, and serve client_handler() to each connection'''
        lsocket = await asyncio.start_server(self.client_handler, self.settings.lhost, self.settings.lport)
        print(f"Listener OPEN on {self.settings.lhost}, {self.settings.lport}")
        async with lsocket:
            await lsocket.serve_forever()