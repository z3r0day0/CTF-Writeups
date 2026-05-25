#!/usr/bin/env python3

def encrypt(data: str, key: str) -> bytes:
    result = bytearray()
    key_len = len(key)

    for i, c in enumerate(data.encode()):
        result.append(c ^ ord(key[i % key_len]))

    return bytes(result)


if __name__ == "__main__":
    plaintext = "flag{example}"
    key = "urchin"

    encrypted = encrypt(plaintext, key)

    with open("enc", "w") as enc:
        enc.write(encrypted.hex())
