The Use of TCP In vidstream
Camera Client (CameraClient): The CameraClient object sends video data over a TCP connection. This data is transferred by converting to JPEG format.
Server (StreamingServer): The server side again receives and processes incoming video packets using a TCP connection.
Why Is UDP Not Used?
Some streaming protocols use UDP for applications such as live streaming, for example. But:

UDP is fast but not reliable; packets may get lost or arrive unordered.
in applications that require synchronization and quality, such as vidstream, it is more important to ensure reliability rather than tolerate data loss.
That's why vidstream prefers TCP.
+--------------------------------------+
Receiver.py and Transmitter.py is just for understanding the library and methods
Camera_Chat.py is for synchronized camera chat.