from tkinter import *
from tkinter import ttk
from functools import partial
from tkinter import filedialog as fd
from torrent import torrent
import threading
# TO-DO
# Magnet link support
class streamtabBuilder:
    def openFiledialog(self):
        filetypes=(("Torrent Files","*.torrent"),('All files', '*.*'))
        filepath=fd.askopenfilename(title="Select a torrent file",filetypes=filetypes)
        self.magnetentry.delete(0,END)
        if str(filepath)=="()" or len(str(filepath))<=3:
            filepath=""
            pass
        else:
            self.magnetentry.insert(0, str(filepath))
            self.torrentsession=torrent(str(filepath))
            self.torrentsession.resetclass=streamtabBuilder
            self.torrentsession.resetframe=self.frame
            self.torrenttable()
    def listboxselection(self,event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            for widget in self.rootframe.winfo_children():
                widget.destroy()
            self.torrentsession.startstream(data,self.rootframe)
    def torrenttable(self):
        root=self.torrentinfobox
        for widget in root.winfo_children():
            widget.destroy()
        filelistbox=Listbox(root)
        filelist=self.torrentsession.getFilenames()
        for file in filelist:
            filelistbox.insert(0,str(file))
        filelistbox.bind("<<ListboxSelect>>",self.listboxselection)
        xscrollbar=Scrollbar(root,orient="horizontal")
        xscrollbar.pack(side = BOTTOM,fill=X)
        filelistbox.pack(side=LEFT,fill=BOTH,expand=True)
        yscrollbar = Scrollbar(root)
        yscrollbar.pack(side = RIGHT,fill=Y)
        filelistbox.config(yscrollcommand = yscrollbar.set,xscrollcommand=xscrollbar.set)
        xscrollbar.config(command=filelistbox.xview)
        yscrollbar.config(command = filelistbox.yview)
    def clearout(self,event):
        event.widget.delete(0,END)
    def buildStreamtab(self,frame):
        root=frame
        self.rootframe=frame
        mainframe=Frame(root)
        self.mainframe=mainframe
        self.magnetentry=ttk.Entry(mainframe,takefocus=0)
        self.magnetentry.insert(0,"Torrent File Path")
        #self.magnetentry.bind("<FocusIn>",self.clearout)
        self.magnetentry.pack(side=LEFT,expand=True,fill=X)
        dialogbutton=ttk.Button(mainframe,text="Browse",command=self.openFiledialog)
        dialogbutton.pack(padx=5,side=LEFT)
        self.torrentinfobox=Frame(root)
        testbutton=ttk.Label(self.torrentinfobox,text="Torrent information will be shown here.",justify=CENTER)
        testbutton.place(anchor=CENTER,relx=.5,rely=.5)
        mainframe.pack(side=TOP,fill=BOTH)
        self.torrentinfobox.pack(side=TOP,fill=BOTH,pady=10,expand=True)
    def __init__(self,frame):
        self.frame=frame
        self.buildStreamtab(frame)