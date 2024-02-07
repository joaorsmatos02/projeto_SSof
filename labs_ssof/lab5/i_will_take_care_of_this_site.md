# Challenge `I will take care of this site` writeup

- Vulnerability: What type of vulnerability is being exploited
  - Vulnerable to SQL injection

- Where: Where is the vulnerability present
  - `http://mustard.stt.rnl.tecnico.ulisboa.pt:23261`, on the login page

- Impact: What results of exploiting this vulnerability
  - Allows the user to login as admin without password

## Steps to reproduce

1. Access `http://mustard.stt.rnl.tecnico.ulisboa.pt:23261/login`
2. The username form is vulnerable to SQLi
3. The executed query is (discovered by inputting `'` with a random string following):

```sql
SELECT id, username, password, bio, age, jackpot_val FROM user WHERE username = '<input>' AND password = '<input>'
```

4.The string used to login as admin was:

```
admin'--
```
