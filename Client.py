import socket
import Message
from Utils import update_ack

serverAddressPort = ("127.0.0.1", 3306)
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

file_to_read = "img.png"
file_to_create = "download/img1.png"

path_initial = str.encode(file_to_create)
path = bytearray()

for _ in range(32 - len(path_initial)):
    path.extend(b'\0')
path.extend(path_initial)

ack = b"\1"

bufferSize = 1024
data_size = 987
UDPClientSocket.settimeout(5.0)

with open(file_to_read, "rb") as f:
    data = f.read(data_size)
    while data:
        package = Message.Package(ack, path, data)

        message = package.create_message()

        send_next_message = False

        while not send_next_message:
            while True:
                try:
                    UDPClientSocket.sendto(message, serverAddressPort)

                    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
                    break
                except socket.timeout:
                    continue

            message = msgFromServer[0]
            address = msgFromServer[1]
            result = Message.Package.decode_message(message)

            send_next_message = ack == result.ack and result.compare_chksums()

        ack = update_ack(ack)
        data = f.read(data_size)

msg = "Message from Server {}".format(msgFromServer[0])
print(msg)
