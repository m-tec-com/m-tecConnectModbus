class mtecConnectModbus:
    def __init__(self, frequencyConverterID = "01"):
        # ToDo
        print("init")
    
    def connect(self):
        # ToDo
        print("connect")
    
    def sendCommand(self, parameter, value):
        # ToDo
        print("sendCommand")
    
    @property
    def ready(self):
        # ToDo
        print("get ready")
    
    @ready.setter
    def ready(self, value):
        raise Exception("ready not setable")
    
    @property
    def frequency(self):
        # ToDo
        print("get frequency")
    
    @frequency.setter
    def frequency(self, value):
        # ToDo
        print("set frequency")
        
    @property
    def voltage(self):
        # ToDo
        print("get voltage")
    
    @voltage.setter
    def voltage(self, value):
        raise Exception("voltage not setable")
    
    @property
    def torque(self):
        # ToDo
        print("get torque")
    
    @torque.setter
    def torque(self, value):
        raise Exception("torque not setable")
    
    def start():
        # ToDo
        print("start")
    
    def startReverse():
        # ToDo
        print("startReverse")
    
    def stop():
        # ToDo
        print("stop")
    
    def ermergencyStop():
        # ToDo
        print("emergencyStop")
    
    @property
    def speed(self):
        raise Exception("speed not getable")
    
    @speed.setter
    def ready(self, value):
        # ToDo
        print("set speed")