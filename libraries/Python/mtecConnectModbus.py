import serial
import math
import time

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
        self.connected = True
        self.temp_sendReady = True
    
    def sendCommand(self, parameter, value):
        return self.sendHexCommand(self.settings_frequencyInverterID + parameter + self.int2hex(value,4))
        
    def sendHexCommand(self, data):
        crc = self.calcCRC(data)
        command = data + crc
        self.temp_sendBuffer.append(command)
        return self.sendHex()
        
    def sendHex(self):
        if self.temp_sendReady and len(self.temp_sendBuffer) > 0:
            self.send(self.temp_sendBuffer.pop())
            self.waitForResponse()
            self.temp_sendReady = True
            if len(self.temp_valueBuffer) > 0:
                return self.temp_valueBuffer.pop()
        
    def send(self, command):
        # ToDo
        self.temp_sendReady = False
        self.serial.write(command.encode())
        
    def waitForResponse(self):
        command = "";
        
        timeout = time.time() + 2
        while True:
            if self.serial.inWaiting() >= 3*2:
                break
            if time.time() > timeout:
                self.serial.read(self.serial.inWaiting())
                return False
        message_fcID = int(self.serial.read(2), 16)
        command += self.int2hex(message_fcID,2)
        message_type = int(self.serial.read(2), 16)
        command += self.int2hex(message_type,2)
        
        completeDataLength = 0
        if message_type == 3: # Type: read
            message_length = int(self.serial.read(2), 16)
            command += self.int2hex(message_length, 2)
            completeDataLength = 3 + message_length + 2 - 3# ID, Type, Length, <Length>, checksum, checksum - alreadyRead
        elif message_type == 6: # Type: send
            completeDataLength = 8 - 2 # 8 - alreadyRead
            
        while True:
            if self.serial.inWaiting() >= completeDataLength*2:
                break
            if time.time() > timeout:
                self.serial.read(self.serial.inWaiting())
                return False    
        
        if message_type == 3: # Type: read
            message_value = 0
            for i in range(message_length):
                message_value *= 256
                m = int(self.serial.read(2), 16)
                message_value += m
                command += self.int2hex(m, 2)
        elif message_type == 6: # Type: send
            message_param = self.int2hex(int(self.serial.read(4), 16), 4)
            command += message_param
            message_value = int(self.serial.read(4), 16)
            command += self.int2hex(message_value, 4)
        message_crc = self.int2hex(int(self.serial.read(4), 16), 4)
        
        if self.calcCRC(command) != message_crc:
            # ToDo: bad CRC
            print("bad crc")
        
        self.temp_valueBuffer.append(message_value)
        self.temp_sendReady = True
        return True
        
        
    def int2hex(self, value, length):
        s = hex(value)[2:]
        while (len(s) < length):
            s = "0" + s
        return s.upper()
            
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
        return self.int2hex((crc % 256) * 256 + math.floor(crc / 256),4)

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
        