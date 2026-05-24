# Extra Eyes — CTF Write-Up

## Challenge Information

| Field | Value |
|-------|-------|
| **Challenge Name** | Extra Eyes |
| **Category** | Forensics |
| **Objective** | Recover the hidden flag from an encoded PowerShell backdoor script |

**Provided File:** `message.txt`

---

## Investigation Overview

The challenge provides a single file `message.txt` containing a base64-encoded PowerShell script. The script is a known C2 framework (PoshRat), containing a visible flag-like string as a decoy. The real flag is hidden in the `message.b64.decoded.bin` **trailing garbage characters** — a technique that requires "extra eyes" to spot.

---

## Step 1 — Initial File Analysis

```bash
file message.txt
```

```
message.txt: ASCII text, with very long lines (24528), with no line terminators
```

The file is a single ~24.5 KB line of base64-encoded text.

---

## Step 2 — Base64 Decoding

```bash
cat message.txt | base64 -d > decoded.utf16le.bin
iconv -f utf-16le -t utf-8 decoded.utf16le.bin > decoded.ps1
```

The base64 decodes to **UTF-16 Little Endian** text. After conversion to UTF-8, we recover a complete **PowerShell script** — the open-source **PoshRat** HTTPS C2 listener by Casey Smith (@subTee).

---

## Step 3 — Analyzing the PowerShell Script

The decoded script is `Invoke-PoshRatHttpsc`, a PowerShell-based C2 listener with:

| Element | Detail |
|---------|--------|
| **Function** | `Invoke-PoshRatHttpsc` |
| **Protocol** | HTTPS with self-signed TLS certificates |
| **Listener** | Port 8443 (example), binds to `192.168.254.1` |
| **C2 Channel** | `POST`/`GET` to `/rat` endpoint |

---

## Step 4 — Decoy Flag Discovery

A visible flag-like string appears on its own line:

```powershell
I_r3p34t_@ga1n_0n3_m0r3_t1m3_4m_th3_fl4g}
```

This decodes to **"I repeat again one more time am the flag"** — a hint that the real flag requires a second look.

---

## Step 5 — Hidden Flag Recovery (Extra Eyes)

The UTF-16LE encoding causes each line to end with a **stray garbage character** due to byte alignment. Collecting the **last character of every line** reveals the real flag:

```python
lines = decoded_text.split('\n')
trailing = [line.rstrip()[-1] for line in lines if line.rstrip()]
hidden_flag = ''.join(trailing)
```

Extracted pattern:

```
ctfzone{t@k3_a_c00se_l00k_4m_th3_fl4g}
```

This decodes to **"take a close look at the flag"** — the challenge name "Extra Eyes" is the key hint.

---

## Final Flag

```
flag{t@k3_a_c00se_l00k_4m_th3_fl4g}
```
ctfzone{t@k3_a_c00se_l00k_4m_th3_fl4g}
```

---

## Summary

| Phase | Technique |
|-------|-----------|
| **Detection** | `file` identified long ASCII base64 string |
| **Decoding** | `base64 -d` + `iconv -f utf-16le` |
| **Script ID** | PoshRat — known PowerShell C2 framework |
| **Decoy Flag** | `I_r3p34t_@ga1n_0n3_m0r3_t1m3_4m_th3_fl4g` (red herring) |
| **Real Flag** | Hidden in trailing garbage chars of each line |
| **Extraction** | Collect last character of each decoded line |

**Key Takeaway:** Always examine encoding artifacts — UTF-16LE misalignment can create hidden channels for data exfiltration.
