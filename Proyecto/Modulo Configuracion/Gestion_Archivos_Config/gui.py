from Tkinter import *
import tkMessageBox

import datetime
from remoteUtilities import *

def btnAction():
    index = int(listBox.curselection()[0])
    remote_file = txtRemFile.get()
    #local_file = txtRemFile.get()
    dir_IP = txtIP.get()
    remote_user = txtUser.get()
    remote_password = txtPwd.get()
    directorio = txtRemDirect.get()
    print(dir_IP)
    try:
        if(index == 0):			#PUT
            local_file = txtLocalFile.get()
            putFile2(dir_IP, remote_file, local_file, remote_user, remote_password, directorio)
            tkMessageBox.showinfo("--", "El archivo se envio")
            

        if(index == 1):			#GET
            local_file = txtRemFile.get()
            getFile2(dir_IP, remote_file, local_file, remote_user, remote_password, directorio)
            tkMessageBox.showinfo("--", "El archivio se recibio")
            
    except Exception,e:
		print e	  


    
def onSelectedList(evt):
    now = datetime.datetime.now()
    marcaDeFecha=now.strftime("%Y-%m-%d_%H_%M_")

    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    #print '%d: "%s"' % (index, value)
    if(index==1):
        txtLocalFile.delete(0,END)
        txtLocalFile.insert(0,'/'+marcaDeFecha+txtRemFile.get())
        txtLocalFile.config(state='disabled')
    else:
        txtLocalFile.config(state='normal')
        

window = Tk()
window.title("Gestion de archivos de configuracion")
window.geometry('650x400')

lbl = Label(window, text="Transferencia")
lbl.grid(column=1, row=0, padx=10, pady=10)


lbl = Label(window, text="Archivo local:")
lbl.grid(column=0, row=2)

txtLocalFile = Entry(window,width=30)
txtLocalFile.grid(column=1, row=2, pady=7)


lbl = Label(window, text="Archivo remoto:")
lbl.grid(column=0, row=3, pady=7)

defaultText = StringVar()
defaultText.set('startup-config')

txtRemFile = Entry(window, width = 30, textvariable = defaultText)
txtRemFile.grid(column=1, row=3)


lbl = Label(window, text="Directorio remoto:")
lbl.grid(column=0, row=4, pady=7)

defaultText0 = StringVar()
defaultText0.set('/')

txtRemDirect = Entry(window, width = 30, textvariable = defaultText0)
txtRemDirect.grid(column=1, row=4)



lbl = Label(window, text="Dir. IP:")
lbl.grid(column=0, row=5)

txtIP = Entry(window,width=20)
txtIP.grid(column=1, row=5, sticky=W, pady=7)

defaultText2 = StringVar()
defaultText2.set('rcp')
lbl = Label(window, text="Usuario:")
lbl.grid(column=0, row=6)

txtUser = Entry(window,width=20, textvariable = defaultText2)
txtUser.grid(column=1, row=6, sticky=W, pady=7)


defaultText3 = StringVar()
defaultText3.set('rcp')

lbl = Label(window, text="Password:")
lbl.grid(column=0, row=7, pady=7)

txtPwd = Entry(window,width=20, textvariable = defaultText3)
txtPwd.grid(column=1, row=7, sticky=W)


lbl = Label(window, text="Operacion:")
lbl.grid(column=0, row=8, pady=7)

listBox = Listbox(window, height=2, width=15, name='listBox')
listBox.insert(1, "PUT (enviar)")
listBox.insert(2, "GET (recibir)")
#listBox.insert(3, "DEL (borrar local)") 
#listBox.insert(4, "DEL (borrar remoto)")
listBox.activate(2)
listBox.grid(column=1, row=8, sticky=W, pady=7)
listBox.bind('<<ListboxSelect>>', onSelectedList)


btn = Button(window, text="Iniciar", bg="light slate blue", command=btnAction)
btn.grid(column=1, row=9)


window.mainloop()
