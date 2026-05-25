# Bytecode Whispers — CTFZone 2026 Writeup

**Category:** Blockchain  
**Difficulty:** Easy  
**Points:** 100  

---

## Challenge Description

> The contract bytecode contains a flag embedded as a constant value. Extract the flag from the bytecode.

Files provided:

- `bytecode.json`

---

## Initial Analysis

The provided file contained a compiled Solidity contract with both:

- creation bytecode
- deployed bytecode

To inspect it:

```bash
cat bytecode.json
```

or:

```bash
jq . bytecode.json
```

Inside the bytecode there were long hexadecimal sequences representing EVM instructions.

---

## Understanding EVM Bytecode

Ethereum bytecode consists of opcodes and their operands.

One opcode immediately stood out:

```text
7f
```

In EVM:

```text
0x7f = PUSH32
```

`PUSH32` places the next **32 bytes** directly onto the stack.

Structure:

```text
7f [32 bytes]
```

This often contains embedded constants such as:

- strings
- hashes
- addresses
- flags

---

## Extracting the Constant

After locating the `PUSH32`, the next 32 bytes were:

```text
6374667a6f6e657b626c30736b735f346c6c5f316e5f304e335f636841316e7d
```

To decode:

```python
hexdata="6374667a6f6e657b626c30736b735f346c6c5f316e5f304e335f636841316e7d"

print(bytes.fromhex(hexdata).decode())
```

Output:

```text
ctfzone{bl0sks_4ll_1n_0N3_chA1n}
```

---

## Why This Worked

Solidity frequently embeds constants directly into bytecode.

When developers use:

```solidity
bytes32 constant FLAG = "...";
```

the compiler may inline it as a `PUSH32` instruction.

Since blockchain bytecode is public, hidden constants can often be recovered directly from the deployed code.

---

## Flag

```text
ctfzone{bl0sks_4ll_1n_0N3_chA1n}
```

