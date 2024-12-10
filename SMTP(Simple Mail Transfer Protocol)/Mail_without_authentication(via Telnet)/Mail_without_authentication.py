import telnetlib
import socket
import threading
import time
from scapy.all import *


# E-posta mesajını parçalara ayırma fonksiyonu
def fragment_message(data, chunk_size=50):
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


# Paketleri farklı portlardan gönderme
def send_fragment(fragment, host, port):
    packet = IP(dst=host) / TCP(dport=port) / fragment
    send(packet)
    print(f"Fragment sent to {host}:{port} - Data: {fragment}")


# Sunucu tarafında paketleri dinleyip birleştirme
def receive_fragment(port, received_data):
    def packet_callback(pkt):
        if TCP in pkt and pkt[TCP].dport == port:
            received_data.append(pkt[TCP].payload.decode())
            print(f"Received data on port {port} - Data: {pkt[TCP].payload.decode()}")

    sniff(prn=packet_callback, filter=f"tcp port {port}", store=0)


# E-posta mesajı (örnek)
email_data = "Subject: Test E-posta Gönderimi\n\nMerhaba,\nBu bir test e-postasıdır. Lütfen dikkate almayın.\nTeşekkürler."
fragments = fragment_message(email_data)


# Verileri farklı portlardan göndermek
def send_email():
    target_host = "smtp.gmail.com"  # Gmail sunucusu
    ports = [25, 587, 465]  # Farklı portlar (genellikle Gmail SMTP portları)

    # E-posta içeriğini burada göndereceğiz
    for i, fragment in enumerate(fragments):
        port = ports[i % len(ports)]  # Her fragmanı farklı port üzerinden gönder
        send_fragment(fragment, target_host, port)
        time.sleep(1)  # Paketler arasında küçük bir gecikme


# Parçaları alıp birleştirme
received_data = []


def receive_email():
    threads = []
    ports = [25, 587, 465]

    # Her port için bir dinleme başlat
    for port in ports:
        thread = threading.Thread(target=receive_fragment, args=(port, received_data))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Verileri birleştir
    full_message = ''.join(received_data)
    print("Full message received:")
    print(full_message)


# Telnet ile Gmail SMTP sunucusuna bağlanma ve e-posta gönderme
def send_email_via_telnet():
    host = "smtp.gmail.com"
    port = 25  # Bu port genellikle açık olmayabilir, bu yüzden 587 veya 465 tercih edebilirsiniz.

    with telnetlib.Telnet(host, port) as tn:
        # Sunucudan gelen yanıtı okuma
        tn.read_until(b"\n")

        # HELO komutu ile sunucuya bağlanma
        tn.write(b"HELO gmail.com\n")
        tn.read_until(b"\n")

        # Gönderen e-posta adresi (MAIL FROM)
        tn.write(b"MAIL FROM:<sender@gmail.com>\n")
        tn.read_until(b"\n")

        # Alıcı e-posta adresi (RCPT TO)
        tn.write(b"RCPT TO:<vict@gmail.com>\n")
        tn.read_until(b"\n")

        # E-posta içeriği (DATA)
        tn.write(b"DATA\n")
        tn.read_until(b"\n")
        tn.write(b"Subject: Test \n")
        tn.write(b"\n")
        tn.write(b"Hello,\n")
        tn.write(b"Sexter.\n")
        tn.write(b"Morgan,\n")
        tn.write(b".\n")  # Mesaj bitişi
        tn.read_until(b"\n")

        # QUIT komutu ile bağlantıyı sonlandırma
        tn.write(b"QUIT\n")
        tn.read_until(b"\n")


# E-posta gönderme ve alma işlemleri
send_email_via_telnet()  # Telnet ile e-posta gönderme
send_email()  # Scapy ile e-posta gönderme (parçalara bölerek)
receive_email()  # E-posta alma (parçaları birleştirerek)
