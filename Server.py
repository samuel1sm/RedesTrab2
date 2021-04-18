import socket
import Message
from Utils import update_ack
import os


def handle_udp_recv(bytesAddressPair):
    address = bytesAddressPair[1]
    result = Message.Package.decode_message(bytesAddressPair[0])
    return address, result


localIP = "127.0.0.1"
localPort = 3306
bufferSize = 1024

ack = b"\0"

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    address, result = handle_udp_recv(bytesAddressPair)

    if result.ack == ack:
        result.data = b""
        new_message = result.create_message()
        UDPServerSocket.sendto(bytesAddressPair[0], address)
        continue

    while not result.compare_chksums():
        result.ack = ack
        result.data = b""
        new_message = result.create_message()

        UDPServerSocket.sendto(new_message, bytesAddressPair[1])

        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        address, result = handle_udp_recv(bytesAddressPair)

    path = result.path.decode().replace('\x00', '')
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(f"{path}", "ab") as f:
        f.write(result.data)

    ack = update_ack(ack)
    result.data = b""
    UDPServerSocket.sendto(bytesAddressPair[0], address)
