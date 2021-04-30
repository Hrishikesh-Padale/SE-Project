from socket  import *
import threading
import pickle
import sys

class User:
    def __init__(self,uID,password):
        #login------------------------------------------------------
        self.recieved_messages = []
        self.quickplay_section_messages = []
        self.pwf_section_messages = []
        self.profile_section_messages = []
        self.main_page_messages = []

        self.chat_messages = []
        self.board_messages = []

        self.color = None
        self.room_id = None
        self.enemy_name = None

        self.ip = '65.0.204.13'
        self.port = 13000
        self.uID = uID
        self.password = password

        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            print("Socket successfully created")
        except error as err:
            print("socket creation failed with error %s" % (err))
        try:
            self.sock.connect((self.ip, self.port))
            message = {'ID':5,'UserID':self.uID,'Password':self.password,'Loggedin':1}
            self.sock.send(pickle.dumps(message))
            reply = self.sock.recv(1024)
            print("Reply:",pickle.loads(reply))
            #------------------------------------------------------------
            self.Flist = pickle.loads(self.sock.recv(2048))
            print(self.Flist)
            self.recieve_thread = threading.Thread(target=self.recieve_messages) 
            self.recieve_thread.start()
        except:
            print("Server is not running")
            sys.exit()

    def send(self,data):
        try:
            self.sock.send(pickle.dumps(data))
        except:
            print("Error while sending message")

    
    def recieve_messages(self):
        while True:
            try:
                message = self.sock.recv(4096) 
                if message:
                    data = pickle.loads(message)
                    print(data)
                    self.recieved_messages.append(data)

                    if data['ID']==24:
                        self.pwf_section_messages.append(data)

                    elif data['ID']==25:
                        self.pwf_section_messages.append(data)

                    elif data['ID']==7:
                        print("Error occured! - {}".format(data))

                    elif data['ID']==50:
                        self.main_page_messages.append(data)

                    elif data['ID']==55:
                        self.pwf_section_messages.append(data)

                    elif data['ID']==2200:
                        self.main_page_messages.append(data)
                        self.pwf_section_messages.append(data)
                        self.quickplay_section_messages.append(data)

                    elif data['ID'] == 11:
                        self.pwf_section_messages.append(data)

                    elif data['ID'] == 30:
                        self.chat_messages.append(data)

                    elif data['ID'] == 12:
                        self.pwf_section_messages.append(data)

                    elif data['ID'] == 27:
                        self.profile_section_messages.append(data)

                    elif data['ID'] == 60:
                        self.board_messages.append(data)

                    elif data['ID'] == 40:
                        self.profile_section_messages.append(data)

                    elif data['ID'] == 56:
                        self.quickplay_section_messages.append(data)

                    elif data['ID'] == 57:
                        pass

                    elif data['ID'] == 28:
                        self.profile_section_messages.append(data)

                    elif data['ID'] == 13:
                        self.pwf_section_messages.append(data)

            except:
                break
