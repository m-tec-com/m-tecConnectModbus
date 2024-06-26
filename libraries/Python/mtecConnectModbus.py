import serial
import math
import time
from threading import Timer

class mtecConnectModbus:
    def __init__(self, frequencyInverterID = "01"):
        self.settings_frequencyInverterID = frequencyInverterID
        self.settings_keepAlive_command = "03FD000001"
        self.settings_keepAlive_interval = 250
        self.settings_keepAlive_callback = None
        self.settings_keepAlive_active = True
        self.settings_keepAlive_loop = None
        self.settings_serial_baudRate = 19200
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
    
    def read(self, command):
        return self.sendCommand("03" + command, 1)
    
    def write(self, command, value):
        return self.sendCommand("06" + command, value)

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
            #self.waitForResponse()
            self.temp_sendReady = True
            if len(self.temp_valueBuffer) > 0:
                return self.temp_valueBuffer.pop()
    
    def keepAlive(self):
        self.print("f: keepAlive")
        if callable(self.settings_keepAlive_command):
            command = self.settings_keepAlive_command()
        else:
            command = self.settings_keepAlive_command
        value = self.sendHexCommand(self.settings_frequencyInverterID + command)
        if callable(self.settings_keepAlive_callback):
            self.settings_keepAlive_callback(value)
    
    def send(self, command):
        self.temp_sendReady = False
        self.print("s: " + command)
        #self.serial.write(command.encode())
        self.serial.write(bytes.fromhex(command))
        self.waitForResponse()
        if self.settings_keepAlive_active:
            if hasattr(self.settings_keepAlive_loop, 'cancel') and callable(self.settings_keepAlive_loop.cancel):
                self.settings_keepAlive_loop.cancel()
            self.settings_keepAlive_loop = Timer(self.settings_keepAlive_interval / 1000, self.keepAlive)
            self.settings_keepAlive_loop.start()
        
    def waitForResponse(self):
        command = ""
        timeout = time.time_ns() + (200 * 1000 * 1000)  #200ms
        while True:
            if self.serial.inWaiting() >= 2:
                break
            if time.time_ns() > timeout:
                self.print("escape")
                self.print(self.serial.read(self.serial.inWaiting()))
                return False
        message_fcID = int.from_bytes(self.serial.read(1), "little")
        command += self.int2hex(message_fcID,2)
        message_type = int.from_bytes(self.serial.read(1), "little")
        command += self.int2hex(message_type,2)
        
        completeDataLength = 0
        if message_type == 3: # Type: read
            message_length = int.from_bytes(self.serial.read(1), "little")
            command += self.int2hex(message_length, 2)
            completeDataLength = 3 + message_length + 2 - 3# ID, Type, Length, <Length>, checksum, checksum - alreadyRead
        elif message_type == 6: # Type: send
            completeDataLength = 8 - 2 # 8 - alreadyRead

        while True:
            if self.serial.inWaiting() >= completeDataLength:
                break
            if time.time_ns() > timeout:
                self.print("escape")
                self.print(self.serial.read(self.serial.inWaiting()))
                return False    
        
        isError = False
        if message_type == 3: # Type: read
            message_value = 0
            for i in range(message_length):
                message_value *= 256
                m = int.from_bytes(self.serial.read(1), "little")
                message_value += m
                command += self.int2hex(m, 2)
        elif message_type == 6: # Type: send
            message_param = self.int2hex(int.from_bytes(self.serial.read(1), "little"), 2) + self.int2hex(int.from_bytes(self.serial.read(1), "little"), 2)
            command += message_param
            message_value0 = int.from_bytes(self.serial.read(1), "little")
            message_value1 = int.from_bytes(self.serial.read(1), "little")
            message_value = message_value0 * 256 + message_value1
            command += self.int2hex(message_value, 4)
        elif message_type == 0x86:
            message_value = int.from_bytes(self.serial.read(1), "little")
            command += self.int2hex(message_value, 2)
            isError = True
        message_crc = self.int2hex(int.from_bytes(self.serial.read(1), "little"), 2) + self.int2hex(int.from_bytes(self.serial.read(1), "little"), 2)

        if self.calcCRC(command) != message_crc:
            isError = True
            # ToDo
            pass
        else:
            if isError:
                # ToDo
                self.print("error")
                pass
            else:
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
            crc ^= buffer[pos]
            for k in range(8):
                i = 8 - k
                if ((crc & 0x0001) != 0):
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return self.int2hex((crc % 256) * 256 + math.floor(crc / 256),4)
    
    def print(self, content):
        if self.settings_log:
            print(content)

    @property
    def ready(self):
        switches = self.read("FD06")
        return ((switches % 32) - (switches % 16) != 0)
    
    @ready.setter
    def ready(self, value):
        raise Exception("ready not setable")
    
    @property
    def frequency(self):
        return self.read("FD00") / 100
    
    @frequency.setter
    def frequency(self, value):
        return self.write("FA01", value * 100)
        
    @property
    def voltage(self):
        return self.read("FD05") / 100
    
    @voltage.setter
    def voltage(self, value):
        raise Exception("voltage not setable")
    
    @property
    def current(self):
        return self.read("FD03") / 100
    
    @current.setter
    def current(self, value):
        raise Exception("current not setable")
    
    @property
    def torque(self):
        return self.read("FD18") / 100
    
    @torque.setter
    def torque(self, value):
        raise Exception("torque not setable")
    
    def start(self):
        return self.write("FA00", 0xC400)
    
    def startReverse(self):
        return self.write("FA00", 0xC600)
    
    def stop(self):
        return self.write("FA00", 0x0000)
    
    def ermergencyStop(self):
        return self.write("FA00", 0x1000)
    
    @property
    def speed(self):
        raise Exception("speed not getable")
    
    @speed.setter
    def speed(self, value):
        if value != self.temp_lastSpeed:
            if value == 0:
                self.stop()
            else:
                if value < 0 and not self.temp_lastSpeed < 0:
                    self.startReverse()
                elif value > 0 and  not self.temp_lastSpeed > 0:
                    self.start()
                self.frequency = abs(value)
        self.temp_lastSpeed = value
