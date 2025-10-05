import hashlib

from typing import Callable


# module end


def calc_hash(string: bytes, hash_type: str = "sha256"):
    return getattr(hashlib, hash_type)(string)


def get_hash_func(hash_type: str = "sha256") -> Callable[[bytes], hashlib._Hash]:
    return getattr(hashlib, hash_type)
