import os,sys
import tkinter as tk
from tkinter import ttk
import subprocess
class tmpfs:
    def umount(self):
        os.system("echo "+self.authwindow.password+" |sudo -S fuser -k /mnt/")
        os.system("echo "+self.authwindow.password+" |sudo -S umount -f "+self.mountpoint)
    def mountdetect(self):
        out=subprocess.Popen(["mount | grep "+self.mountpoint],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        log,err=out.communicate()
        if "does not exist" in log.decode() or len(log.decode())==0:
            return True
        else:
            return False
    class auth:
        def savepw(self,event):
            password=event.widget.get()
            event.widget.delete(0,tk.END)
            self.password=password
            self.root.quit() # have to stop the mainloop before killing it
            self.root.destroy()
        def __init__(self):
            self.root=tk.Tk()
            root=self.root
            #root.tk.call("source", sys.path[0]+"/azure.tcl")
            #root.tk.call("set_theme", "dark")
            root.geometry("400x100")
            root.title("Enter your root password")
            mainframe=tk.Frame(root)
            passwordbox=ttk.Entry(root,show="*")
            passwordbox.pack(side=tk.TOP,fill=tk.X,expand=True)
            passwordbox.bind("<Return>",self.savepw)
            mainframe.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
            root.mainloop()
    def flushpw(self):
        del(self.authwindow.password) # remove password from the memory
    def mount(self):
        os.system("echo "+self.authwindow.password+" |sudo -S mount -t tmpfs -o size="+self.size+" tmpfs"+" /"+self.mountpoint)
    def __init__(self,size,mountpoint):
        self.size=size
        self.mountpoint=mountpoint
        self.authwindow=self.auth()
#tmpfs("10M","/mnt").mount()
