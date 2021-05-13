from mtecConnectModbus import mtecConnectModbus as pump

def connect():
    pump.connect()
    
def stop():
    pump.stop()
    
def changeSpeed(newSpeed):
    pump.speed = newSpeed
    
def updatedValue(newValue):
    print(newValue)
    