from vidstream import CameraClient
from vidstream import StreamingServer

import threading

lock = threading.Lock() # Creating Lock System for multiple threading

host = "   " #Host's local IP address
port = 55555    #port//Avoid using the well known port like hhtp,https,ftp,ssh...

client = " " #Client's local IP address
port = 55555

receiver = StreamingServer(host, port)

transmitting_to = CameraClient(client, port)

def receiving():
    receiver.start_server()

def transmitting():
    transmitting_to.start_stream()

t1 = threading.Thread(target= receiving)
t2 = threading.Thread(target= transmitting)

lock.acquire()
t1.start()
lock.release()
t2.start()
t2.join()

while input("") != "STOP":
    continue

transmitting_to.stop_stream()
receiver.stop_server()


    


