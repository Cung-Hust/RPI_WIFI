import socket
import time

HOST = "192.168.1.8"
PORT = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
print("connecting to %s port " + str(server_address))
s.connect(server_address)

try:
    while True:
        # msg = input('Client: ')
        while True:
            msg = ":D0004503000000000000000000000000111\r\n"
            s.sendall(bytes(msg, "utf8"))
            time.sleep(1)
            print(msg)
        # if msg == "quit":
        #     break

        # data = s.recv(1024)
        # print('Server: ', data.decode("utf8"))
finally:
    s.close()