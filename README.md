# mtecConnectModbus

## Supported Machines

The P20 connect and P50 connect use Modbus RTU as communication protocol. ([The duo-mix connect and SMP connect use OPC-UA instead.](https://github.com/m-tec-com/m-tecConnectOPC-UA))

## Connection
The modbus connection is using the same plug as ethernet but not the same protocol.

So you can use an ethernet cable to transport the data but you might have to convert the serial data via an adapter to something useful for your control unit. At m-tec we use the USB001ZKIT adapter from Toshiba as serial to USB adapter.

## Communication
We provide some [documentation](docs) of the communication protocol in the docs folder.

You might want to use our [JavaScript](libraries/JavaScript) or [Python](libraries/Python) libraries for an easier start.
