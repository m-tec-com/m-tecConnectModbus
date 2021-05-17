> :warning: &nbsp; This library is not completely tested

&nbsp;

# Usage

> :warning: &nbsp; [pyserial](https://github.com/pyserial/pyserial) has to be installed
> use `pip install pyserial`

&nbsp;

## Minimal init

```python
from mtecConnectModbus import mtecConnectModbus
pump = mtecConnectModbus("01");

def connect():
    #pump.serial_port = '/dev/cu.usbmodem1431201'
    pump.serial_port = 'COM3'
    pump.connect()
    
def stop():
    pump.speed = 0
    
def changeSpeed(newSpeed):
    pump.speed = newSpeed
```

&nbsp;

## Documentation

### :wrench: &nbsp; :boom: &nbsp; constructor

Creates the Object to use the library.

```python
from mtecConnectModbus import mtecConnectModbus
pump = mtecConnectModbus("01");
```

result:
* mtecConnectModbus, conatins everything used to communicate via modbus

&nbsp;

### :wrench: &nbsp; :electric_plug: &nbsp; connect

Connects to the serial converter.

```python
connected = pump.connect()
```

result:
* bool, connection to serial interface sucessful?

&nbsp;

### :gear: &nbsp; :arrows_counterclockwise: &nbsp; keep alive

> :memo: &nbsp; While the pump is running, a valid command has to be sent at least every second

If activated, the keep alive feature sends a command some time (interval) after the last command.

This feature can be tweaked in the settings:

* bool `pump.settings_keepAlive_active`, if keep alive feature is enabled, default: true
* int `pump.settings_keepAlive_interval`, interval after which the command is sent (in ms), default: 250
* string (or function with return string) `pump.settings.keepAlive.command` (length: 10), action number (2) + parameter number (4) + value (4), default: "03FD000001"
* function `pump.settings_keepAlive_callback`, gets called with return value as parameter, optional

&nbsp;

### :wrench: &nbsp; :arrow_forward: &nbsp; start & stop

Starts or stops the pump (target frequency has to be set)

```python
# target frequency has to be set
pump.start()         # starts the pump
pump.startReverse()  # starts the pump in reverse
pump.stop()          # stops the pump
```

&nbsp;

### :pencil2: &nbsp; :timer_clock: &nbsp; set frequency

Sets the target frequency

```python
pump.frequency = frequency
```

parameters:
* float, positive (resolution: 0.01), target frequency in Hz

&nbsp;

### :mag: &nbsp; :timer_clock: &nbsp; get frequency

Gets the actual frequency

```python
f = pump.frequency
```

result:
* float, positive (resolution: 0.01), actual frequency in Hz

&nbsp;

### :pencil2: &nbsp; :fast_forward: &nbsp; set speed

Starts (or stops) the pump in the desired direction

> :warning: &nbsp; Do not switch between `set frequency` and `set speed`

```python
pump.speed = speed
```

parameters:
* float, negative to reverse (resolution: 0.01), target frequency

&nbsp;

### :mag: &nbsp; :vertical_traffic_light: &nbsp; get ready

Gets the readiness of the machine (on)

```python
f = pump.ready
```

result:
* bool, machine is ready for operation

&nbsp;

### :mag: &nbsp; :zap: &nbsp; get voltage

Gets the actual output voltage

```python
f = pump.voltage
```

result:
* float, positive (resolution: 0.01), actual voltage in % of voltage rating

&nbsp;

### :mag: &nbsp; :bulb: &nbsp; get current

Gets the actual output current

```python
f = pump.current
```

result:
* float, positive (resolution: 0.01), actual voltage in % of current rating

&nbsp;

### :mag: &nbsp; :muscle: &nbsp; get torque

Gets the actual torque

```python
f = pump.torque
```

result:
* float, positive (resolution: 0.01), actual voltage in % of torque rating

&nbsp;

### :wrench: &nbsp; :hash: &nbsp; send custom command

Sends custom command to inverter

```python
answer = pump.sendCommand(parameter, value)
```

parameters:
* string (length: 6), action number (2) + parameter number (4), example: "03FD00"
* int, value

result:
* int, answer value (equals input value if write command)

&nbsp;
