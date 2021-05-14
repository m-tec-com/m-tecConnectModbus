from mtecConnectModbus import mtecConnectModbus
pump = mtecConnectModbus("01");

def connect():
    pump.serial_port = '/dev/cu.usbmodem1431201'
    pump.connect()
    
def stop():
    pump.stop()
    
def changeSpeed(newSpeed):
    pump.speed = newSpeed
    
def updatedValue(newValue):
    print(newValue)
    





