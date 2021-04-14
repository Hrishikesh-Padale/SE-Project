from tkinter import *
import random

window = Tk()
window.geometry('400x500+1125+290')
window.title('Chat')
#window.config(bg="BLACK")
messages = []
for i in range(30):
	msg = "Username:"
	for j in range(random.randint(10,20)):
		msg += chr(random.randrange(97,123))
	messages.append(msg)

messages[3] = "Username:The text written inside the widget is set to the control variable StringVar so that it can be accessed and changed accordingly."
for i in range(4):
	label = Label(window,text=messages[i],font=('consolas bold',14),wraplength=370,justify=LEFT)
	label.place(relx=0.05,rely=(i+0.5)*0.1)


#relative change caused by consolas-14 = 0.05

label = Label(window,text="Test",font=('consolas bold',14),wraplength=380,justify=LEFT)
label.place(relx=0.05,rely=0.1)
msginput = Entry(window,width=27,font=('consolas',15),bd=2)
msginput.place(relx=0.05,rely=0.87)
send_button = Button(text="Send",font=('consolas bold',11),bg="GREEN",fg="WHITE",padx=8)
send_button.place(relx=0.83,rely=0.865)
window.mainloop()