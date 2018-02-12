from socket import *
import time


TEST_LCP_COMMANDS = [
    (0x12, 0x0),
    (0x20, 0x3, 0x000000),
    (0x20, 0x3, 0xAAAAAA),
    (0x20, 0x3, 0xBBBBBB),
    (0x20, 0x3, 0xFFFFFF),
    (0x13, 0x0),
]


s = socket(AF_INET, SOCK_STREAM)
s.bind(('', 9999))
s.listen(1)


try:
    while True:
        client, addr = s.accept()
        print('client: %s' % str(addr))
        for i in TEST_LCP_COMMANDS:
            print(i)
            data = i[0].to_bytes(1, byteorder='big')
            data += i[1].to_bytes(2, byteorder='big')
            if len(i) == 3:
                data += i[2].to_bytes(i[1], byteorder='big')
            print(data)
            time.sleep(1)
            client.send(data)
        client.close()
except:
    s.close()
