from tkinter import *

window = Tk()
window.geometry('350x650')
window.title("Login")
window.config(bg="BLACK")

def uname_click(*args):
	username.delete(0,'end')

def pass_click(*args):
	password.delete(0,'end')

def login():
	print(username.get())
	print(password.get())

#26ff00
label = Label(window, text="Online chess game", font=("Arial Bold", 25),fg="#26ff00",bg="BLACK")
#label.grid(column=0,row=0)
label.place(relx=0.07,rely=0.05)

label = Label(window, text="Login", font=("Arial Bold", 20),fg="#26ff00",bg="BLACK")

label.place(relx=0.35,rely=0.2)

username = Entry(window,width=21,font=('Impact',15),fg="BLACK",bd=2)
username.insert(0,"Username/Email")
username.place(relx=0.15,rely=0.3)
username.bind("<Button-1>",uname_click)


password = Entry(window,width=21,font=('Impact',15),fg="BLACK",bd=2,show="*")
password.insert(0,"Password")
password.place(relx=0.15,rely=0.4)
password.bind("<Button-1>",pass_click)

login_button = Button(text="Sign in",padx=85,font=('Impact',15),bg="LIGHTGREEN",command=login)
login_button.place(relx=0.15,y=375)

register_button = Button(text="Register",padx=78,font=('Impact',15),bg="LIGHTGREEN")
register_button.place(relx=0.15,y=450)

window.mainloop()