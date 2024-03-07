class ShowSessions:
    def __init__(self, server):
        self.server = server
        self.name = "Show Sessions"
        self.label = "sessions"
        self.action = self.show_sessions

    def show_sessions(self):
        print("Sessions\n=================")
        for s in self.server.sessions.keys():
            client = self.server.sessions[s]
            print(f"{client.id} : {client.ip_addr}")



def any(server, args):
    show = ShowSessions(server)
    show.show_sessions()