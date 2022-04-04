from tkinter import *
from tkinter import ttk
from configuration import configurator
class settingstabBuilder:
    def setmountpoint(self,event):
        config=self.configuration.config
        config["mount"]["mountpoint"]=event.widget.get()
        self.configuration.writeconfig()
    def setplayer(self,event):
        config=self.configuration.config
        config["videoplayer"]["player"]=event.widget.get()
        self.configuration.writeconfig()
    def buildsettingsTab(self,frame):
       root=frame
       style=ttk.Style()
       style.map('TCombobox', selectbackground=[('readonly', NONE)])
       themelabel=Label(root,text="Theme : ")
       current_var=StringVar()
       themeselection=ttk.Combobox(root,textvariable=current_var)
       #themeselection["values"]="Azure"
       themeselection["state"]="disabled"
       themelabel.grid(row=0,column=0)
       themeselection.grid(row=0,column=1)
       mountpointlabel=Label(root,text="Mount Point : ")
       mountpointentry=ttk.Entry(root,takefocus=False)
       mountpointentry.bind("<KeyRelease>",self.setmountpoint)
       mountpointentry.insert(0,str(self.configuration.config["mount"]["mountpoint"]).replace('"',""))
       mediaplayerlabel=Label(root,text="Video Player : ")
       mediaplayerentry=ttk.Entry(root,takefocus=False)
       mediaplayerentry.insert(0,str(self.configuration.config["videoplayer"]["player"]).replace('"',""))
       mediaplayerentry.bind("<KeyRelease>",self.setplayer)
       mountpointlabel.grid(row=1,column=0)
       mountpointentry.grid(row=1,column=1,pady=5)
       mediaplayerlabel.grid(row=2,column=0)
       mediaplayerentry.grid(row=2,column=1,pady=5)
       root.pack(fill=BOTH,expand=True)
    def __init__(self,frame):
        self.configuration=configurator()
        self.buildsettingsTab(frame)
