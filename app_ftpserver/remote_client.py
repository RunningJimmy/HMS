
import socket
ip_port = ('10.7.103.205',9000)
sk = socket.socket()
sk.connect(ip_port)

while True:
    raw = input('>> ').strip()
    sk.send(bytes(raw,'utf8'))
    msg = sk.recv(1024)
    print(str(msg,'utf8'))
sk.close()