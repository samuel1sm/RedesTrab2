import zlib


def check_sum(data: bytes):
    return (zlib.crc32(data) & 0xffffffff).to_bytes(4, "big")


def update_ack(ack: bytes) -> bytes:
    return b"\1" if ack == b"\0" else b"\0"
