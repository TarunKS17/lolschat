import socket, thread             
import Tkinter as tk

print 'Client'

root=tk.Tk()
root.title("Client")
root.geometry(('400x275'))

class Client(tk.Tk):

    s=''
    sending = False
    
    def __init__(self):
        self.display=tk.Label(root, text='Received messages appear here')
        tk.Label(root, text='Client').pack()
        self.inputf=tk.Entry(root)
        self.host=tk.Entry(root)
        self.port=tk.Entry(root)
        self.send=tk.Button(root, text="Send", command=self.Send)
        self.connect=tk.Button(root, text="Connect", command=lambda: self.Connect(self.host.get(), int(self.port.get())))
        self.exit=tk.Button(root, text='Exit', command=self.Exit)
        self.placewidgets()
        #self.Connect()
        
    def placewidgets(self):
        tk.Label(root, text='Host IP Address').pack()
        self.host.pack()
        tk.Label(root, text='Port').pack()
        self.port.pack()
        self.connect.pack()
        self.display.pack()
        self.inputf.pack()
        self.send.pack()
        self.exit.pack()

    def Connect(self, host, port):
        try:
            Client.s = socket.socket()         
            #host = '127.0.0.1'
            #port = 8080                 
            Client.s.connect((host, port))     
            thread.start_new_thread(self.Recv, ())
        except socket.error as msg:
            print msg
        
    def Send(self):
        Client.sending = True
        #while True:
        try:
            print 'Ready to send'
            msg=self.inputf.get()
            #if msg=='Exit':
            #    Client.s.close()
                #break
            Client.s.send(msg)
            print 'Sent'
            
        except:
            print 'Error occured in send'
        Client.sending = False  

    def Recv(self):
        while not Client.sending:
            print 'Ready to receive'
            try:
                msg=Client.s.recv(1024)
                print 'Message received'
                self.display.config(text=msg)
                self.display.pack()
                print msg
            except:
                print 'Error occured in recv'
                break
        self.display.config(text='Connection dropped')
        self.display.pack()
        Client.s.close()
    
    def Exit(self):
        try:
            Client.sending=True
            Client.s.close()
        except:
            pass
        root.quit()

        
C=Client()
root.mainloop()
