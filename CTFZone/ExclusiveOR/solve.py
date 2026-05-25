#!/usr/bin/env python3

with open("files/exclusiveOR/enc") as f:
    ciphertext_hex = f.read().strip()

ciphertext = bytes.fromhex(ciphertext_hex)
print(f"Ciphertext bytes ({len(ciphertext)}): {ciphertext.hex()}")

key = b"urchin"
plaintext = bytes(
    ciphertext[i] ^ key[i % len(key)] for i in range(len(ciphertext))
).decode()

print(f"Key: {key.decode()}")
print(f"Flag: {plaintext}")
