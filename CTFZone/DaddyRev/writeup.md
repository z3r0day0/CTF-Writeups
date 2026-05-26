# DaddyRev — CTFZone Reversing Writeup

## Challenge Information

- **Category:** Reverse Engineering
- **Difficulty:** Medium
- **Challenge:** DaddyRev
- **Goal:** Find what is "missing" and recover the hidden flag.

---

## Initial Analysis

After extracting the challenge, I inspected the binary:

```bash
file daddyrev
checksec --file=daddyrev

Output:

ELF 64-bit LSB pie executable
Dynamically linked
Not stripped
Contains debug information

The binary was a Go executable, which immediately suggested that reversing would involve identifying Go runtime functions and main.main.

String Analysis

I extracted strings:

strings daddyrev

Interesting values appeared:

pewpew
ctfzone
BEEP BOOP CRASH
You are trying so hard but you are failing!

This hinted that an environment variable check was involved.

Finding the Hidden Check

Using:

nm daddyrev | grep main.main

I found:

0000000000004ce0 T main.main

Disassembling:

objdump -d daddyrev

revealed:

os.LookupEnv("pewpew")

The program checks for an environment variable named:

pewpew

Behavior:

Variable not set → fail
Wrong value → crash
Correct value → continue execution

Further analysis showed the expected value:

ctfzone

So:

export pewpew=ctfzone
Hidden Ciphertext

A long hexadecimal string exists in .rodata:

1606051206001606171d33300055142b111f301a175247523e300c10172b20282e272926301b

The binary decodes it using:

encoding_hex.DecodeString()

Decoded length:

38 bytes
XOR Logic

Inside the main loop:

for i in range(length):
    output[i] = env[i % len(env)] ^ ciphertext[i]

The environment value:

ctfzone

acts as the XOR key.

Pseudo-code:

env = b"ctfzone"

for i in range(len(ciphertext)):
    flag += ciphertext[i] ^ env[i % len(env)]
Solve Script
hex_str = "1606051206001606171d33300055142b111f301a175247523e300c10172b20282e272926301b"

cipher = bytes.fromhex(hex_str)

key = b"ctfzone"

flag = bytearray()

for i in range(len(cipher)):
    flag.append(cipher[i] ^ key[i % len(key)])

print(flag.decode())

Run:

python3 solve.py

Output:

urchinsec{I_n0w_we_tr134D_but_FRAILED}
Flag
urchinsec{I_n0w_we_tr134D_but_FRAILED}
Summary

The challenge used:

Hidden environment-variable checks
Hex decoding
Repeating XOR encryption

By reversing the Go binary and understanding the environment logic, we recovered the XOR key and decrypted the hidden flag.
