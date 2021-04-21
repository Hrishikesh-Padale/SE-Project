from socket  import *
import threading
import pickle

class User:
    def __init__(self):
        #login------------------------------------------------------
        self.recieved_messages = []
        self.quickplay_section_messages = []
        self.pwf_section_messages = []
        self.profile_section_messages = []
        self.ip = '65.0.204.13'
        self.port = 12000
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            print("Socket successfully created")
        except error as err:
            print("socket creation failed with error %s" % (err))
        self.sock.connect((self.ip, self.port))

        self.sock.send("Request".encode())
        self.sock.recv(1024)
        message = {'ID':5,'UserID':'Hrishi1234','Password':'1234'}
        self.sock.send(pickle.dumps(message))
        reply = self.sock.recv(1024)
        print("reply:",pickle.loads(reply))
        #------------------------------------------------------------

        self.Flist = pickle.loads(self.sock.recv(2048))
        self.recieve_thread = threading.Thread(target=self.recieve_messages) 
        self.recieve_thread.start()

    def send(self,data):
        try:
            self.sock.send(pickle.dumps(data))
        except:
            print("Error while sending message")

    
    def recieve_messages(self):
        while True:
            message = self.sock.recv(4096) 
            data = pickle.loads(message)
            self.recieved_messages.append(data)
            if data['ID']==24:
                self.pwf_section_messages.append(data)
            elif data['ID']==25:
                self.pwf_section_messages.append(data)
            elif data['ID']==7:
                self.pwf_section_messages.append(data)


    #def send_messages(self):
    #    while not self.logout:
    #        if len(self.sending_messages) > 0:
    #            message = self.sending_messages.pop(0)
    #            data = pickle.dumps()
    #            self.sock.send(data)
    #        else:
    #            continue
    #    return