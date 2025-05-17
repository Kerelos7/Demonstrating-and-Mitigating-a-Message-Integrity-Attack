import struct

# Constants for MD5
S = [
    7, 12, 17, 22] * 4 + [
    5, 9, 14, 20] * 4 + [
    4, 11, 16, 23] * 4 + [
    6, 10, 15, 21] * 4

K = [int(abs(__import__('math').sin(i + 1)) * 2**32) & 0xFFFFFFFF for i in range(64)]

def left_rotate(x, c):
    return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF

class MD5:
    def __init__(self):
        self.reset()

    def reset(self):
        self.A = 0x67452301
        self.B = 0xefcdab89
        self.C = 0x98badcfe
        self.D = 0x10325476
        self.buffer = b""
        self.count = 0  # in bits

    def set_state(self, A, B, C, D):
        self.A, self.B, self.C, self.D = A, B, C, D

    def set_message_length(self, length_bytes):
        self.count = length_bytes * 8  # Convert to bits

    def update(self, input_bytes):
        self.buffer += input_bytes
        self.count += len(input_bytes) * 8
        while len(self.buffer) >= 64:
            self._process_chunk(self.buffer[:64])
            self.buffer = self.buffer[64:]

    def _process_chunk(self, chunk):
        a, b, c, d = self.A, self.B, self.C, self.D
        M = struct.unpack('<16I', chunk)

        for i in range(64):
            if 0 <= i <= 15:
                f = (b & c) | (~b & d)
                g = i
            elif 16 <= i <= 31:
                f = (d & b) | (~d & c)
                g = (5 * i + 1) % 16
            elif 32 <= i <= 47:
                f = b ^ c ^ d
                g = (3 * i + 5) % 16
            elif 48 <= i <= 63:
                f = c ^ (b | ~d)
                g = (7 * i) % 16

            f = (f + a + K[i] + M[g]) & 0xFFFFFFFF
            a, d, c, b = d, c, b, (b + left_rotate(f, S[i])) & 0xFFFFFFFF

        self.A = (self.A + a) & 0xFFFFFFFF
        self.B = (self.B + b) & 0xFFFFFFFF
        self.C = (self.C + c) & 0xFFFFFFFF
        self.D = (self.D + d) & 0xFFFFFFFF

    def digest(self):
        padding = self._padding()
        self.update(padding)
        return struct.pack('<4I', self.A, self.B, self.C, self.D)

    def hexdigest(self):
        return self.digest().hex()

    def _padding(self):
        message_len = self.count
        padding = b'\x80'
        pad_len = (56 - ((message_len // 8 + 1) % 64)) % 64
        padding += b'\x00' * pad_len
        padding += struct.pack('<Q', message_len)
        return padding
