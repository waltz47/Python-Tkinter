from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import os
import tkinter
from tkinter import *
import tkinter.messagebox
from tkcolorpicker import askcolor
import time
from time import sleep
import threading
from PIL import ImageTk, Image
import pymysql

my_user_name = str(time.time())
pnconfig = PNConfiguration()
random_user_name = str(time.time())
pnconfig.publish_key = #your publish key
pnconfig.subscribe_key = #your sub key
pnconfig.uuid = myuuid = my_user_name #unique username
pubnub = PubNub(pnconfig)
channel_name = "my-channel"

myfont = "consolas" 
db = pymysql.connect(#your sql login)
dbc = db.cursor()
# dbc.execute("select * from userlist")
# print(list())
# dbc.execute("create table userlist(name varchar(30), username varchar(30), password int)")
def get_message(msg, state): 
	chats.config(state = NORMAL)
	chats.tag_configure('right_side', justify = 'left', rmargin = 10,spacing1 = 10,spacing3 = 1, selectbackground = chats.cget("background"))
	chats.tag_configure('left_side', justify = 'right', rmargin = 10, spacing1 = 10, spacing3 = 1, selectbackground = chats.cget("background"))
	chats.tag_configure('centered', justify = 'center', background = "red")
	if state == 0:
		chats.insert(END,msg, 'left_side')
		chats.config(font = ("Consolas",0))
		chats.insert(END,"\n")
		chats.config(font = (myfont,16))
	elif state == 1:
		chats.insert(END,msg, 'right_side')
		chats.config(font = (myfont,2))
		chats.insert(END,"\n")
		chats.config(font = (myfont,16))
	else:
		chats.insert(END,msg + "\n", 'centered')
	chats.config(state = DISABLED)
def my_publish_callback(pb, status):
	if  status.is_error():
		pass #message successfully passed
		# get_message("message couldnt be sent due to unknown reasons",0)
	else:
		pass #message sending failed	
def here_now_callback(result, status):
	if status.is_error():
		return
	ret = []
	for chD in result.channels:
		for occ in chD.occupants:
			ret.append(str(occ.uuid))
	active_users_update(ret)
	
class MySubscribeCallback(SubscribeCallback):
	def presence(self, pubnub, presence):
			update_users()
			
	def status(self, pubnub, status):
		if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
			# pubnub.publish().channel(channel_name).message("has left!").pn_async(my_publish_callback)
			update_users()
			
		elif status.category == PNStatusCategory.PNConnectedCategory:
			# pubnub.publish().channel(channel_name).message("joined the channel").pn_async(my_publish_callback)
			update_users()
		elif status.category == PNStatusCategory.PNReconnectedCategory:
			pass #connectivity regained
		elif status.category == PNStatusCategory.PNDecyptionErrorCategory:
			pass #message decryption error	
	def message(self, pubnub, message):
			if message.publisher != my_user_name:
				get_message(message.publisher + ":" + message.message,1)
				
def update_users():
	pubnub.here_now().channels(channel_name).include_state(False).include_uuids(True).pn_async(here_now_callback)
	threading.Timer(3.0,update_users).start()
	pass

class Register(tkinter.Toplevel):
	def __init__(self,window):
		super().__init__(window)
		self.rt = window
		self.title("Register Details")
		self.geometry("300x200")
		msg_sign = StringVar()
		msg_sign.set("Name")
		self.e0 = tkinter.Entry(self, text = msg_sign)
		self.e0.pack(padx = 20, ipadx = 20, pady = 5, ipady = 4)
		self.e0.bind("<FocusIn>", lambda event = None:self.e0.delete("0","end"))
		msg_sign = StringVar()
		msg_sign.set("UserName")
		self.e1 = tkinter.Entry(self, text = msg_sign)
		self.e1.pack(padx = 20, ipadx = 20, pady = 5, ipady = 4)
		self.e1.bind('<FocusIn>',lambda event=None:self.e1.delete("0","end"))
		msg_sign_pwd = StringVar()
		msg_sign_pwd.set("Password")
		self.e2 = tkinter.Entry(self, text = msg_sign_pwd)
		self.e2.pack(padx = 20, ipadx = 20, pady = 5, ipady = 4)
		self.e2.bind('<FocusIn>',lambda evt = None: pwdd())
		def pwdd(event = None):
			self.e2.delete("0","end")
			self.e2.config(show = "*")
		btn2 = tkinter.Button(self, text = "Register", command = self.db_insert, relief = "solid", bg = "white")
		btn2.pack(ipady = 6, ipadx = 10)
		
	def db_insert(self, event = None):
		name = self.e0.get()
		username = self.e1.get()
		password = self.e2.get()
		if len(name) < 1 or len(username) <1 or len(password) < 1 or name == "Name" or username == "UserName" or password == "Password":
			tkinter.messagebox.showinfo(message = "Invalid creds")
			return
		global dbc
		dbc.execute("select * from userlist where username='{0}'".format(username))
		result = dbc.fetchall()
		l=0
		for x in result:
			print(x)
			l+=1
		if l == 0:
			# print("looks good", len(list(result)))
			dbc.execute("insert into userlist values('{0}','{1}','{2}')".format(name,username,password))
			db.commit()
			self.withdraw()
			self.rt.deiconify()
		else:
			tkinter.messagebox.showinfo(message = "User name already exists")
		
class Login(tkinter.Toplevel):
	def __init__(self, window):
		super().__init__(window)
		self.rt = window;
		self.title("Login")
		self.geometry("300x200")
		msg_sign = StringVar()
		msg_sign.set("UserName")
		self.e1 = tkinter.Entry(self, text = msg_sign)
		self.e1.pack(padx = 20, ipadx = 20, pady = 5, ipady = 4)
		self.e1.bind('<FocusIn>',lambda event=None:self.e1.delete("0","end"))
		msg_sign_pwd = StringVar()
		msg_sign_pwd.set("Password")
		self.e2 = tkinter.Entry(self, text = msg_sign_pwd)
		self.e2.pack(padx = 20, ipadx = 20, pady = 5, ipady = 4)
		self.e2.bind('<FocusIn>',lambda event=None:pwd())
		def pwd():
			self.e2.delete("0","end")
			self.e2.config(show = "*")
		btn1 = tkinter.Button(self, text="Go", command = self.going, relief = "solid", bg = "white")
		btn1.pack(pady = 5, ipady = 2, ipadx = 5)
		btn2 = tkinter.Button(self, text = "Register", command = self.reg, relief = "solid", bg = "white")
		btn2.pack(ipady = 1, ipadx = 5)
	def reg(self, event = "None"):
		self.withdraw()
		reg = Register(self)	
	def going(self,event="nothing"):
		myname = self.e1.get()
		password = self.e2.get()
		if len(myname) < 1 or len(password) < 1 or myname == "UserName" or password == "Password":
			tkinter.messagebox.showinfo(message ="Enter valid username/password")
			return
		good = 0
		global dbc
		dbc.execute("select * from userlist where username='{0}' and password='{1}'".format(myname,password))
		result = dbc.fetchall()
		l = 0
		for x in result:
			print(x)
			l+=1
		if l >= 1:
			good = 1
		else:
			tkinter.messagebox.showinfo(message = "Invalid username or password")
		if good == 1:
			global my_user_name
			my_user_name = myname
			global pubnub
			global pnconfig
			pnconfig.uuid = my_user_name
			pubnub = PubNub(pnconfig)
			pubnub.add_listener(MySubscribeCallback())
			pubnub.subscribe().channels(channel_name).with_presence().execute()
			self.withdraw()
			self.rt.deiconify()	
			message_entry.focus_set()
	
def active_users_update(curr):
			curr.sort()
			active_users.delete("activeuserlist")
			mystr = ""
			for i in range(len(curr)):
				mystr += str(curr[i]) + "\n"
				if i == len(curr) - 1:
					active_users.create_text(5,5, tag = "activeuserlist", anchor = tkinter.NW, text = mystr, font = (myfont,15), fill = "#faf0e6")
					active_users.config(scrollregion = active_users.bbox("activeuserlist"))

def send_message(my_message):
	get_message(my_message, 0)
	env = pubnub.publish().channel(channel_name).message(my_message).sync()
window = tkinter.Tk()
window.geometry("{0}x{1}". format (
	int(0.6*window.winfo_screenwidth()), int(0.6*window.winfo_screenheight()) 
))
window.title("Messenger app")
window.resizable(False,False)
window.withdraw()
lw = Login(window)
def color_pick(event = None):
	col = askcolor()
	chats.config(background = col[1])
frame_left_active_users = tkinter.Frame(window,width = 200, bd = 2,background = "white", relief = GROOVE)   
frame_left_active_users.pack(side = "left", fill = "y", padx = 10,  pady = 10)
frame_bottom_message_entry = tkinter.Frame(window, height = 130)                            
frame_bottom_message_entry.pack_propagate(0);
frame_bottom_message_entry.pack(side = "bottom", fill = "x")
text_receiving_frame = tkinter.Frame(window, bg = "white", width = 600, height = 1000)
text_receiving_frame.pack_propagate(0)
text_receiving_frame.pack(fill = "both", padx = 10)
chats_scroll = tkinter.Scrollbar(text_receiving_frame)
chats_scroll.pack(side = "right", fill = "y")
chat_label = tkinter.Label(text_receiving_frame, text = "Conversations", font = (myfont, 17),background = "white", borderwidth = 3, relief = "solid")
chat_label.pack_propagate(0)
chat_label.pack(expand = "true", fill = "y")
chats = tkinter.Text(text_receiving_frame, font = (myfont,16),bg = "#312222", fg = "white")
chats.pack(fill = "both", expand = "true", pady = 5, ipadx = 5)
chats.bind("<Button-3>",color_pick)
chats_scroll.config(command = chats.yview)
chats.config(yscrollcommand = chats_scroll.set)
chats.config(state = "disabled", cursor = "arrow")
def check_function(key = None):
	my_message = message_entry.get()
	ok = 0
	for ch in my_message:
		if ch != ' ':
			ok = 1
	if ok == 0:
		message_entry.delete(0,"end")
		return
	if len(my_message) < 1 or my_message == "Enter your messages here":
		return
	if my_message == "whoami":
		get_message(my_user_name,0)
		message_entry.delete(0,"end")
		return
	send_message(my_message)
	message_entry.delete(0,'end') 
def clear_sign(key):
	message_entry.delete(0,'end')
msg_sign = StringVar()
msg_sign.set("Enter your messages here")
message_entry = tkinter.Entry(frame_bottom_message_entry, textvariable = msg_sign, font = (myfont, 15))
message_entry.bind("<FocusIn>", clear_sign)
message_entry.bind("<Return>",check_function) 
iimg = Image.open("filled-sent.png")
iimg = iimg.resize((20,20), Image.ANTIALIAS)
photo_img = ImageTk.PhotoImage(iimg)
send = tkinter.Button(message_entry, text = "Send", font = (myfont,10), relief = "solid", command = lambda:check_function(0) and clear_sign(0))
send.config(image = photo_img)
send.pack_propagate(0)
send.pack(side = "right", ipadx = 15, ipady = 7)
message_entry.pack_propagate(0)																												
message_entry.pack(fill = "x",ipady = 8)
label_in_frame_active_users = tkinter.Label(frame_left_active_users, text="Active", font = (myfont,17),borderwidth = 5, relief = "solid")
label_in_frame_active_users.pack(side = "top", fill = "x")
iimg = Image.open("img.png")
iimg = iimg.resize((1800,1000),Image.ANTIALIAS)
img = ImageTk.PhotoImage(iimg)
active_users = tkinter.Canvas(frame_left_active_users, scrollregion = (0,0,50,50))
active_users.pack(expand = "true", fill = "both", side = "left", ipadx = 0)
active_users.create_image(1,1,image = img,anchor = tkinter.NW)
active_scroll = tkinter.Scrollbar(frame_left_active_users, orient = VERTICAL)
active_users.config(yscrollcommand = active_scroll.set)
active_scroll.config(command = active_users.yview)
active_scroll.pack(side = "right", fill = "y")
def on_closing(evt = None):
	pubnub.unsubscribe().channels(channel_name).execute() #unsub from channel
	db.close()  #close connections from mysql
	window.destroy()
	os._exit(0)
window.protocol("WM_DELETE_WINDOW", on_closing)    
window.mainloop()
