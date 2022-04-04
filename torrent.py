import libtorrent as lt
import time
import sys,random,queue,os
from mount import tmpfs
from configuration import configurator
from tkinter import *
import threading
from tkinter import ttk
import subprocess
class torrent:
    def createsession(self):
        self.randPort=random.randint(6000, 20000)
        self.ses = lt.session({'listen_interfaces': '0.0.0.0:'+str(self.randPort)})
        #print("Started torrent session on port "+str(self.randPort))
    def getfilesize(self,filename):
        self.setfileindex(filename)
        #print(str(self.info.files().file_name(self.indexno))+" "+str(self.info.files().file_size(self.indexno)/1048576))
        return int(round(float(self.info.files().file_size(self.indexno)/1048576),0))
    def setfileindex(self,filename):
        for indexno in range(0,self.info.files().num_files()):
            if filename==self.info.files().file_path(indexno):
                self.indexno=indexno
                break
    def hasmetadata(self,filename):
        self.configuration=configurator().readconfig()
        configuration=self.configuration
        try:
            filepath=configuration["mount"]["mountpoint"]+"/"+filename
            result = subprocess.run(['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', filepath], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if float(result.stdout)>0:
                #print(float((result.stdout)))
                return True
        except Exception as err:
            return False
    def setpriority(self,filename):
        self.setfileindex(filename)
        for i in range(0,self.info.files().num_files()):
            if i!=self.indexno:
                self.h.file_priority(i,0)
            elif i==self.indexno:
                self.h.file_priority(i,8)
        self.h.resume()  
    def startstream(self,filename,mainframe):
        self.createsession()
        self.filepath=filename
        tmpfssize=self.getfilesize(filename)
        self.configuration=configurator().readconfig()
        configuration=self.configuration
        self.mountedfs=tmpfs(str(tmpfssize+5)+"M",configuration["mount"]["mountpoint"])
        self.mountedfs.mount()
        self.h=self.ses.add_torrent({'ti': self.info, 'save_path': configuration["mount"]["mountpoint"]+"/"})
        while (not self.h.has_metadata()):
            time.sleep(1)
        self.h.pause()
        # self.h.set_sequential_download(True)
        self.setpriority(filename)
        self.mainframe=mainframe
        self.progressupdater=threading.Thread(target=self.streamloader,daemon=True)
        self.progressupdater.start()
    def kill(self,event):
        self.h.pause()
        time.sleep(1)
        self.mountedfs.umount()
        sys.exit()
    def streamloader(self):
        s=self.h.status()
        mainframe=self.mainframe
        configuration=self.configuration
        playerpath=configuration["videoplayer"]["player"]
        mountpoint=configuration["mount"]["mountpoint"]+"/"
        for widget in mainframe.winfo_children():
            widget.destroy()
        statuslabel=ttk.Label(mainframe,text="Loading...",justify=CENTER)
        statuslabel.pack(side=LEFT)
        statusbutton=ttk.Button(mainframe,text="Kill")
        statusbutton.bind("<Button-1>",self.kill)
        statusbutton.pack(side=RIGHT)
        playerrunning=False
        while (not s.is_seeding):
            s=self.h.status()
            if round(s.progress*100,0)==100 and playerrunning==False:
                playerrunning=True
                statuslabel.configure(text="Opened "+str(playerpath)+" player.")
                x=subprocess.Popen([playerpath,mountpoint+self.filepath])
                status=x.wait()
                self.h.pause()
                time.sleep(2)
                self.mountedfs.umount()
            else:
                statuslabel.configure(text="Loading "+str(self.filepath).split("/")[-1][:35]+"... "+str(round(s.progress*100,2))+"%"f' D:{str(s.download_rate / 1000).split(".")[0]} kB/s')
            time.sleep(0.5)
    def getFilenames(self):
        self.info=lt.torrent_info(self.link)
        filenames=[]
        for file in range(0,self.info.files().num_files()):
            filenames.append(self.info.files().file_path(file))
        return filenames
    def __init__(self,filepath):
        self.link=filepath