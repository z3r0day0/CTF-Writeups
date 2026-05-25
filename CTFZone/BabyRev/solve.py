#!/usr/bin/env python3
import struct

# The flag is embedded in main() as immediate values (movabs) written to the stack.
# Each 8-byte chunk is stored little-endian in the instruction encoding.

chunks = [
    # movabs $0x65736e6968637275, %rax  -> stored at rbp-0x30
    struct.pack("<Q", 0x65736e6968637275),
    # movabs $0x6d30636c65777b63, %rdx  -> stored at rbp-0x28
    struct.pack("<Q", 0x6d30636c65777b63),
    # movabs $0x7633725f30745f65, %rax  -> stored at rbp-0x20
    struct.pack("<Q", 0x7633725f30745f65),
    # movabs $0x474e455f65737265, %rdx  -> stored at rbp-0x18
    struct.pack("<Q", 0x474e455f65737265),
    # movabs $0x4e49474e455f6573, %rax  -> stored at rbp-0x16 (overwrites last 6B of above)
    struct.pack("<Q", 0x4e49474e455f6573),
    # movabs $0x7d474e49524545,   %rdx  -> stored at rbp-0x0e
    struct.pack("<Q", 0x7d474e49524545),
]

# Simulate the stack writes
buf = bytearray(b"\x00" * 42)

# Write 1 at offset 0
buf[0:8] = chunks[0]
# Write 2 at offset 8
buf[8:16] = chunks[1]
# Write 3 at offset 16
buf[16:24] = chunks[2]
# Write 4 at offset 24 (rbp-0x18 = 0x30-0x18 = 24)
buf[24:32] = chunks[3]
# Write 5 at offset 26 (rbp-0x16 = 0x30-0x16 = 26) — overwrites bytes 26-31 of previous
buf[26:34] = chunks[4]
# Write 6 at offset 34 (rbp-0x0e = 0x30-0x0e = 34)
buf[34:42] = chunks[5]

flag = buf.decode("ascii").rstrip("\x00")
print(f"Flag: {flag}")
