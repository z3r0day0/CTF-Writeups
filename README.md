# RAPID INVASION — CTF Write-Up

## Challenge Information

**Challenge Name:** RAPID INVASION
**Category:** Reverse Engineering
**Difficulty:** Medium
**Description:**
*"Can we really view opcode in plaintext or not?"*

**Flag Format:**

```text
ctfzone{...}
```

**Files Provided:**

```text
rapid.zip
```

After extracting:

```text
rapid_invasion
```

---

# Initial Recon

I started by creating a workspace and extracting the challenge files.

```bash
mkdir rapid
mv ~/Downloads/rapid.zip ~/rapid/
cd ~/rapid
unzip rapid.zip
ls
```

The archive extracted a file named:

```text
rapid_invasion
```

I identified the file type:

```bash
file rapid_invasion
```

Output:

```text
Mach-O 64-bit arm64 executable
```

This indicated the binary was compiled for macOS ARM64.

---

# String Analysis

The first step in reverse engineering a binary is searching for readable strings.

```bash
strings rapid_invasion
```

Output:

```text
Initializing rapid invasion protocol...
Enter the access code:
flag{this_is_not_the_flag_nice_try}
ctfzone{nope_not_this_one_either}
[+] ACCESS GRANTED.
[+] The invasion begins. Well done, operative.
[!] INVASION REPELLED. Access denied.
```

Two possible flags immediately appeared:

```text
flag{this_is_not_the_flag_nice_try}
ctfzone{nope_not_this_one_either}
```

However, both were fake flags intentionally inserted as decoys.

This indicated that the challenge author expected players to rely only on visible strings and stop there.

---

# Disassembly

I moved to static analysis using LLVM tools:

```bash
llvm-objdump-18 -d rapid_invasion
```

I also dumped constant sections:

```bash
llvm-objdump-18 -s -j __const rapid_invasion
```

During analysis, I discovered that the binary did not perform validation directly.

Instead, it generated and executed instructions dynamically through a custom virtual machine.

---

# Discovering the Virtual Machine

The binary contained a dispatch table used to interpret custom opcodes.

Valid opcodes included:

```text
0x10 -> MUL
0x11 -> LOAD INPUT
0x20 -> XOR
0x21 -> ADD
0x22 -> SUB
0x23 -> ROTATE LEFT
0x30 -> COMPARE
0x31 -> CONDITIONAL SKIP
0xff -> HALT
```

The application was effectively executing a small bytecode program rather than validating user input directly.

This meant the challenge was hiding its logic inside VM instructions.

---

# Understanding Bytecode Generation

While tracing execution, I found a loop responsible for constructing bytecode.

Each entry generated approximately 22 bytes of VM instructions.

The generated logic looked conceptually like:

```text
Load character
Multiply accumulator
XOR values
Add constant
Subtract constant
Rotate bits
Compare against expected value
```

The interesting part was the challenge description:

> "Can we really view opcode in plaintext or not?"

During analysis I noticed the binary XORed data using:

```text
XOR 0xbe
```

and later performed:

```text
XOR 0xbe
```

again.

Since:

```text
A XOR B XOR B = A
```

the operation cancels itself.

Meaning:

```text
the opcode stream was plaintext the entire time
```

This was the hidden trick of the challenge.

---

# Reversing the Validation Logic

After understanding the VM operations, the validation formula reduced to:

```text
ROL(input + previous_offset − constant, rotate_value)
=
expected_value
```

To recover the original input:

```text
input =
ROR(expected_value, rotate_value)
− previous_offset
+ constant
```

So instead of brute forcing the access code, I reversed each VM operation mathematically.

I wrote a Python script to recover every character.

Example helper functions:

```python
def rol(v,k):
    k &= 7
    return ((v << k)|(v>>(8-k))) & 0xff

def ror(v,k):
    k &= 7
    return ((v >> k)|(v<<(8-k))) & 0xff
```

Using the constants extracted from the binary template section, I reconstructed all 30 bytes.

Recovered access code:

```text
394bc164e4aa17a63da5168249aa6e11bc2aa400cc30b0689850c01ca33c
```

---

# Final Step

The recovered access code still appeared random.

Further analysis revealed another transformation:

Each byte was XORed with previous VM constants.

Running:

```python
flag = access_code ^ e3_values
```

revealed:

```text
ctfzone{r4p1d_vm_cr4ck3r_2026}
```

---

# Final Flag

```text
ctfzone{r4p1d_vm_cr4ck3r_2026}
```

---


This challenge demonstrates that bytecode and opcodes can appear hidden while actually remaining in plaintext.
