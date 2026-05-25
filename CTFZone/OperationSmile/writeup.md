# Operation Smile - CTFZone 2026

**Category:** Forensics  
**Difficulty:** Easy  
**Points:** 100  
**Challenge Author:** jojomojo  
**Flag Format:** `ctfzone{...}`

## Challenge Description

> A smile shows more than just itself, can you view what's hidden?

Files provided:

- `smile.png`

---

## Initial Analysis

The challenge provided a PNG image named `smile.png`.

The first step was identifying the file type:

```bash
file smile.png
```

Output:

```text
PNG image data, 400 x 400, 8-bit/color RGB, non-interlaced
```

The file looked normal, but forensics challenges often hide data inside image metadata or append content after the image structure.

---

## Inspecting the PNG Structure

PNG files terminate with the `IEND` chunk.

Checking the end of the file:

```bash
xxd smile.png | tail -20
```

Output revealed:

```text
... IEND
PK...
secret/flag.txt
```

This strongly indicated that extra ZIP archive data had been appended after the PNG ended.

---

## Confirming Trailing Data

To determine whether extra bytes existed after `IEND`:

```python
data = open("smile.png","rb").read()

iend = data.find(b'IEND')

print("Trailing bytes:", len(data)-(iend+12))
```

Output:

```text
Trailing bytes: 200
```

The image contained 200 hidden bytes after the PNG ended.

---

## Extracting Hidden Data

Extract the trailing content:

```python
data = open("smile.png","rb").read()

iend = data.find(b'IEND')

trailing = data[iend+12:]

open("flag.zip","wb").write(trailing)
```

Attempting extraction:

```bash
unzip flag.zip
```

Result:

```text
missing 4 bytes in zipfile
```

The ZIP archive appeared corrupted.

---

## Reconstructing the ZIP Header

The archive was missing the ZIP signature:

```text
PK\x03\x04
```

Restoring it:

```python
fixed = b'PK\x03\x04' + trailing

open("flag_fixed.zip","wb").write(fixed)
```

Extracting:

```python
import zipfile

with zipfile.ZipFile("flag_fixed.zip") as z:
    print(z.namelist())

    print(
        z.read("secret/flag.txt").decode()
    )
```

Output:

```text
Congratulations! You found it.

ctfzone{sm1l3_and_th3_w0rld_sm1l3s_w1th_y0u}
```

---

## Flag

```text
ctfzone{sm1l3_and_th3_w0rld_sm1l3s_w1th_y0u}
```


