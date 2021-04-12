from tkinter import *
from PIL import Image,ImageTk
import sys


class Login_Register:
	def __init__(self):
		self.window = Tk()
		self.window.overrideredirect(1)
		self.window.geometry('350x650+500+50')
		self.window.title("Login")
		render = ImageTk.PhotoImage(image=Image.open('Media/cross.png').resize((20,20),Image.ANTIALIAS))
		self.cross = Button(image=render,command=self.close)
		self.cross.image = render
		self.cross.place(x=320,y=5)
		#self.window.config(bg="BLACK")
		self.label1 = Label(self.window, text="Online chess game", font=("Arial Bold", 25),fg="BLACK")
		self.label1.place(relx=0.07,rely=0.08)
		self.load_login_widgets()
		#self.load_register_widgets()


	def load_login_widgets(self):

		self.label2 = Label(self.window, text="Login", font=("Arial Bold", 20),fg="BLACK")
		self.label2.place(relx=0.38,rely=0.18)
		
		self.username = Entry(self.window,width=21,font=('Impact',15),fg="BLACK",bd=2)
		self.username.insert(0,"GameID/Email")
		self.username.place(relx=0.15,rely=0.3)
		self.username.bind("<Button-1>",self.uname_click)
			
		self.password = Entry(self.window,width=21,font=('Impact',15),fg="BLACK",bd=2)
		self.password.insert(0,"Password")
		self.password.place(relx=0.15,rely=0.4)
		self.password.bind("<Button-1>",self.pass_click)

		self.show_pass = IntVar()
		self.show_pass_check = Checkbutton(text="Show Password",font=('Impact',15),variable=self.show_pass,onvalue=1,offvalue=0,command=self.login_show_pass)
		self.show_pass_check.place(relx=0.15,rely=0.5)

		self.remem = IntVar()
		self.remember_me = Checkbutton(text="Remember Me",font=('Impact',15),variable=self.remem,onvalue=1,offvalue=0,command=self.save_login)
		self.remember_me.place(relx=0.15,rely=0.6)
		
		self.login_button = Button(text="Sign in",padx=85,font=('Impact',15),bg="GREEN",command=self.login)
		self.login_button.place(relx=0.15,rely=0.7)
		
		self.register_button = Button(text="Register",padx=78,font=('Impact',15),bg="GREEN",command=self.forget_login_widgets)
		self.register_button.place(relx=0.15,rely=0.8)
		
		self.forgot_pass = Button(text="Forgot Password",padx=45,font=('Impact',15),bg="GREEN",command=self.forgot_password)
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


	def forget_login_widgets(self):

		self.label2.place_forget()
		self.username.place_forget()
		self.password.place_forget()
		self.login_button.place_forget()
		self.register_button.place_forget()
		self.remember_me.place_forget()
		self.forgot_pass.place_forget()

		self.load_register_widgets()

	def forget_register_widgets(self):

		self.label3.place_forget()
		self.Email.place_forget()
		self.reg_username.place_forget()
		self.reg_password.place_forget()
		self.confirm_reg_password.place_forget()
		self.reg_button.place_forget()
		self.go_back_button.place_forget()

		self.load_login_widgets()



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
	
	def login(self,*args):
		print(self.username.get())
		print(self.password.get())
		#self.window.destroy()
	
	def register(self,*args):
		print("Registeration")

	def reg(self,*args):
		print("Registeration online")

	def save_login(self,*args):
		print(self.remem.get())

	def login_show_pass(self,*args):
		if self.show_pass.get() == 1:
			if self.password.get() == "Password":
				self.password.delete(0,'end')
			self.password.config(show="")

		else:
			self.password.config(show="*")

	def forgot_password(self,*args):
		print("Forgot Password")

	def close(self):
		sys.exit()


login = Login_Register()
login.window.mainloop()