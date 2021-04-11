from tkinter import *
from PIL import Image,ImageTk
import sys

class Login:
	def __init__(self):
		self.window = Tk()
		self.window.overrideredirect(1)
		self.window.geometry('350x650+500+50')
		self.window.title("Login")
		render = ImageTk.PhotoImage(image=Image.open('Media/cross.png').resize((20,20),Image.ANTIALIAS))
		self.cross = Button(image=render,command=self.close)
		self.cross.image = render
		self.cross.place(x=320,y=5)
		#self.window.config(bg="WHITE")

		self.label = Label(self.window, text="Online chess game", font=("Arial Bold", 25),fg="BLACK")
		self.label.place(relx=0.07,rely=0.08)

		self.label = Label(self.window, text="Login", font=("Arial Bold", 20),fg="BLACK")
		self.label.place(relx=0.38,rely=0.18)
		
		self.username = Entry(self.window,width=21,font=('Impact',15),fg="BLACK",bd=2)
		self.username.insert(0,"GameID/Email")
		self.username.place(relx=0.15,rely=0.3)
		self.username.bind("<Button-1>",self.uname_click)
			
		self.password = Entry(self.window,width=21,font=('Impact',15),fg="BLACK",bd=2,show="*")
		self.password.insert(0,"Password")
		self.password.place(relx=0.15,rely=0.4)
		self.password.bind("<Button-1>",self.pass_click)
		
		self.login_button = Button(text="Sign in",padx=85,font=('Impact',15),bg="GREEN",command=self.login)
		self.login_button.place(relx=0.15,y=375)
		
		self.register_button = Button(text="Register",padx=78,font=('Impact',15),bg="GREEN",command=self.register)
		self.register_button.place(relx=0.15,y=450)
		
		self.remem = IntVar()
		self.remember_me = Checkbutton(text="Remember me",font=('Impact',15),variable=self.remem,onvalue=1,offvalue=0,command=self.save_login)
		self.remember_me.place(relx=0.15,y=310)

		self.forgot_pass = Button(text="Forgot Password",padx=45,font=('Impact',15),bg="GREEN",command=self.forgot_password)
		self.forgot_pass.place(relx=0.15,y=525)

	def uname_click(self,*args):
		self.username.delete(0,'end')
	
	def pass_click(self,*args):
		self.password.delete(0,'end')
	
	def login(self,*args):
		print(self.username.get())
		print(self.password.get())
		#self.window.destroy()
	
	def register(self,*args):
		print("Registeration")

	def save_login(self,*args):
		print(self.remem.get())

	def forgot_password(self,*args):
		print("Forgot Password")

	def close(self):
		sys.exit()


login = Login()
login.window.mainloop()