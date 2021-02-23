import socket
import os
import pika
import _thread
import time

# os.system('fuser -k 1234/tcp')
ServerSideSocket = socket.socket()
host = '192.168.1.10'
port = 1234
ThreadCount = 0

credentials = pika.PlainCredentials('avani', 'avani')

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(20)

def multi_threaded_client(connection):
    while True:
        data = connection.recv(38)
        if not data:
            break
        print(data)
        # try:
        #Connected = pika.BlockingConnection(
         #   pika.ConnectionParameters('192.168.1.21', 5672, '/', credentials))
        #channel = Connected.channel()
        #channel.queue_declare(queue='Pi1')
        #channel.basic_publish(exchange='', routing_key='Pi1', body= data)
while True:
    try:
        while True:
            Client, address = ServerSideSocket.accept()
            _thread.start_new_thread(multi_threaded_client, (Client, ))
    finally:
        ServerSideSocket.close()
