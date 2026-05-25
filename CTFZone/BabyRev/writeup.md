# BabyRev — CTFZone Reversing Challenge

## Analysis

The binary is a minimal 64-bit ELF that prints `"Hello World!"` and exits. The real flag is **not printed** — it's hidden in the `main` function's instruction stream.

In `main` (at `0x1139`), six `movabs` instructions load 8-byte immediates that are written to the stack at overlapping offsets. These byte sequences spell out the flag when concatenated in memory order.

## Stack Layout

Starting at `rbp-0x30`, the writes are:

| Offset | Bytes (little-endian) | ASCII |
|--------|----------------------|-------|
| +0     | `75 72 63 68 69 6e 73 65` | `urchinse` |
| +8     | `63 7b 77 65 6c 63 30 6d` | `c{welc0m` |
| +16    | `65 5f 74 30 5f 72 33 76` | `e_t0_r3v` |
| +24    | `65 72 73 65 5f 45 4e 47` | `erse_ENG` ← last 6 bytes overwritten |
| +26    | `73 65 5f 45 4e 47 49 4e` | `se_ENGIN` |
| +34    | `45 45 52 49 4e 47 7d 00` | `EERING}\0` |

The write at offset +26 overwrites bytes 26-31 of the write at +24, so only bytes 24-25 (`er`) survive from the 4th chunk.

## Recovered Flag

```
urchinsec{welc0me_t0_r3verse_ENGINEERING}
```

## Solve Script

See `solve.py` for the automated recovery.
