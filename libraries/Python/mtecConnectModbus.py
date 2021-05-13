class mtecConnectModbus:
    def __init__(self, frequencyInverterID = "01"):
        self.settings_frequencyInverterID = frequencyInverterID
        self.settings_keepAlive_command = "03FD000001"
        self.settings_keepAlive_interval = 250
        self.settings_keepAlive_callback = undefined
        self.settings_keepAlive_active = true
        self.settings_serial_baudRate = 19200
        self.settings_serial_dataBits = 8
        self.settings_serial_stopBits = 2
        self.settings_serial_parity = "none"
        self.settings_serial_flowControl = "none"
        self.settings_log = false
        self.temp_sendBuffer = []
        self.temp_valueBuffer = []
        self.temp_readBuffer = []
        self.temp_sendReady = false
        self.temp_lastSpeed = 0
        self.available = true # ToDo
        self.connected = false
        
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