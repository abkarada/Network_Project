from vidstream import CameraClient
from vidstream import StreamingServer

import threading


receiving = StreamingServer('192.168.234.1', 9999)
t1 = threading.Thread(target= receiving.start_server)
t1.start()
t1.join()

while input("") != "STOP":
    continue

receiving.stop_server()