from tkinter import *
from PIL import Image,ImageTk
import sys


def close():
	sys.exit()


window = Tk()
window.geometry('400x820+1135+0')
window.title('Chat')
window.overrideredirect(1)
#window.config(bg="BLACK")

header = Label(window,bg="#ABB2B9",bd=0.1)
header.place(relwidth=1,relheight=0.06)

render = ImageTk.PhotoImage(image=Image.open('Media/cross.png').resize((20,20),Image.ANTIALIAS))
cross = Button(image=render,command=close)
cross.image = render
cross.place(relx=0.93,rely=0.004)

message_box = Text(window,width = 20, height = 2,bg = "#17202A",fg = "#EAECEE",font = "Helvetica 14", padx = 5,pady = 5)
message_box.place(relheight = 0.9,relwidth = 1,rely=0.06)

message_box.config(state = DISABLED)

footer = Label(window,bg = "#ABB2B9")
footer.place(relwidth=1,rely=0.9,relheight=0.1)

message_input = Entry(footer,bg = "#2C3E50",fg = "#EAECEE",font = "Helvetica 13 bold")
message_input.place(relwidth = 0.74,relheight = 0.8,rely = 0.1,relx = 0.02)

send_button = Button(footer,text = "Send",font = "Helvetica 12 bold", width = 20,bg = "#ABB2B9")
send_button.place(relx=0.78,rely=0.1,relwidth=0.2,relheight=0.8)

window.mainloop()