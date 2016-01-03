# Pi2Go basic motor sketch - for the first episode of my robot tutorial series.
# In truth this program is very simple - the parts where it captures key presses is the daunting bit.
# Try to work through it slowly and you'll soon understand!

# Use the arrow keys to control the direction of the Pi2Go and use the 'greater than' and 'less than'
# keys to edit the speed!

import pi2go, time

# Reading a button press from your keyboard, don't worry about this too much!
import sys
import tty
import termios
import curses
import curses.textpad
import time

stdscr = curses.initscr()
from _socket import *
import thread

def displayStatus():
    left=pi2go.irLeft()
    right=pi2go.irRight()
    leftLine=pi2go.irLeftLine()
    rightLine=pi2go.irRightLine()
    distance=pi2go.getDistance()
    myscreen.addstr(2,40,"sonar          "+str(distance))
    myscreen.addstr(4,40,"left sensor    "+str(left))
    myscreen.addstr(5,40,"right sensor   "+str(right))
    myscreen.addstr(6,40,"leftIR sensor  "+str(leftLine))
    myscreen.addstr(7,40,"rightRI sensor "+str(rightLine))
    myscreen.refresh()
        

class robotMove():
    
    def left(self):
        print "moving left"
    def right(self):
        print "moving right"
    def back(self):
        print "moving back"
    def forward(self):
        print "moving forward"
    def help(self):
        print "use qzds for control"
        print "h for help"
        print "r for status"
        print "m for quit"
    def status(self):
        print "status asked"
        
class robotDebug():
    def left(self):
        print "moving left"
    def right(self):
        print "moving right"
    def back(self):
        print "moving back"
    def forward(self):
        print "moving forward"
    def help(self):
        print "use qzds for control"
        print "h for help"
        print "r for status"
        print "m for quit"
    def status(self):
        print "status asked"
        
class myserver():
    def __init__(self,name="myserver",address="0.0.0.0",port=2222):
        self.serverName=name
        self.address=address
        self.port=port
        self.nbrconnexion=0
        self.Bstop=False
        self.Cstop=False
        self.rmove=robotDebug()
        
    def listen(self):
        while True:
            connexion, new_client= self.socket.accept()
            print "%d connection from %s:%d " % (self.nbrconnexion,new_client[0],new_client[1])
            thread.start_new_thread(self.parser,(connexion,))
            self.nbrconnexion +=1
            
    def quit(self):
        self.Cstop=True
    def parser(self,connexion):  
        #thread.start_new_thread(self.worker, (connexion,))
        retour=""
        switcher = {
                'q': self.rmove.left,
                'z': self.rmove.forward,
                'd': self.rmove.right,
                's': self.rmove.back,
                'r': self.rmove.status,
                'h': self.rmove.help,
                'm': self.quit
            }
        while not self.Cstop:
            print "waiting for char"
            retour=connexion.recv(1)
            if retour in switcher.keys():
                switcher[retour]()


    def displayStatus():
        myscreen.addstr(40,2,"ligne 1")
        myscreen.addstr(40,3,"ligne 2")
                    
    
    def start(self):
        self.socket=socket(AF_INET,SOCK_STREAM)
        self.addr=(self.address,self.port)
        self.socket.bind(self.addr)
        self.socket.listen(5)
        self.id=thread.start_new_thread(self.listen,())
        while True:
	    time.sleep(1)
	    displayStatus()
        #test=raw_input("q for quit")
        #if test=="q":
        #    return()
        #self.socket.close()
        
        
    def stopserver(self):
        self.Bstop=True
        
        
hostname=gethostname()
print "Launched on "+hostname
if hostname=="majordomo":
    pi2go.init()
    myscreen=curses.initscr()
    myscreen.border(1)
    myscreen.refresh()
    myscreen.addstr(2,2,"ServerRobot on %s" % (hostname))
    c=myserver(name="robot")
else:
    c=myserver(name="test")
    print "lauching in test mode"
c.start()
myscreen.getch()
pi2go.cleanup()
curses.endwin()
