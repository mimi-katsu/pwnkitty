class Client:
    def __init__(self, pwnkitty, reader, writer, id, listener_id):
        self.pwnkitty = pwnkitty
        self.listener_id = listener_id
        self.id = id
        self.type = 'client'
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

    def issue_command(self, command):
        if command:
            arguments = command.split()
            comm = arguments[0]
            args = arguments[1:]
        if comm not in self.pwnkitty.command_parser.command_map.keys():
            self.pwnkitty.listeners[self.listener_id].outbuffer.put_nowait((self, command))
        elif comm in self.pwnkitty.command_parser.command_map.keys():
            self.pwnkitty.command_parser.command_map[comm].action(args)

    def __repr__(self):
        return f'{self.id}'