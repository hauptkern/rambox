from tkinter import *
from tkinter import ttk
from allocate import allocatetabBuilder
from createvisual import createvisual
from stream import streamtabBuilder
from settings import settingstabBuilder
import sys
root=Tk()
root.title("RamBOX")
root.geometry("600x300")
#root.resizable(0,0)
root.tk.call("source", sys.path[0]+"/azure.tcl")
root.tk.call("set_theme", "dark")
mainframe=Frame(root)
tabcontrol=ttk.Notebook(mainframe)
allocatetab=Frame(tabcontrol)
streamtab=Frame(tabcontrol)
settingstab=Frame(tabcontrol)
infographicframe=Frame(allocatetab)
createinformatic=createvisual(infographicframe,0)
buildallocateTab=allocatetabBuilder(allocatetab,infographicframe)
buildstreamTab=streamtabBuilder(streamtab)
buildsettingsTab=settingstabBuilder(settingstab)
tabcontrol.add(allocatetab,text="Allocate")
tabcontrol.add(streamtab,text="Torrents")
tabcontrol.add(settingstab,text="Settings")
tabcontrol.pack(fill=BOTH,expand=True)
mainframe.pack(fill=BOTH,expand=True)
root.mainloop()
