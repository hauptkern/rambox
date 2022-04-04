from tkinter import *
from tkinter import messagebox as msg
from tkinter import ttk
from functools import partial
import psutil
from createvisual import createvisual
from mount import tmpfs
from configuration import configurator
class allocatetabBuilder:
    def bytesto(self,bytes, to, bsize=1024): 
        a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
        r = float(bytes)
        return round(bytes / (bsize ** a[to]),0)
    def sliderset(self,scaleVal):
        self.sizeLabel.configure(text="Size: "+str(int(round(float(scaleVal),0)))+" MB")
        self.sizeSpin.delete(0,200)
        self.sizeSpin.insert(0,str(int(round(float(scaleVal),0))))
        self.availablememory=self.bytesto(psutil.virtual_memory()[1],"m")
        self.sizeSlider.configure(to=self.availablememory)
        self.tmpfsvalue=int(round(float(scaleVal),0))
        createvisual(self.infographicframe,int(round(float(scaleVal),0)))
    def spinset(self):
        self.sizeLabel.configure(text="Size: "+str(self.strsizeValue.get())+" MB")
        self.sizeSlider.set(float(self.strsizeValue.get()))
        self.availablememory=self.bytesto(psutil.virtual_memory()[1],"m")
        createvisual(self.infographicframe,int(round(float(self.strsizeValue.get()),0)))
        self.tmpfsvalue=int(round(float(self.strsizeValue.get()),0))
        self.sizeSpin.configure(to=self.availablememory)
    def spinkeyset(self,event):
        val=str(event.widget.get())
        if len(val)>0:
            self.sizeSlider.set(float(val))
    def setfilesystem(self):
        configuration=configurator().readconfig()
        if self.mountbtn["text"]=="Mount":
            try:
                self.mountedfs=tmpfs(str(self.tmpfsvalue)+"M",configuration["mount"]["mountpoint"])
                check=self.mountedfs.mountdetect()
                if check==True:
                    self.mountedfs.mount()
                    self.mountbtn["text"]="Unmount"
                else:
                    msg.showerror("Error","Mount point is already mounted. Please unmount the point before mounting.")
            except Exception as err:
                pass
        elif self.mountbtn["text"]=="Unmount":
            try:
                self.mountedfs.umount()
                self.mountbtn["text"]="Mount"
                self.mountedfs.flushpw()
                del(self.mountedfs)
            except Exception as err:
                pass
    def buildallocateTab(self,frame):
        root=frame
        #virtualmemory=int(round(self.bytesto(psutil.virtual_memory()[0],"m"),0))
        self.availablememory=self.bytesto(psutil.virtual_memory()[1],"m")
        self.sizeValue=DoubleVar()
        self.strsizeValue=StringVar()
        self.sizeLabel=Label(root,text="Size: ",anchor=NW)
        self.sizeLabel.pack(side=TOP,fill=X)
        self.sizeSlider=ttk.Scale(root,orient=HORIZONTAL,variable=self.sizeValue,from_=0,to=self.availablememory,command=self.sliderset)
        self.sizeSlider.pack(fill=X,side=TOP)
        self.sizeSpin=ttk.Spinbox(root,textvariable=self.strsizeValue,command=self.spinset,from_=0,to=self.availablememory)
        self.sizeSpin.bind("<KeyRelease>",self.spinkeyset)
        self.sizeSpin.pack(side=TOP,anchor=E)
        self.mountbtn=ttk.Button(root,text="Mount",command=self.setfilesystem)
        self.mountbtn.pack(side=BOTTOM,fill=X,pady=20)
    def __init__(self,frame,infographicframe):
        self.frame=frame
        self.infographicframe=infographicframe
        self.buildallocateTab(frame)
