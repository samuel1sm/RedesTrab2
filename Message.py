import io
from Utils import check_sum


# header
# ack : 1 byte
# cksum : 4 bytes
# path : 32 bytes
# data : 987
#
#
class Package:
    def __init__(self, ack: bytes, path: bytes, data: bytes, cksum: bytes = None):
        self.data = data
        self.ack = ack
        self.path = path

        self.cksum = check_sum(self.data + self.ack + self.path)

        self.previous_cksum = cksum

    def create_message(self) -> bytes:
        return self.ack + self.cksum + self.path + self.data

    def compare_chksums(self) -> bool:
        return self.cksum == self.previous_cksum

    @staticmethod
    def decode_message(message: bytes):
        ack = message[0:1]
        cksum = message[1:5]
        path = message[5:37]

        data = message[37:]

        return Package(ack, path, data, cksum)


if __name__ == '__main__':
    Package(b"asdasdsad", b"\1")
