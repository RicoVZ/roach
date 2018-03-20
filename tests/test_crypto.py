# Copyright (C) 2018 Jurriaan Bremer.
# This file is part of Roach - https://github.com/jbremer/roach.
# See the file 'docs/LICENSE.txt' for copying permission.

from roach.crypto.aes import AES
from roach import aes, rc4

def test_aes128cbc():
    assert AES("A"*16, "B"*16).decrypt("C"*16) == (
        "\x0b\xd4\x18\xa6\xf7\xbd\x1a\xff\x16\x1f\xd1A\xd4\xbe5\x9b"
    )

def test_short_aes():
    # Note that ECB doesn't use the IV.
    assert aes.ecb.decrypt("A"*16, "B"*16, "C"*32) == (
        "I\x96Z\xe4\xb5\xffX\xbdT]\x93\x03\x96\xfcw\xd9"
        "I\x96Z\xe4\xb5\xffX\xbdT]\x93\x03\x96\xfcw\xd9"
    )
    assert aes.ecb.decrypt("A"*16, data="C"*32) == (
        "I\x96Z\xe4\xb5\xffX\xbdT]\x93\x03\x96\xfcw\xd9"
        "I\x96Z\xe4\xb5\xffX\xbdT]\x93\x03\x96\xfcw\xd9"
    )

    assert aes.cbc.decrypt("A"*16, "B"*16, "C"*32) == (
        "\x0b\xd4\x18\xa6\xf7\xbd\x1a\xff\x16\x1f\xd1A\xd4\xbe5\x9b"
        "\n\xd5\x19\xa7\xf6\xbc\x1b\xfe\x17\x1e\xd0@\xd5\xbf4\x9a"
    )

def test_short_rc4():
    assert rc4.encrypt("Key", "Plaintext") == "bbf316e8d940af0ad3".decode("hex")
    assert rc4.decrypt("Wiki", "pedia") == "1021bf0420".decode("hex")
    assert rc4.decrypt("Secret", "Attack at dawn") == (
        "45a01f645fc35b383552544b9bf5".decode("hex")
    )
    assert rc4("hello", "world") == "783ecd96cf".decode("hex")