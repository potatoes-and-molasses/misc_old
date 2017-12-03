from Tkinter import *
import os
import time
pspath = r'\\open\nope.ps1' #change later to correct path
inpath = r'\\open\lol\in.txt'
newpictures = r'\\open\klol'
startscreen = r'C:\temp\untitled.gif'
local = r'C:\temp\ok.gif'
label=None
name = filter(lambda x: x != 'Thumbs.db',os.listdir(newpictures))
if(name):
    os.remove('{}\\{}'.format(newpictures,name[0]))
    


def leftclick(event):
    
    cmd = 'powershell {} \'move-mouse {} {};click-mouse left;Start-Sleep -Milliseconds 200;screenshot {}\''.format(pspath,event.x,event.y,newpictures)
    
    f=open(inpath,'w')
    f.write(cmd)
    f.close()
    update(label)

def rightclick(event):
    cmd = 'powershell {} \'move-mouse {} {};click-mouse right;Start-Sleep -Milliseconds 200;screenshot {}\''.format(pspath,event.x,event.y,newpictures)
    f=open(inpath,'w')
    f.write(cmd)
    f.close()
    update(label)

def mousemove(event):
    cmd = 'powershell {} \'move-mouse {} {};Start-Sleep -Milliseconds 200;screenshot {}\''.format(pspath,event.x,event.y,newpictures)
    f=open(inpath,'w')
    f.write(cmd)
    f.close()
    update(label)


def update(label):
    lol = None
    while not lol:
        lol = filter(lambda x: x != 'Thumbs.db',os.listdir(newpictures))
        time.sleep(0.05)
    name = lol[0]
    if(name):
        os.rename('{}\\{}'.format(newpictures,name),local)
        img = PhotoImage(file=local)
        label.configure(image=img)
        label.image=img
        os.remove(local)

def textboxing(event):
    def send():
        msg = b.get()

        top.destroy()
        
        cmd = 'powershell {} \'sendkeys {};Start-Sleep -Milliseconds 200;screenshot {}\''.format(pspath,msg,newpictures)
        
        f=open(inpath,'w')
        f.write(cmd)
        f.close()
        update(label)
        root.focus_set()
        
    top = Toplevel()
    b=Entry(master=top)
    b.pack()
    c=Button(master=top,text='cool',command=send)
    d=Button(master=top,text='cancel',command=top.destroy)
    d.pack()
    c.pack()
    
    b.focus_set()
    top.mainloop()
   
def refresh(event):

    cmd = 'powershell {} \'screenshot {}\''.format(pspath,newpictures)
    f=open(inpath,'w')
    f.write(cmd)
    f.close()
    update(label)
    now = time.time()



root = Tk()
w,h = root.winfo_screenwidth(),root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w,h))
root.focus_set()
root.bind('<Escape>', lambda x: exit(0))
root.bind('<Button-1>',leftclick)
root.bind('<Button-3>',rightclick)
root.bind('<Button-2>',mousemove)
root.bind('<F5>',refresh)
root.bind('<Insert>',textboxing)



img = PhotoImage(file=startscreen)
label=Label(master=root,image=img)
label.image=img
label.grid(row=0,column=1)




root.mainloop()
