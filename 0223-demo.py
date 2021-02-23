import socket
import os
import pika
import _thread
import time
from datetime import datetime
import threading
from threading import Timer,Thread,Event

# os.system('fuser -k 1234/tcp')
ServerSideSocket = socket.socket()
host = '192.168.1.8'
port = 1234
ThreadCount = 0

credentials = pika.PlainCredentials('avani', 'avani')

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(20)


class perpetualTimer():

   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

# initial rabbit connect
def initial_rb_connect():
    try:
        rb_connnection = pika.BlockingConnection(
            pika.ConnectionParameters(
                "192.168.1.3",
                5672,
                "/",
                credentials,
                heartbeat=0,
                socket_timeout=1,
            )
        )

        return rb_connnection
    except:
        return False

def try_rb_connect():
    try:
        rb_connnection = pika.BlockingConnection(
            pika.ConnectionParameters(
                "192.168.1.8",
                # "localhost",
                5672,
                "/",
                credentials,
                heartbeat_interval=0,
                blocked_connection_timeout=1,
            )
        )

        return rb_connnection
    except:
        return False
        
def process_data(tcp_connnection):
    global channel
    while True:
        data = tcp_connnection.recv(1024).decode('latin-1')
        err_data = time.strftime("%H:%M:%S", time.localtime()) + " - " + data
        file = open("data-test.txt", "a")
        if not data:
            break        
        print(err_data)
        
        rb_connect = initial_rb_connect()

        if rb_connect == False:
            print("Connect fail !")
            file.write(err_data)
        else:            
            print("Connect OK, send : ", data)
            channel = rb_connect.channel()
            channel.queue_declare(queue="data")
            channel.basic_publish(exchange="", routing_key="data", body=data)


def scan_data():
    f = open("data-test.txt", "r")
    rb_connected = try_rb_connect()
    rb_connect = initial_rb_connect()

    if rb_connect == False:
        initial_rb_connect()
    else:            
        print("Reconnect OK, send : ", data)
        channel = rb_connect.channel()
        channel.queue_declare(queue="err-data")
        channel.basic_publish(exchange="", routing_key="err-data", body=err-data)


def scan():
    # time.sleep(10)
    # global channel
    # global connection
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                "192.168.1.8",
                5672,
                "/",
                credentials,
                heartbeat=0,
                # socket_timeout=1,
            ))
        channel = connection.channel()
        channel.queue_declare(queue='err-data')
        
        a_file = open('data-test.txt', 'r')
        Lines = a_file.readlines()
        a_file.close()
        

        time1 = time.ctime()

        count = 0
        # Strips the newline character
        try:
            new_file = open("data-test.txt", "w")
            for line in Lines:
                time2 = time.ctime()
                # if line != "\n" and ((time2-time1)<60):
                if line != "\n":
                    del_line = line
                    count += 1    
                    channel.basic_publish(exchange='', routing_key='err-data', body=line)
                    print("Line{}: {}".format(count, line.strip()))
                    # if line.strip("\n") != del_line:
                    #     # print("Delete line: ", del_line)
                    #     Delete "line" from new_file
                    #     new_file.write(line)
                    del Lines[0]
        except:
            connection.close()
    
    except:
        pass        

    # time.sleep(delay)

def Main():
    try:
        while True:
            Client, address = ServerSideSocket.accept()
            _thread.start_new_thread(process_data, (Client, ))
            
            # time.sleep(1)
            # # print(i)
            # _thread.start_new_thread(scan,())
            t = perpetualTimer(20,scan)
            t.start()
    except:        
        print("Lỗi hàm main")
        ServerSideSocket.close()

if __name__ == '__main__':
    Main()