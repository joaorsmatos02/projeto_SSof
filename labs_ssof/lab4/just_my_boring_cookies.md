# Challenge `Just my boring cookies` writeup

- Vulnerability: What type of vulnerability is being exploited
  - Vulnerable to XSS

- Where: Where is the vulnerability present
  - `http://mustard.stt.rnl.tecnico.ulisboa.pt:23251`, on the search bar

- Impact: What results of exploiting this vulnerability
  - Allows the user to run code through XSS, possibly used to steal cookies

## Steps to reproduce

1. Access `http://mustard.stt.rnl.tecnico.ulisboa.pt:23251`
2. The search feature will run any html passed on the search
3. In order to get the flag, the cookie was displayed on an alert, by searching:

```html
<script>alert(document.cookie)</script> 
```