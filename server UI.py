import Tkinter as tk
import socket, thread

print 'Server'

root= tk.Tk()
root.title("Server")
root.geometry(('400x150'))

class Server(tk.Tk):
    
    c=''
    sending=False
    s=''
    
    def __init__(self):
        self.display=tk.Label(root, text='Received messages appear here')
        #tk.Label(root, text='Server').pack()
        self.inputf=tk.Entry(root)
        self.send=tk.Button(root, text='Send', command=self.Send)
        self.exit=tk.Button(root, text='Exit', command=self.Exit)
        self.placewidgets()
        self.startserver()

    def placewidgets(self):
        self.display.pack()
        self.inputf.pack()
        self.send.pack()
        self.exit.pack()

        
    def startserver(self):
        Server.s=socket.socket()
        #host = '127.0.0.1'
        #port = 8080
        host=socket.gethostname()
        port=12345
        tk.Label(root, text=str(host+':'+str(port))).pack()
        Server.s.bind((host, port))        
        Server.s.listen(5)
        Server.sending=False
        thread.start_new_thread(self.Recv, ())

    def Recv(self):
        while not Server.sending:
            Server.c, addr = Server.s.accept()     
            print addr
            print 'Got connection from', addr

            while not Server.sending:
                try:
                    print 'Ready to receive'
                    data=Server.c.recv(1024)
                    print 'Message received'
                    self.display.config(text=data)
                    self.display.pack()
                    if data!='':
                        print data
             
                    #if data == 'Exit':
                    #    Server.sending = True
                    #    Server.c.close()
                    #    break
                    #if data=='':
                    #    del data
                except:
                    print 'Error occured in recv'
                    break
            
            
        Server.s.close()

    def Send(self):
        Server.sending=True
        try:
            print 'Ready to send'
            msg=self.inputf.get()
            Server.c.send(msg)
            print 'Sent'
            #Server.c.close()
        except:
            print 'Error occured in send'
        Server.sending=False
        #thread.start_new_thread(self.Recv, ())

    def Exit(self):
        try:
            Server.sending=True
            Server.c.close()
            Server.s.close()
        except:
            pass
        root.quit()

S=Server()
root.mainloop()
