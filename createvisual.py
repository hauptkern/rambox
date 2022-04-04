from tkinter import *
from tkinter import ttk
import psutil
class createvisual:
    def bytesto(self,bytes, to, bsize=1024): 
        a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
        r = float(bytes)
        return round(bytes / (bsize ** a[to]),0)
    def createcanvas(self,frame,ramfssize):
        root=frame
        for widget in root.winfo_children():
            widget.destroy()
        mainframe=Frame(root)
        canvas=Canvas(mainframe,width=280,height=100,bg="gray")
        virtualmemory=self.bytesto(psutil.virtual_memory()[0],"m")
        availablememory=self.bytesto(psutil.virtual_memory()[1],"m")
        canvasVirtlength=270
        canvasVirtheight=90
        canvasVirt=canvas.create_rectangle(5,5,5+canvasVirtlength,5+canvasVirtheight,fill="orange")
        virtmemtext="Virtual Memory : "+str(virtualmemory)+" Mbytes"
        canvasVirtlabel=canvas.create_text(8,8,text=virtmemtext,anchor=NW)
        canvasAvailable=canvas.create_rectangle(10,30,120,65,fill="red")
        canvasAvailabletext="Available \n"+str(availablememory)+" Mbytes"
        canvasAvailablelabel=canvas.create_text(14,32,text=canvasAvailabletext,anchor=NW)
        canvasramfs=canvas.create_rectangle(130,30,240,65,fill="green")
        canvasAvailabletext="TMPFS: \n"+str(ramfssize)+" Mbytes"
        canvasramfstext=canvas.create_text(135,32,text=canvasAvailabletext,anchor=NW)
        canvas.pack(side=TOP)
        mainframe.pack(side=TOP)
        root.pack(side=TOP)
    def __init__(self,frame,ramfssize):
        self.createcanvas(frame,ramfssize)