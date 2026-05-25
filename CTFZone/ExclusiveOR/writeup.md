# ExclusiveOR — Crypto Challenge

## Challenge

We are given `enc.py` (the encryption script) and `enc` (the encrypted output).

```python
def encrypt(data: str, key: str) -> bytes:
    result = bytearray()
    key_len = len(key)
    for i, c in enumerate(data.encode()):
        result.append(c ^ ord(key[i % key_len]))
    return bytes(result)

plaintext = "flag{example}"  # placeholder
key = "urchin"               # placeholder
encrypted = encrypt(plaintext, key)
with open("enc", "w") as enc:
    enc.write(encrypted.hex())
```

## Vulnerability

The encryption is a simple repeating-key XOR (Vigenère over ASCII). The key is **reused** for every block. Given known plaintext structure (the flag format), we can recover the key.

## Attack

1. The `enc` file contains hex-encoded ciphertext: `000000000000061700131101072d0504080908` (19 bytes).
2. The first 6 bytes are `0x00`, meaning `plaintext[0:6] == key`.
3. Using the example key `"urchin"` (6 chars) from `enc.py`, we decrypt:

```python
from bytes import bytes, hex
key = b"urchin"
ciphertext = bytes.fromhex("000000000000061700131101072d0504080908")
flag = bytes(ciphertext[i] ^ key[i % 6] for i in range(len(ciphertext))).decode()
```

4. This reveals the flag directly since the example key **is** the real key used.

## Flag

```
urchinsec{xor_flag}
```
