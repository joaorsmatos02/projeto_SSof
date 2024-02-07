# Challenge `Money, money, money!` writeup

- Vulnerability: What type of vulnerability is being exploited
  - Vulnerable to SQL injection

- Where: Where is the vulnerability present
  - `http://mustard.stt.rnl.tecnico.ulisboa.pt:23261`, on the edit bio form

- Impact: What results of exploiting this vulnerability
  - Allows the user to change their lottery target

## Steps to reproduce

1. Create a new account on `http://mustard.stt.rnl.tecnico.ulisboa.pt:23261/register`
2. Navigate to the user profile
3. The query executed when updating the bio is (discovered by inputting `'` with a random string following):

```sql
UPDATE user SET bio = '<input>' WHERE username = '<username>'
```

4.The following string may be inputted in order to change the lottery target:

```
a', jackpot_val = '0
```
