# Challenge `PwnTools Sockets` writeup

- Vulnerability: What type of vulnerability is being exploited
  - Vulnerable to brute-force attack

- Where: Where is the vulnerability present
  - `http://mustard.stt.rnl.tecnico.ulisboa.pt:23055`

- Impact: What results of exploiting this vulnerability
  - Allows the user to brute-force tries to get the correct result

## Steps to reproduce

1. Start a `remote` session in `mustard.stt.rnl.tecnico.ulisboa.pt` on port 23055
2. Receive the text and extract the target and current sum
4. Repeatedly send `MORE` until the total equals the target
5. Send `FINISH` to get the flag

The code used was the following:

```py
  from pwn import *
  import re

  s = remote("mustard.stt.rnl.tecnico.ulisboa.pt", "23055", timeout=9999)

  res = s.recv()
  nums = re.findall(r'\d+', res.decode())
  target = nums[0]

  while target != nums[1]:
      s.send(b"MORE\n")
      res = s.recv()
      nums = re.findall(r'\d+', res.decode())

  s.send(b"FINISH\n")
  res = s.recvall()
  print(res)
```
