import hmac
import struct

import time

from _hydrogenlib_core.hash import get_hash_func


class TOTP:
    def __init__(self, secret_key, digits=6, period=30, hash_method: str = 'sha256'):
        self.secret_key = secret_key
        self.digits = digits
        self.period = period
        self.hash_method = get_hash_func(hash_method)

    def generate(self, timestamp=None):
        if timestamp is None:
            timestamp = int(time.time())

        timestamp = timestamp // self.period
        ts_bytes = struct.pack('>Q', timestamp)
        hash_value = self.hash_method(ts_bytes + self.secret_key).digest()
        return int.from_bytes(hash_value[-4:], 'big') % 10 ** self.digits


class HOTP(TOTP):
    def generate(self, timestamp=None):
        if timestamp is None:
            timestamp = int(time.time())

        timestamp //= self.period
        ts_bytes = struct.pack('>Q',  timestamp)
        hash_value = hmac.new(self.secret_key, ts_bytes, self.hash_method)
        return int.from_bytes(hash_value.digest(), 'big') % 10 ** self.digits
