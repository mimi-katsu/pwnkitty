from util.messages import ok, oops

class Help:
    def __init__(self, server):
        self.server = server
        self.label = "help"
        self.help_str = "Display the help message"
        self.action = self.show_help
        self.types = {'menu', 'client'}
        self.is_async = False

    def show_help(self, _):
        if self.server.modules.loaded:
            print("    Modules:\n")
     
            for m in self.server.modules.loaded:
                print(f'\t{m.label}{(" "* (25 - len(m.label)))}{m.help_str}')
            print('\n')
        if self.server.commands.loaded:
            print('    Commands:\n')
            for c in self.server.commands.loaded:
                if self.server.session.type in c.types:
                    print(f'\t{c.label}{(" "* (25 - len(c.label)))}{c.help_str}')
        ok()

class GoToMenu:
    def __init__(self,pwnkitty):
        self.pwnkitty = pwnkitty
        self.label = 'menu'
        self.help_str = 'Go back to the main menu'
        self.types = {'client'}
        self.is_async = False
        self.action = self.go_to_menu

    def go_to_menu(self,_):
        self.pwnkitty.session = self.pwnkitty.menu
        self.pwnkitty.command_parser.update_command_map()
        print("Main Menu")

class ShowSessions:
    def __init__(self, server):
        self.server = server
        self.label = 'sessions'
        self.help_str = 'List clients currently connected to the server'
        self.action = self.show_sessions
        self.types = {'menu', 'client'}
        self.is_async = False

    def show_sessions(self, _):
        print(f'\n[+] Sessions (Current: {self.server.session.label or self.server.session.id})\n')
        sesh_header = "ID" + (" "*18) + "Label" +(" "* 17)+ "Host"
        print(f'\t{sesh_header}\n\t{("=" * len(sesh_header))}')
        for s in self.server.sessions.keys():
            client = self.server.sessions[s]
            print(f'\t{client.id}{" " * (20 - len(str(client.id)))}{client.label or "None"}{" " * (20 - len(client.label or "None"))}{client.ip_addr}')
            print(f'\t{("-" * len(sesh_header))}')
        ok()

class ChangeSession:
    def __init__(self, server):
        self.server = server
        self.label = 'session'
        self.help_str = 'Change the active session. Ex: "session 1"'
        self.is_async = False

        self.action = self.change_sessions
        self.types = {'menu', 'client'}
    def change_sessions(self, args):
        if not args:
            print("Invalid arguments")
            oops()
        else:
            if args[0] in self.server.sessions.keys():
                self.server.session = self.server.sessions[args[0]]
                self.server.command_parser.update_command_map()
                print(f'Current session: {self.server.session}')
                ok()
            else:
                oops()
                print('[-] Session not found')

class Info:
    def __init__(self, server):
        self.server = server
        self.label = 'info'
        self.help_str = 'Display info about the current session'
        self.is_async = False

        self.action = self.show_info
        self.types = {'client'}
    
    def show_info(self, _):
        print(f'ID: {self.server.session.id}\nIp Address: {self.server.session.ip_addr}')
        ok()

class LabelSession:
    def __init__(self, server):
        self.server = server
        self.label = 'label'
        self.help_str = 'Make a label for a session. Ex: "label MySession" or "label 1 MySession" (label {id} name)'
        self.is_async = False

        self.action = self.make_label
        self.types = {'menu', 'client'}
    def make_label(self, args):
        if args:
            if args[0] in self.server.sessions.keys():  
                sesh = self.server.sessions[args[0]]
                label = " ".join(args[1:])
                sesh.label = label
                ok()
            else:
                self.server.session.label = " ".join(args)
                ok()
        else:
            oops()