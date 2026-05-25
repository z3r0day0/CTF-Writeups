# BabyRev — CTFZone 2026 Writeup

**Category:** Reverse Engineering  
**Difficulty:** Easy  
**Points:** 100  

---

## Challenge Description

> Just a program printing hello world!

Files provided:

- `babyrev`

At first glance the binary simply prints:

```text
Hello World!
```

This looked suspicious because reverse engineering challenges often use simple output as a distraction.

---

## Initial Analysis

First I checked the binary:

```bash
file babyrev
checksec --file=babyrev
strings babyrev
```

Running the program:

```bash
./babyrev
```

Output:

```text
Hello World!
```

No flag appeared.

This suggested that the visible output was only a decoy and the actual flag was hidden elsewhere.

---

## Reversing in Ghidra

Opening the binary in Ghidra and inspecting `main()` revealed several unusual `movabs` instructions.

Example:

```asm
movabs rax,0x65736e6968637275
mov [rbp-0x30],rax
```

Instead of loading normal values, these instructions contained large immediate constants.

The values were copied directly into stack memory.

---

## Extracting the Hidden Bytes

Converting each immediate value from little-endian format produced:

| Offset | Bytes | ASCII |
|----------|--------|--------|
| +0 | 75 72 63 68 69 6e 73 65 | urchinse |
| +8 | 63 7b 77 65 6c 63 30 6d | c{welc0m |
| +16 | 65 5f 74 30 5f 72 33 76 | e_t0_r3v |
| +24 | 65 72 73 65 5f 45 4e 47 | erse_ENG |
| +26 | 73 65 5f 45 4e 47 49 4e | se_ENGIN |
| +34 | 45 45 52 49 4e 47 7d 00 | EERING} |

---

## Understanding the Overlap

The writes overlap in memory.

The write at offset:

```text
+26
```

overwrites part of:

```text
+24
```

Therefore only:

```text
er
```

survives from the fourth chunk.

After reconstructing all stack writes in memory order:

```text
urchinse
c{welc0m
e_t0_r3v
er
se_ENGIN
EERING}
```

Combining everything gives:

```text
urchinsec{welc0me_t0_r3verse_ENGINEERING}
```

---

## Recovered Flag

```text
urchinsec{welc0me_t0_r3verse_ENGINEERING}
```


