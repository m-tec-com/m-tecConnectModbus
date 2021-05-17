from mtecConnectModbus import mtecConnectModbus
pump = mtecConnectModbus("01");

def connect():
    #pump.serial_port = '/dev/cu.usbmodem1431201'
    pump.serial_port = 'COM3'
    pump.connect()
    
def stop():
    pump.stop()
    
def changeSpeed(newSpeed):
    pump.speed = int(newSpeed)
    
def updatedValue(newValue):
    print(newValue)
    newText = "Output: " + str(newValue/100) + "Hz"
    speedLabel.config(text=newText) 

def changeKeepAlive():
    if(keepAliveVar.get() == 1):
        print("active")
        pump.settings_keepAlive_active = True
    else:
        print("inactive")
        pump.settings_keepAlive_active = False        
    
    
import tkinter

master = tkinter.Tk()

connectButton = tkinter.Button(master, text="Connect", command=connect)
connectButton.pack()
stopButton = tkinter.Button(master, text="Stop", command=stop)
stopButton.pack()

slider = tkinter.Scale(master, from_=0, to=100, orient=tkinter.HORIZONTAL, command=changeSpeed, label="Input: ")
slider.pack()

speedLabel = tkinter.Label(master, text="Output: Hz")
speedLabel.pack()

keepAliveVar = tkinter.IntVar(value=1)
keepAlive = tkinter.Checkbutton(master, text='keepAlive',variable=keepAliveVar, onvalue=1, offvalue=0, command=changeKeepAlive)
keepAlive.pack()