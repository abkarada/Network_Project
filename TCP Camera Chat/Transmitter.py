from vidstream import CameraClient
from vidstream import StreamingServer

import threading
import time 


sending = CameraClient('192.168.234.1', 9999)



t2 = threading.Thread(target= sending.start_stream)
t2.start()
t2.join()


while input("") != "STOP":
    continue

sending.stop_stream()
