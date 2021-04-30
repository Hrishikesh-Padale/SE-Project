import socket
import threading
from database import Database
import pickle
from User import Client
import sys
import random
import smtplib
from email.message import EmailMessage

THREADS = []
CLOSE = False
PORT = 12000
IP = ''
DB = Database()
Users = []
Rooms = []
QUICK_PLAY = []
Message_Queue = []

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((IP, PORT))
sock.listen(20)

def random_number():
    num = random.randint(100000, 999999)
    return str(num)


def Send_VerificationCode(to, uid, code):
    msg = EmailMessage()
    msg['Subject'] = 'Verification Code From Chess Project'
    msg['From'] = 'Chess Project SE 2021'
    msg['To'] = to
    msg.set_content('Hello {},\n\n \t Your verification code is {}'.format(uid, code))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login('chessprojectse2021@gmail.com', '')
            server.send_message(msg)
        print("Mail sent1")
        return True
    except:
        return False


def Send_Welcome_Email(to, uid):
    msg = EmailMessage()
    msg['Subject'] = 'Welcome To Chess Project'
    msg['From'] = 'Chess Project SE 2021'
    msg['To'] = to
    msg.set_content('Hello {},\n \t Your account has successfully activated. Lets start the game'.format(uid))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login('chessprojectse2021@gmail.com', '')
            server.send_message(msg)
        print("Mail sent2")
        return True
    except:
        return False

def handle_client(conn, data):
    Exit = False
    print(data)
    while not Exit:    
        #rec = conn.recv(1024)
        #data =  pickle.loads(rec)
        id = data['ID']
        userid, password = data['UserID'], data['Password']
        if id == 5:
            if DB.validate_user(userid, password):
                rdata = {
                    'ID': 500,
                    'Message' : 'Login successfull'
                }
                rdata = pickle.dumps(rdata)
                conn.send(rdata)
                #Starting client
                #print("1: {}".format(len(Users)))
                loggedin = data['Loggedin']
                if loggedin:
                    c = Client(UserID=userid, conn=conn, database=DB, users=Users, rooms=Rooms, quickplay = QUICK_PLAY, message_queue=Message_Queue)
                    for usr in Users:
                        if usr['UserID'] == userid:
                            Users.remove(usr)
                            print("User removed from the existing list")
                            break
                    Users.append({'UserID':userid, 'conn': conn, 'Client': c})
                    #print("2: {}".format(len(Users)))
                    c.start()
                    print("{} User logout".format(userid))
                else:
                    Exit = True
                    
                Exit = True
            else:
                data = {
                    'ID' : 501,
                    'Message' : 'Invalid credentials'
                }
                data = pickle.dumps(data)
                conn.send(data)
                Exit = True
                sys.exit()
                return
        elif id == 6:           ##Forgot password
            #email = data['Email']
            uid = data['UserID']
            email = DB.get_emailid(uid=uid)
            if email:
                print(email)
                ncode = random_number()
                Send_VerificationCode(to=email, uid=uid, code=ncode)
                data = {
                    'ID':6,
                    'Message':"User Exist",
                    'Status':True
                }
            else:
                data = {
                    'ID':6,
                    'Status':False,
                    'Message':"User does not exist"
                }
            conn.send(pickle.dumps(data))
        elif id == 2:
            revcode = data['Code']
            if revcode == code:
                newpass = data['Password']
                
                if DB.update_user_password(uid, newpass) :
                    data = {
                        'ID' : 8,
                        'Message': "Password update successful"
                    }
                else:
                    data = {
                        'ID' : 7,
                        'Message' : 'Password update unsuccessful'
                    }
                Exit = True
            else:
                #ncode = random_number()
                #Send_VerificationCode(to=email, code=ncode)
                data = {
                    'ID' : 9,
                    'Message':'Invalide Code,'
                }
                
            data = pickle.dumps(data)
            conn.send(data)
        elif id == 600:
            Exit = True
            return
        else:
            data = {
                'ID': 7,
                'Message': 'Invalid ID Used for sending message'
            }
            data = pickle.dumps(data)
            conn.send(data)
    print("Returning from handle client")        
    return

# def forgot_password(conn):
#     EXIT = False
#     while not exit:
#         rev = conn.recv(1024)
#         data = pickle.loads(rev)
#         if id == 1100:
#             email = data['Email']
#             userid = data['UserID']
#             #send these details to database to recover password
#             continue
#         else:
#             data = {
#             'ID': 7,
#             'Message': 'Invalid ID Used for sending message'
#             }
#             data = pickle.dumps(data)
#             conn.send(data)



def Register_Client(conn, rdata):
    Exit = False
    Variefy = False
    while not Variefy:
        print("Inside the loop register")
        rev = conn.recv(1024)
        rdata = pickle.loads(rev)
        id = rdata['ID']
        if id == 1:
            uid = rdata['UserID']
            # uname = data['Username']
            email = rdata['Email']
            passwd = rdata['Password']
            ####Add these fields to Clients table
            #try:
            if (DB.Add_new_User(uid, email, Password= passwd)):
                code = random_number()
                data = {
                    'ID': 1000,
                    'Message': 'Successful but not varified',
                    #'Code' : code,
                }
                #    continue
                # Send email to the client for verification with code
                Send_VerificationCode(email, uid, code)
            else:
                data = {
                    'ID' : 1500,
                    'Message': 'User with given email address is already exist'
                }
            # except:
            #     print("Error while Creating new user with username {}".format(uid))
            #     data = {
            #         'ID' : 2000,
            #         'Message' : 'Registration Unsuccessfull'
            #     }
            #     # data = pickle.dumps(data)
                # conn.send(data)
                #continue
            ####After success send the message of confermation
            
            data = pickle.dumps(data)
            conn.send(data)
            #rev = sock.recv(2048)
            #rdata = pickle.dumps(rev)
            Exit = True
        elif id == 2:
            revcode = rdata['Code']
            print("Recieved code is {}".format(revcode))
            if revcode == code:
                Variefy = True
                DB.verify_user(uid=uid)
                data = {
                    'ID': 2,
                    'Message': 'Successful and varified',
                }
            else:
                #ncode = random_number()
                #Send_VerificationCode(to=email, code=ncode)
                data = {
                    'ID' : 9,
                    'Message':'Invalide Code, new verification code sent'
                }
                
            data = pickle.dumps(data)
            conn.send(data)
        else:
            continue
    print("Completed")
    return

print("Server is running on port {}".format(PORT))

while not CLOSE:
    try:
        conn, addr = sock.accept()
        #rec = conn.recv(1024).decode()
        rec = conn.recv(2048)
        data = pickle.loads(rec)
        if data['ID'] == 5 or data['ID'] == 6:
            #conn.send("Connected".encode())
            thread = threading.Thread(target=handle_client, args=(conn,data,))
            THREADS.append({'conn': conn,'Thread':thread})
            thread.start()
        elif data['ID'] == 700:
            #conn.send("Connected".encode())
            thread1 = threading.Thread(target=Register_Client, args=(conn, rdata))
            THREADS.append({'Thread':thread1, 'conn':conn})
            thread1.start()
        # elif rec == 'ForgotPassword':
        #     conn.send("Connected".encode())
        #     thread2 = threading.Thread(target=forgot_password, args=(conn,))
        #     THREADS.append(thread2)
        #     thread2.start()
        else:
            continue    
    except KeyboardInterrupt:
        CLOSE = True
        print('')
        print("Server is closed")
    except ConnectionRefusedError:
        continue
    except:
        continue


# while len(THREADS) > 0:
for t in THREADS:
    t['Thread'].join()

print("Closing the server..........")