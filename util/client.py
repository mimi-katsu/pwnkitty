class MachineInfo:
    def __init__(self):
        self.hostname = None
        self.os = None
        self.architecture = None
        self.Interfaces = None
        self.suid = None
        self.sudo = None
        self.users = None
        self.ip_addr = None

class ReverseClient:
    def __init__(self, pwnkitty, reader, writer, id, listener_id):
        self.pwnkitty = pwnkitty
        self.listener_id = listener_id
        self.id = id
        self.type = 'client'
        self.reader = reader
        self.writer = writer
        self.messages = []
        self.label = None
        self.info = MachineInfo()
        self.info.ip_addr = writer.get_extra_info('peername')[0]

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