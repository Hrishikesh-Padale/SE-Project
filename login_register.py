from tkinter import *
from PIL import Image,ImageTk
import sys
from socket import *
import pickle
from configure import *
import threading

password = ""

class Login_Register:
	def __init__(self):
		self.window = Tk()
		self.window.overrideredirect(1)
		self.window.geometry('350x650+500+50')
		self.window.title("Login")

		self.settings = read_settings()
		if not self.settings:
			update_settings()
			self.settings = read_settings()

		render = ImageTk.PhotoImage(image=Image.open('Media/cross.png').resize((20,20),Image.ANTIALIAS))
		self.cross = Button(image=render,command=self.close)
		self.cross.image = render
		self.cross.place(x=320,y=5)
		#self.window.config(bg="BLACK")
		self.label1 = Label(self.window, text="Online chess game", font=("Arial Bold", 25),fg="BLACK")
		self.label1.place(relx=0.07,rely=0.08)
		self.load_login_widgets()
		self.get_server()
		#self.load_register_widgets()
		self.invalid_creds = Label(self.window,text="Invalid Credentials",font=("Consolas",15),fg="RED")
		self.logged_in = Label(self.window,text="Logged in successfully",font=('Consolas',15),fg="GREEN")
		self.invalid_code = Label(self.window,text="Invalid code",font=('Consolas',15),fg="RED")

		self.mandatory = Label(self.window,text="All fields are required !",font=('Consolas',15),fg="RED")
		self.pass_mismatch = Label(self.window,text="Passwords dont match !",font=('Consolas',15),fg="RED")

		self.already_in_use = Label(self.window,text="Email already in use !",font=('Consolas',15),fg="RED")

		self.length_error = Label(self.window,text="Password must contain at least 5 characters",font=('Consolas',15),fg="RED")
		self.nouser = Label(self.window,text="No such user exits !",font=('Consolas',15),fg="RED")

	def get_server(self):
		self.ip = '65.0.204.13'
		self.port = 13000


	def receive(self):
		while True:
			try:
				self.data = sock.recv(4096)
			except:
				print("Error occured while receiving")
				self.sock.close()

	def load_login_widgets(self):

		self.label2 = Label(self.window, text="Login", font=("Arial Bold", 20),fg="BLACK")
		self.label2.place(relx=0.38,rely=0.18)
		
		self.username = Entry(self.window,width=21,font=('Impact',15),fg="BLACK",bd=2)
		self.password = Entry(self.window,width=21,font=('Impact',15),fg="BLACK",bd=2)

		if self.settings['Remember Credentials']=="True":
			self.username.insert(0,self.settings['UserID'])
			self.password.insert(0,self.settings['Password'])
			self.password.config(show = "*")
		else:
			self.username.insert(0,"GameID")
			self.password.insert(0,"Password")

		self.username.place(relx=0.15,rely=0.3)
		self.username.bind("<Button-1>",self.uname_click)	
		
		self.password.place(relx=0.15,rely=0.4)
		self.password.bind("<Button-1>",self.pass_click)

		self.show_pass = IntVar()
		self.show_pass_check = Checkbutton(text="Show Password",font=('Impact',15),variable=self.show_pass,onvalue=1,offvalue=0,command=self.login_show_pass)
		self.show_pass_check.place(relx=0.15,rely=0.5)

		if self.settings['Remember Credentials']=="True":
			self.remem = IntVar(value=1)
		else:
			self.remem = IntVar(value=0)

		self.remember_me = Checkbutton(text="Remember Me",font=('Impact',15),variable=self.remem,onvalue=1,offvalue=0,command=self.save_login)
		self.remember_me.place(relx=0.15,rely=0.6)
		
		self.login_button = Button(text="Sign in",padx=85,font=('Impact',15),bg="GREEN",command=self.login)
		self.login_button.place(relx=0.15,rely=0.7)
		
		self.register_button = Button(text="Register",padx=78,font=('Impact',15),bg="GREEN",command=self.forget_login_widgets)
		self.register_button.place(relx=0.15,rely=0.8)
		
		self.forgot_pass = Button(text="Forgot Password",padx=45,font=('Impact',15),bg="GREEN",command=self.load_forgotpass_widgets)
		self.forgot_pass.place(relx=0.15,rely=0.9)

	def load_register_widgets(self):

		self.label3 = Label(self.window, text="Register", font=("Arial Bold", 20),fg="BLACK")
		self.label3.place(relx=0.33,rely=0.18)

		self.Email = Entry(self.window,width=21,font=('Impact',15),fg="BLACK",bd=2)
		self.Email.insert(0,"Email")
		self.Email.place(relx=0.15,rely=0.3)
		self.Email.bind("<Button-1>",self.email_click)

		self.reg_username = Entry(self.window,width=21,font=('Impact',15),fg="BLACK",bd=2)
		self.reg_username.insert(0,"Username")
		self.reg_username.place(relx=0.15,rely=0.4)
		self.reg_username.bind("<Button-1>",self.reg_uname_click)

		self.reg_password = Entry(self.window,width=21,font=('Impact',15),fg="BLACK",bd=2)
		self.reg_password.insert(0,"Password")
		self.reg_password.place(relx=0.15,rely=0.5)
		self.reg_password.bind("<Button-1>",self.reg_pass_click)

		self.confirm_reg_password = Entry(self.window,width=21,font=('Impact',15),fg="BLACK",bd=2)
		self.confirm_reg_password.insert(0,"Confirm password")
		self.confirm_reg_password.place(relx=0.15,rely=0.6)
		self.confirm_reg_password.bind("<Button-1>",self.confirm_reg_pass_click)

		self.reg_button = Button(text="Register",padx=78,font=('Impact',15),bg="GREEN",command=self.reg)
		self.reg_button.place(relx=0.15,rely=0.7)

		self.go_back_button = Button(text="Go Back",padx=78,font=('Impact',15),bg="GREEN",command=self.forget_register_widgets)
		self.go_back_button.place(relx=0.15,rely=0.8)

	def load_otp_widgets(self):

		self.label3.place_forget()
		self.Email.place_forget()
		self.reg_username.place_forget()
		self.reg_password.place_forget()
		self.confirm_reg_password.place_forget()
		self.reg_button.place_forget()
		self.go_back_button.place_forget()
		try:
			self.mandatory.place_forget()
		except:
			pass

		self.label4 = Label(self.window,text="Enter OTP sent on your email",font=("Arial Bold", 15),fg="BLACK")
		self.otp = Entry(self.window,width=20,font=('Impact',15),fg="BLACK",bd=2)

		self.label4.place(relx=0.1,rely=0.2)
		self.otp.place(relx=0.15,rely=0.3)

		self.submit_button = Button(text="Submit",padx=78,font=('Impact',15),bg="GREEN",command=self.validate_otp_code)
		self.submit_button.place(relx=0.15,rely=0.4)

	def load_forgotpass_widgets(self):
		self.label2.place_forget()
		self.username.place_forget()
		self.password.place_forget()
		self.login_button.place_forget()
		self.register_button.place_forget()
		self.show_pass_check.place_forget()
		self.remember_me.place_forget()
		self.forgot_pass.place_forget()

		self.username.place(relx=0.15,rely=0.4)
		if not self.username.get():
			self.username.insert(0,'GameID')

		self.Reset_pass_text = Label(self.window,text="Reset Password",font=('Arial Bold',20),fg="GREEN")
		self.Reset_pass_text.place(relx=0.2,rely=0.25)

		self.forgot_password = Entry(self.window,width=21,font=('Impact',15),fg="BLACK",bd=2)
		self.forgot_password.insert(0,"Password")
		self.forgot_password.place(relx=0.15,rely=0.5)
		self.forgot_password.bind("<Button-1>",self.forgot_pass_click)

		self.confirm_forgot_password = Entry(self.window,width=21,font=('Impact',15),fg="BLACK",bd=2)
		self.confirm_forgot_password.insert(0,"Confirm password")
		self.confirm_forgot_password.place(relx=0.15,rely=0.6)
		self.confirm_forgot_password.bind("<Button-1>",self.confirm_forgot_pass_click)

		self.reset_pass_button = Button(text="Reset",padx=90,font=('Impact',15),bg="GREEN",command=self.reset_password)
		self.reset_pass_button.place(relx=0.15,rely=0.7)

		self.goback_from_reset = Button(text="Go Back",padx=80,font=('Impact',15),bg="GREEN",command=self.go_to_login)
		self.goback_from_reset.place(relx=0.15,rely=0.8)

	def forget_login_widgets(self):

		self.label2.place_forget()
		self.username.place_forget()
		self.password.place_forget()
		self.login_button.place_forget()
		self.register_button.place_forget()
		self.show_pass_check.place_forget()
		self.remember_me.place_forget()
		self.forgot_pass.place_forget()
		try:
			self.mandatory.place_forget()
		except:
			pass
		try:
			self.invalid_creds.place_forget()
		except:
			pass

		self.load_register_widgets()

	def forget_register_widgets(self):

		self.label3.place_forget()
		self.Email.place_forget()
		self.reg_username.place_forget()
		self.reg_password.place_forget()
		self.confirm_reg_password.place_forget()
		self.reg_button.place_forget()
		self.go_back_button.place_forget()
		try:
			self.mandatory.place_forget()
		except:
			pass

		self.load_login_widgets()

	def forget_otp_widgets(self):

		self.label4.place_forget()
		self.otp.place_forget()
		self.submit_button.place_forget()

		self.load_login_widgets()


	def go_to_login(self):

		self.forgot_password.place_forget()
		self.confirm_forgot_password.place_forget()
		self.reset_pass_button.place_forget()
		self.goback_from_reset.place_forget()
		self.Reset_pass_text.place_forget()

		self.load_login_widgets()

	def validate_otp_code(self):
		otp_msg = {'ID':2,'Code':self.otp.get()}
		#self.sock = socket(AF_INET, SOCK_STREAM)
		#self.sock.connect((self.ip, self.port))
		self.sock2.send(pickle.dumps(otp_msg))
		data = self.sock2.recv(1024)
		data = pickle.loads(data)
		#print(data)
		if data['ID']==2:
			try:
				self.mandatory.place_forget()
			except:
				pass
			try:
				self.invalid_code.place_forget()
			except:
				pass
			self.forget_otp_widgets()
			self.load_login_widgets()
		else:
			self.invalid_code.place(relx=0.2,rely=0.5)
		print(data)
	
	
	def reset_password(self):

		print(bool(self.username.get()))

		if self.username.get() == "GameID" or not bool(self.username.get()):
			try:
				self.pass_mismatch.place_forget()
			except:
				pass

			try:
				self.length_error.place_forget()
			except:
				pass

			try:
				self.nouser.place_forget()
			except:
				pass
			self.mandatory.place(relx=0.15,rely=0.3)

		if self.forgot_password.get() == self.confirm_forgot_password.get() and self.username.get() != "GameID" and bool(self.username.get()):
			if len(self.forgot_password.get()) >= 5:
				message = {'ID':6,'UserID':self.username.get()}
				reply = self.sock3.recv(1024)
				reply = pickle.loads(reply)
				if reply['ID'] == 6 and bool(reply['Status']):
					self.sock3 = socket((AF_INET,SOCK_STREAM))
					self.sock3.connect((self.ip,self.port))
					self.sock3.send(pickle.dumps(message))
					message = {'ID':2,'Password':self.forgot_password.get()}
					self.sock3.send(pickle.dumps(message))
					reply = self.sock3.recv(1024)
					reply = pickle.loads(reply)
					if reply['ID']==8:
						print("Password reset successfully!")
						try:
							self.mandatory.place_forget()
						except:
							pass

						try:
							self.pass_mismatch.place_forget()
						except:
							pass

						try:
							self.length_error.place_forget()
						except:
							pass

						try:
							self.nouser.place_forget()
						except:
							pass

						self.username.place_forget()
						self.forgot_password.place_forget()
						self.confirm_forgot_password.place_forget()
						self.reset_pass_button.place_forget()
						self.load_login_widgets()
					else:
						self.invalid_code.place(relx=0.15,rely=0.3)
				else:
					try:
						self.mandatory.place_forget()
					except:
						pass

					try:
						self.pass_mismatch.place_forget()
					except:
						pass
					try:
						self.length_error.place_forget()
					except:
						pass

					self.nouser.place(relx=0.15,rely=0.3)


			else:
				try:
					self.mandatory.place_forget()
				except:
					pass

				try:
					self.pass_mismatch.place_forget()
				except:
					pass

				try:
					self.nouser.place_forget()
				except:
					pass
				self.length_error.place(relx=0.15,rely=0.3)
		else:
			try:
				self.mandatory.place_forget()
			except:
				pass

			try:
				self.length_error.place_forget()
			except:
				pass

			try:
				self.nouser.place_forget()
			except:
				pass

			self.pass_mismatch.place(relx=0.15,rely=0.3)

		

	def uname_click(self,*args):
		self.username.delete(0,'end')

	def email_click(self,*args):
		self.Email.delete(0,'end')

	def reg_uname_click(self,*args):
		self.reg_username.delete(0,'end')
	
	def pass_click(self,*args):
		if self.password.get() == "Password":
			self.password.delete(0,'end')

		if self.show_pass.get() == 0:	
			self.password.config(show = "*")

	def reg_pass_click(self,*args):
		self.reg_password.delete(0,'end')

	def confirm_reg_pass_click(self,*args):
		self.confirm_reg_password.delete(0,'end')

	def forgot_pass_click(self,*args):
		if self.forgot_password.get() == "Password":
			self.forgot_password.delete(0,'end')

	def confirm_forgot_pass_click(self,*args):
		if self.confirm_forgot_password.get() == "Confirm password":
			self.confirm_forgot_password.delete(0,'end')

	
	def login(self,*args):
		print(self.username.get())
		print(self.password.get())
		if not bool(self.username.get()) or not bool(self.password.get()) or self.username.get()=="GameID" or self.password.get()=="Password":
			self.mandatory.place(relx=0.1,rely=0.24)

		else:
			#self.update_configurations()
			message = {'ID':5,'UserID':self.username.get(),'Password':self.password.get(),'Loggedin':0}
			self.sock1 = socket(AF_INET, SOCK_STREAM)
			self.sock1.connect((self.ip, self.port))
			self.sock1.send(pickle.dumps(message))
			reply = self.sock1.recv(1024)
			print(pickle.loads(reply))
			reply = pickle.loads(reply)
			if reply['ID']==501:
				try:
					self.mandatory.place_forget()
				except:
					pass
				try:
					self.invalid_creds.place(relx=0.2,rely=0.24)
				except:
					pass
				self.sock1.close()
			else:
				try:
					self.invalid_creds.place_forget()
				except:
					pass

				try:
					self.mandatory.place_forget()
				except:
					pass

				self.logged_in.place(relx=0.1,rely=0.24)
				#timer = threading.Timer(3.0, self.close())
				#timer.start()
				temp = open("Temp","w")
				temp.write(self.password.get())
				temp.close()
				self.update_configurations()
				self.window.destroy()
	
	def register(self,*args):
		print("Registeration")

	def reg(self,*args):
		print("Registeration online")
		if not bool(self.Email.get()) or not bool(self.reg_username.get()) or not bool(self.reg_password.get()) or not bool(self.confirm_reg_password.get()) or self.Email.get()=="Email" or self.reg_username.get()=="Username" or self.reg_password.get()=="Password" or self.confirm_reg_password.get() == "Confirm password":
			self.mandatory.place(relx=0.1,rely=0.24)
		else:
			self.sock2 = socket(AF_INET, SOCK_STREAM)
			self.sock2.connect((self.ip, self.port))
			email = self.Email.get()
			uname = self.reg_username.get()
			password = self.reg_password.get()
			reconfirm_pass = self.confirm_reg_password.get()
			message = {'ID':700}
			self.sock2.send(pickle.dumps(message))
			if password == reconfirm_pass:
				message = {'ID':1,'UserID':uname,'Email':email,'Password':password}
				self.sock2.send(pickle.dumps(message))
				reply = self.sock2.recv(1024)
				print(pickle.loads(reply))
				try:
					self.pass_mismatch.place_forget()
				except:
					pass

				try:
					self.mandatory.place_forget()
				except:
					pass

				#add already existing email condition

				self.load_otp_widgets()
			else:
				try:
					self.mandatory.place_forget()
				except:
					pass
				self.pass_mismatch.place(relx=0.1,rely=0.24)

			

	def save_login(self,*args):
		print(self.remem.get())

	def login_show_pass(self,*args):
		if self.show_pass.get() == 1:
			if self.password.get() == "Password":
				self.password.delete(0,'end')
			self.password.config(show="")

		else:
			self.password.config(show="*")


	def close(self):
		# ID = 600 --> logging out from login page 
		#message = {'ID':600}
		try:
			self.sock1.send(pickle.dumps(message))
			self.sock1.close()
		except:
			pass

		try:
			self.sock2.send(pickle.dumps(message))
			#self.sock2.close()
		except:
			pass
		self.window.destroy()

	def update_configurations(self):
		if self.remem.get():
			update_settings(UserID=self.username.get(),Password=self.password.get())
		else:
			update_settings()