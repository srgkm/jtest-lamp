import asyncio
import struct
import sys


def _bytes_to_int(data):
    _bytes = struct.unpack('>{}s'.format(len(data)), data)[0]
    return int.from_bytes(_bytes, byteorder='big')


class LampControlProtocol(asyncio.Protocol):
    def __init__(self, loop, host, port):
        self.loop = loop
        self.host = host
        self.port = port
        self.loop.create_task(self.connect())
        self.on = False
        self.color = 0x000000

    def connection_made(self, transport):
        print('Connection made')

    def data_received(self, data):
        for tag, value in self.parse_command(data):
            self.handle_command(tag, value)

    def connection_lost(self, exc):
        print('Connection lost')
        self.loop.create_task(self.connect())

    def parse_command(self, data):
        # http://code.activestate.com/recipes/533137-simple-tlv-parser/
        while data:
            try:
                tag = _bytes_to_int(data[0:1])
                length = _bytes_to_int(data[1:3])
                if length:
                    value = _bytes_to_int(data[3:(3 + length)])
                else:
                    value = None
                data = data[(3 + length):]
                yield tag, value
            except Exception as err:
                print(err)

    def handle_command(self, tag, value):
        COMMANDS = {
            0x12: self.handle_command_on,
            0x13: self.handle_command_off,
            0x20: self.handle_command_change_color,
        }
        if tag in COMMANDS:
            COMMANDS[tag](value)

    def handle_command_on(self, value):
        self.on = True
        print('LAMP ON', '💡')

    def handle_command_off(self, value):
        self.on = False
        print('LAMP OFF')

    def handle_command_change_color(self, value):
        self.color = value
        print('COLOR: ', hex(value))

    async def connect(self):
        while True:
            try:
                await self.loop.create_connection(lambda: self, self.host, self.port)
            except Exception as err:
                print(err)
                print('Reconnect in 1 seconds...')
                await asyncio.sleep(1)
            else:
                break


if __name__ == '__main__':
    if len(sys.argv) == 3:
        _, host, port = sys.argv
    else:
        host, port = '127.0.0.1', 9999
    loop = asyncio.get_event_loop()
    LampControlProtocol(loop, host, port)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        # TODO: How to close socket?
        loop.stop()
        print('Do cleanup')
    finally:
        loop.close()
