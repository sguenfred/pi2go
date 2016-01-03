# Pi2Go 'avoider sketch' - for the second episode of my robot tutorial series
# This program is fairly simple - it utilises the IR and ultrasonic sensors
# on the Pi2Go in order to sense obstacles and avoid them
# Created by Matthew Timmons-Brown and Simon Beal

#Fbenoit just added hooks for manual mode to recover robots in danger

import pi2go, time
import sys,termios,tty,select


# Here we set the speed to 40 out of 100 - feel free to change!
speed = 50

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def readkey():
    c1 = sys.stdin.read(1)
    if ord(c1) != 0x1b:
        return ord(c1)
    c2 = sys.stdin.read(1)
    if ord(c2) != 0x5b:
        return ord(c1)
    c3 = sys.stdin.read(1)
    return ord(c3)

old_settings = termios.tcgetattr(sys.stdin)
pi2go.init()

UP = 65
DOWN = 66
RIGHT = 67
LEFT = 68

SWITCHMODE=32
SPEEDUP=97
SPEEDDOWN=113

# Here is the main body of the program - a lot of while loops and ifs!
# In order to get your head around it go through the logical steps slowly!
manual=True
try:
  tty.setcbreak(sys.stdin.fileno())
  while True:
    if isData():
      key = readkey()
      if key == '\x1b':         # x1b is ESC
        pi2go.stop()
        break
      #print "key is %s or (%d)" % (key,key)
      if key == SWITCHMODE:
        pi2go.stop()
        if manual:
          print "going to auto mode"
          manual=False
        else:
          print "going to manual mode"
          manual=True
      if key== SPEEDUP:
        speed=min(100,speed+10)
        print "speed up to %d" % (speed)
      if key== SPEEDDOWN:
        speed=max(0,speed-10)
        print "speed down to %d" % (speed)
      if key == 'w' or key == UP:
        print "going to manual mode"
        manual=True
        pi2go.forward(speed)
        print 'Forward', speed
      elif key == 's' or key == DOWN:
        print "going to manual mode"
        manual=True
        pi2go.reverse(speed)
        print 'Backward', speed
      elif key == 'd' or key == RIGHT:
        print "going to manual mode"
        manual=True
        pi2go.spinRight(speed)
        print 'Spin Right', speed
      elif key == 'a' or key == LEFT:
        print "going to manual mode"
        manual=True
        pi2go.spinLeft(speed)
        print 'Spin Left', speed

    if not manual:    
      if pi2go.irLeft():
        while pi2go.irLeft():
          # While the left sensor detects something - spin right
          pi2go.spinRight(speed)
        pi2go.stop()
      if pi2go.irRight():
        while pi2go.irRight():
          # While the right sensor detects something - spin left
          pi2go.spinLeft(speed)
        pi2go.stop()
      while not (pi2go.irLeft() or pi2go.irRight()):
        if pi2go.getDistance() <= 0.3: # If the distance is less than 0.3, spin right for 1 second
          pi2go.spinRight(speed)
          time.sleep(1)
        else:
          pi2go.forward(speed)
      pi2go.stop()

finally: # Even if there was an error, cleanup
  pi2go.cleanup()
  termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

