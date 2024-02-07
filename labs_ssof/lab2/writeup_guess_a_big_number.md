# Challenge `Guess a BIG Number` writeup

- Vulnerability: What type of vulnerability is being exploited
  - Vulnerable to brute-force attack, allowing the user to guess the correct number

- Where: Where is the vulnerability present
  - `http://mustard.stt.rnl.tecnico.ulisboa.pt:22052/number/`

- Impact: What results of exploiting this vulnerability
  - Allows the user to brute-force tries to get the correct result

## Steps to reproduce

1. Start a `remote` session in `http://mustard.stt.rnl.tecnico.ulisboa.pt:22052`
2. Guess a number between 0 and 100000 in `http://mustard.stt.rnl.tecnico.ulisboa.pt:22052/number/{guess}`
3. Receive the text and verify if the result is lower or higher
4. Since we know the correct guess is between 0 and 100000, in each try we can discard half of the possible guesses by testing the median number

The code used was the following:

```py
  import requests

  link = "http://mustard.stt.rnl.tecnico.ulisboa.pt:22052"

  s = requests.Session()

  s.get(link)

  lower = 0
  upper = 100000

  while True:
      test = int((lower + upper) / 2)
      response = s.get(link + "/number/" + str(test))
      
      if ("SSof" in response.text):
          print(response.text)
          break
      elif ("Higher" in response.text):
          lower = test
      else:
          upper = test
```
