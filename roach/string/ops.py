# Copyright (C) 2018 Jurriaan Bremer.
# This file is part of Roach - https://github.com/jbremer/roach.
# See the file 'docs/LICENSE.txt' for copying permission.

from builtins import range
import base64
import binascii

def asciiz(s):
    return s.split(b"\x00")[0]

def hex(s):
    return binascii.hexlify(s)

def unhex(s):
    return binascii.unhexlify(s)

def uleb128(s):
    ret = 0
    for idx in range(len(s)):
        if isinstance(s[idx], str):
            ret += (ord(s[idx]) & 0x7f) << (idx*7)
        else:
            ret += (s[idx] & 0x7f) << (idx*7)
        if s[idx] < 0x80:
            break
    return idx+1, ret

class Base64(object):
    def encode(self, s):
        return base64.b64encode(s)

    def decode(self, s):
        return base64.b64decode(s)

    __call__ = decode

class Padding(object):
    def __init__(self, style):
        self.style = style

    @staticmethod
    def null(s, block_size):
        return Padding("null").pad(s, block_size)

    def pad(self, s, block_size):
        length = block_size - len(s) % block_size
        padding = None
        if length == block_size:
            padding = b""
        elif self.style == "pkcs7":
            padding = b"%c" % length * length
        elif self.style == "null":
            padding = b"\x00" * length
        return s + padding

    __call__ = pkcs7 = pad

class Unpadding(object):
    def __init__(self, style):
        self.style = style

    def unpad(self, s):
        if isinstance(s, str):
            count = ord(s[-1]) if s else 0
        else:
            count = s[-1] if s else 0
        if self.style == "pkcs7" and s[-count:] == b"\x03" * count:
            return s[:-count]
        return s

    __call__ = pkcs7 = unpad
