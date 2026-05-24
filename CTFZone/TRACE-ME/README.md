# TRACE-ME - Reverse Engineering Writeup

## Challenge Information

* **Challenge Name:** TRACE-ME
* **Category:** Reverse Engineering
* **Difficulty:** Beginner / Easy
* **Flag:** `ctfzone{str4c3_l34ks_my_byt3s_1_by_1_e2f9}`

---

# Description

The challenge provided a stripped 64-bit ELF binary.
The goal was to analyze the executable and recover the hidden flag.

The binary appeared noisy at first because it mixed junk output with encoded bytes in an attempt to confuse analysis.

---

# Initial Enumeration

The first step was identifying the binary type.

```bash
file trace-me
```

Output:

```text
ELF 64-bit LSB executable, x86-64, stripped
```

The binary being stripped meant symbol names and debugging information had been removed.

---

# Checking Strings

Next, I searched for readable strings inside the binary.

```bash
strings trace-me
```

Interesting output:

```text
/dev/null
photons logged. nothing to see here.
```

This indicated the binary was intentionally hiding its actual functionality.

---

# Runtime Analysis

Running the binary produced strange output containing random symbols mixed with unreadable bytes.

To understand what was happening internally, I analyzed the executable behavior using reverse engineering tools.

The binary performs the following operations:

1. Opens `/dev/null` using:

```c
open("/dev/null", O_WRONLY)
```

2. Uses a `cmovs` instruction to redirect output to `stderr` if `/dev/null` fails to open.

3. Executes a loop exactly 42 times — matching the expected flag length.

Inside each loop iteration, the program performs two single-byte `write()` calls:

| Step | Action                                                 |
| ---- | ------------------------------------------------------ |
| 1    | Writes junk characters from `!@#$%^&*?~.+=`            |
| 2    | Writes encrypted flag bytes XORed with a repeating key |

The junk output was only used as noise to mislead anyone reading the raw program output.

---

# Important Data in `.rodata`

During analysis, several important values were found inside the `.rodata` section.

| Offset   | Contents                 |
| -------- | ------------------------ |
| `0x2040` | `!@#$%^&*?~.+=`          |
| `0x2050` | XOR key                  |
| `0x2060` | XOR encrypted flag bytes |

Key bytes:

```python
key = bytes([
    0x37, 0x9a, 0x4c, 0x1d,
    0xb8, 0x6e, 0xf1, 0x25
])
```

Encrypted bytes:

```python
encoded = bytes([
    0x8d, 0xf0, 0x2d, 0x6f, 0xdd, 0x07, 0x82, 0x4f,
    0xfa, 0x92, 0x7c, 0x3b, 0xac, 0x06, 0xa2, 0x0a,
    0xd6, 0xd7, 0x1d, 0x37, 0xdd, 0x01, 0xb5, 0x40,
    0xc3, 0xd0, 0x18, 0x43, 0xde, 0x00, 0xa6, 0x7c,
    0xc2, 0x9a, 0x6b, 0x04, 0x99, 0x5d, 0xee, 0x21,
    0x80, 0x10
])
```

---

# Decryption Logic

The binary used XOR encryption with a repeating 8-byte key.

Since XOR is reversible:

```text
flag[i] = encoded[i] XOR key[i % 8]
```

The junk characters written between bytes were irrelevant and did not affect the actual encrypted flag data.

---

# Solve Script

```python
encoded = bytes([
    0x8d, 0xf0, 0x2d, 0x6f, 0xdd, 0x07, 0x82, 0x4f,
    0xfa, 0x92, 0x7c, 0x3b, 0xac, 0x06, 0xa2, 0x0a,
    0xd6, 0xd7, 0x1d, 0x37, 0xdd, 0x01, 0xb5, 0x40,
    0xc3, 0xd0, 0x18, 0x43, 0xde, 0x00, 0xa6, 0x7c,
    0xc2, 0x9a, 0x6b, 0x04, 0x99, 0x5d, 0xee, 0x21,
    0x80, 0x10
])

key = bytes([
    0x37, 0x9a, 0x4c, 0x1d,
    0xb8, 0x6e, 0xf1, 0x25
])

flag = ''.join(chr(encoded[i] ^ key[i % 8]) for i in range(len(encoded)))

print(flag)
```

---

# Output

```text
ctfzone{str4c3_l34ks_my_byt3s_1_by_1_e2f9}
```

---

# Final Flag

```text
ctfzone{str4c3_l34ks_my_byt3s_1_by_1_e2f9}
```



