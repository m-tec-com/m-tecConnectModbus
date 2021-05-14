import serial
import math

class mtecConnectModbus:
    def __init__(self, frequencyInverterID = "01"):
        self.settings_frequencyInverterID = frequencyInverterID
        self.settings_keepAlive_command = "03FD000001"
        self.settings_keepAlive_interval = 250
        self.settings_keepAlive_callback = None
        self.settings_keepAlive_active = True
        #self.settings_serial_baudRate = 19200
        self.settings_serial_baudRate = 9600
        self.settings_serial_dataBits = serial.EIGHTBITS
        self.settings_serial_stopBits = serial.STOPBITS_TWO
        self.settings_serial_parity = serial.PARITY_NONE
        self.settings_log = False
        self.temp_sendBuffer = []
        self.temp_valueBuffer = []
        self.temp_readBuffer = []
        self.temp_sendReady = False
        self.temp_lastSpeed = 0
        self.available = True # ToDo
        self.connected = False
    
    def connect(self):
        self.serial = serial.Serial(baudrate=self.settings_serial_baudRate, parity=self.settings_serial_parity,stopbits=self.settings_serial_stopBits,bytesize=self.settings_serial_dataBits,port=self.serial_port)
    
    def sendCommand(self, parameter, value):
        data = self.settings_frequencyInverterID + parameter + value
        crc = self.calcCRC(data)
        command = data + crc
        self.sendHex(command.encode())
        
    def sendHex(self, command):
        self.serial.write(command.encode());
        
    def waitForResponse(self):
        print("waitForResponse")
        
    def calcCRC(self, command):
        buffer = bytearray.fromhex(command)
        crc = 0xFFFF
        for pos in range(len(buffer)):
            crc ^= buffer[pos];
            for k in range(9):
                i = 8 - k
                if ((crc & 0x0001) != 0):
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1;
        crcstr = hex((crc % 256) * 256 + math.floor(crc / 256))[2:]
        while (len(crcstr) < 4):
            crcstr = "0" + crcstr
        return crcstr.upper()
    
   















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
        