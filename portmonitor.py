import tkinter
import psutil
import time
import sys

class portmoniter:
    def __init__(self,root):
        self.root=root
        self.root.title("Port Monitoring Dashboard")
        self.root.geometry("600x400")
        self.process_frame=tkinter.Frame(self.root)
        self.process_frame.pack(fill="both",expand=True)
        self.updatedashboard()
        
    def listeningprocess(self):
        listening={}
        for i in psutil.net_connections():
            if i.status==psutil.CONN_LISTEN:
                pid=i.pid 
                port=i.laddr.port 
                process=psutil.Process(pid)
                listening[(pid,port)]=process.name()
        return listening

    def stopprocess(self,pid,port):
        process=psutil.Process(pid)
        process.kill()
    
    def updatedashboard(self):
        for widget in self.process_frame.winfo_children():
            widget.destroy()
        listening=self.listeningprocess()
        for (pid,port),name in listening.items():
            row=tkinter.Frame(self.process_frame)
            row.pack(fill="x",pady=2)

            info =f"PID: {pid}, Port: {port}, Process: {name}"
            lbl=tkinter.Label(row,text=info,anchor="w")
            lbl.pack(side="left",fill="x",expand=True)

            btn=tkinter.Button(row,text="Stop Process",command=lambda:self.stopprocess(pid,port),bg="red",fg="white")
            btn.pack(side="right",padx=10)
        self.root.after(1000,self.updatedashboard)
       
def onblock(popup,pid):
    process=psutil.Process(pid)
    process.kill()
    popup.destroy()

def onallow(popup):        
    popup.destroy()
        
knownprocess={}
def showwarning(pid,port,name):
        popup=tkinter.Tk()
        popup.title("New Listening Process Detected")
        popup.geometry("400x150")
        popup.attributes("-topmost",True)

        msg=f"New process is listening:\nPID: {pid}\nPort: {port}\nProcess: {name}"
        label=tkinter.Label(popup,text=msg,pady=10)
        label.pack()

        btn_frame=tkinter.Frame(popup)
        btn_frame.pack(pady=10)

        allow_btn=tkinter.Button(btn_frame,text="Allow",command=lambda:onallow(popup),width=10)
        allow_btn.pack(side="left",padx=10)

        block_btn=tkinter.Button(btn_frame,text="Block",command=lambda:onblock(popup,pid),width=10)
        block_btn.pack(side="right",padx=10)
        popup.mainloop()


def listeningprocess():
        listening={}
        for i in psutil.net_connections():
            if i.status==psutil.CONN_LISTEN:
                pid=i.pid 
                port=i.laddr.port 
                process=psutil.Process(pid)
                listening[(pid,port)]=process.name()
        return listening

def monitorports():
        global knownprocess
        if len(knownprocess)==0:
            knownprocess=listeningprocess()
        while True:
            current=listeningprocess()
            for (pid,port),name in current.items():
                if (pid,port) not in knownprocess:
                    showwarning(pid,port,name)
                    knownprocess[(pid, port)]=name

            to_remove=[k for k in knownprocess if k not in current]
            for k in to_remove:
                del knownprocess[k]
            time.sleep(2)

#main
if sys.argv[1]== "gui":
    root = tkinter.Tk()
    app = portmoniter(root)
    root.mainloop()

elif sys.argv[1]=="alert":
    monitorports()
