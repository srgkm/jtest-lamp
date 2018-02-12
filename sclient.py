from socket import *
import time


s = socket(AF_INET, SOCK_STREAM)
s.connect(('', 9999))

while True:
    resp = s.recv(1024)
    if not resp:
        break
    print(resp)

s.close()
