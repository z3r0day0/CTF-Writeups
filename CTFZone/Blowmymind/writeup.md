# Blowmymind — Crypto Challenge

## Challenge

We are given a bcrypt hash of an admin's password:

```
$2a$12$0dr0QLZXBYEgGArDlqMVOebTRTiEKNTflYOz9Eht30VelGBfBm1.C
```

## Background

Bcrypt (`$2a$`) is a password hashing function based on the Blowfish cipher. The `$2a$12$` prefix means a cost factor of 12 (2^12 iterations). The hash is a base64-encoded string containing the salt and the digest.

## Attack

The challenge title "Blow My Mind" is a hint — the password is something trivial. Since bcrypt is intentionally slow (cost 12 makes brute-forcing expensive), the password must be weak and guessable.

A quick test with common passwords reveals the answer immediately:

```python
import bcrypt

hash = b"$2a$12$0dr0QLZXBYEgGArDlqMVOebTRTiEKNTflYOz9Eht30VelGBfBm1.C"

# The password is simply "password"
print(bcrypt.checkpw(b"password", hash))  # True
```

## Flag

```
password
```
