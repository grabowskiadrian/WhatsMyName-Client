# WhatsMyName-Client (WMNC)

This is external tool for: https://github.com/WebBreacher/WhatsMyName/

While attempting to develop the WhatsMyName project, I encountered several issues. Other available tools did not handle http-headers or POST requests. That's why I wrote my own script implementing the principles of WhatsMyName.

My version of the client supports 'request headers' and POST requests. I tried to follow all the guidelines provided in the wmn-data-schema.json file (https://github.com/WebBreacher/WhatsMyName/blob/main/CONTRIBUTING.md#format-of-the-json-file).

The script was prepared not only to search for a user with a given username but also to test newly added pages to the database.

Feel free to use this script; it's open-source, so that's exactly why it was made available!

<img width="333" src="https://user-images.githubusercontent.com/104733166/189120786-f854c5f8-57df-408c-bf33-b8eda521572c.png">

## Installation

```bash
git clone https://github.com/grabowskiadrian/whatsmyname-client.git
cd WhatsMyName-Client
pip3 install -r requirments.txt

python3 wmnc.py update
python3 wmnc.py
```
## Usage

WMNC (WhatsMyName-Client) is a command-line tool with the following commands:


```
$ python3 wmnc.py

░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░▒█░░▒█░█░░░░█▀▀▄░▀█▀░█▀▀░▒█▀▄▀█░░░░░░▒█▄░▒█░█▀▀▄░█▀▄▀█░█▀▀░
░▒█▒█▒█░█▀▀█░█▄▄█░░█░░▀▀▄░▒█▒█▒█░█▄▄█░▒█▒█▒█░█▄▄█░█░▀░█░█▀▀░
░▒▀▄▀▄▀░▀░░▀░▀░░▀░░▀░░▀▀▀░▒█░░▒█░▄▄▄▀░▒█░░▀█░▀░░▀░▀░░▒▀░▀▀▀░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░▒█▀▀▄░█░░░▀░░█▀▀░█▀▀▄░▀█▀░░░░░    WhatsMyName-Client   ░░░░
░▒█░░░░█░░░█▀░█▀▀░█░▒█░░█░░░░░░ v0.1 by grabowskiadrian ░░░░
░▒█▄▄▀░▀▀░▀▀▀░▀▀▀░▀░░▀░░▀░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

Look: https://github.com/WebBreacher/WhatsMyName

usage: python3 wmnc.py COMMAND [-h]

Commands:
  update           Download the newest version of wmn-data.json from the official GitHub repository.
  find USERNAME    Search for a specific USERNAME across all websites in the Project WhatsMyName database (wmn-data.json).

Development:
  list-sites       List all websites from the wmn-data.json file.
  list-categories  List all website categories from the wmn-data.json file.
  test             Run tests on websites to verify that the website configuration is correct.
```

Each command supports various options, which can be displayed by using the -h or --help flag.

## Examples for Searchers

### Update the local database

```bash
python3 wmnc.py update
```

Output:
```bash
$ python3 wmnc.py update

[+] wmn-data.json updated
[+] wmn-data-schema.json updated
```

### Search for a Username
To search for a specific username across all websites in the database, use the find command:

```bash
python3 wmnc.py find username-to-find
```

For example:

```bash
python3 wmnc.py find grabowskiadrian
```

You can use several parameters to limit the scope of the search:

To search only on one website use flag **-s** or **--site**:
```bash
python3 wmnc.py find grabowskiadrian -s bitbucket.com
```

To search only in one category use flag **-c** or **--category**:
```bash
python3 wmnc.py find grabowskiadrian -c social
```

You can also use **-l** or **--list** flag to pass path to your own .json file

```bash
python3 wmnc.py find grabowskiadrian -c social -l /path/to/my-list.json
```

**Output:**
```bash
$ python3 wmnc.py find adriangrabowski4

...
[+] Checking cda.pl : Found : https://www.cda.pl/adriangrabowski4
[-] Checking cfx.re : Not found
[-] Checking championat : Not found
[-] Checking Mastodon-Chaos.social : Not found
[-] Checking chaturbate : Not found
[-] Checking cHEEZburger : Not found
[-] Checking Chamsko : Not found
[-] Checking Chess.com : Not found
[+] Checking Chomikuj.pl : Found : https://chomikuj.pl/adriangrabowski4/
[+] Checking DockerHub : Found : https://hub.docker.com/v2/users/adriangrabowski4/
...
```


## Examples for Contributors of WhatsMyName

### List all websites
To list all websites in the database file, use the following command:

```bash
python3 wmnc.py list-sites
```
Output:

```bash
$ python3 wmnc.py list-sites  
         
|====================================================|======================|
| Site Name                                          | Category             |
|====================================================|======================|
| Mastodon-101010.pl                                 | social               |
| 1001mem                                            | social               |
| 3DNews                                             | social               |
| 247sports                                          | hobby                |
| 35photo                                            | social               |
| 3dtoday                                            | hobby                |
...
...
...
...
|====================================================|======================|
| Total                                              | 630                  |
|====================================================|======================|
```


If you're working on your own list of websites, you can pass -l or --list parameter to test your own .json file.

```bash
python3 wmnc.py list-sites -l /path/to/my-list.json
```

### List Website Categories
To list website categories and the number of websites in each category, run the following command:

```bash
python3 wmnc.py list-categories
```

Output:

```bash
$ python3 wmnc.py list-categories
|====================================================|======================|
| Category                                           | Sites count          |
|====================================================|======================|
| social                                             | 195                  |
| hobby                                              | 46                   |
| coding                                             | 31                   |
| xx NSFW xx                                         | 43                   |
| finance                                            | 23                   |
| misc                                               | 35                   |
| blog                                               | 16                   |
| political                                          | 13                   |
| gaming                                             | 47                   |
| tech                                               | 29                   |
| art                                                | 14                   |
| music                                              | 18                   |
| business                                           | 23                   |
| health                                             | 13                   |
| shopping                                           | 23                   |
| news                                               | 9                    |
| video                                              | 11                   |
| images                                             | 24                   |
| dating                                             | 13                   |
| archived                                           | 4                    |
|====================================================|======================|
| Total                                              | 630                  |
|====================================================|======================|
```

If you're working on your own list of websites, you can pass -l or --list parameter to test your own .json file.

```bash
python3 wmnc.py list-categories -l /path/to/my-list.json
```

### Test wmn-data.json file

You can test websites to verify their configurations using the **test** command. 

For example, to test a specific website by name, use:

```bash
python3 wmnc.py test -s github.com
```

To test specific category, use: 

```bash
python3 wmnc.py test -c social
```

You can pass **-l** or **--list** parameter to test your own .json file 

```bash
python3 wmnc.py test -c social -l /path/to/my-list.json
```

To test all websites, use:

```bash
python3 wmnc.py test
```

A check is performed for each website. This testing process evaluates whether the responses defined for the found user and user not found cases are correct. This allows you to verify that previously defined pages still work as expected.

**Output:**

```bash
$ python3 wmnc.py test

| Site name                                          | User found                      | User not found                  |
|====================================================|=================================|=================================|
| Mastodon-101010.pl                                 | PASSED                          | PASSED                          |
| 1001mem                                            | PASSED                          | PASSED                          |
| 3DNews                                             | PASSED                          | PASSED                          |
| 247sports                                          | PASSED                          | PASSED                          |
| 35photo                                            | PASSED                          | PASSED                          |
| 3dtoday                                            | PASSED                          | PASSED                          |
| 7cup                                               | PASSED                          | PASSED                          |
| 7dach                                              | PASSED                          | PASSED                          |
| 21buttons                                          | PASSED                          | PASSED                          |
| aaha_chat                                          | NOT PASSED                      | ???                             |
| about.me                                           | PASSED                          | PASSED                          |
| ACF                                                | PASSED                          | PASSED                          |
| admire_me                                          | PASSED                          | PASSED                          |
| Adult_Forum                                        | PASSED                          | PASSED                          |
| adultism                                           | PASSED                          | PASSED                          |
| ADVFN                                              | PASSED                          | PASSED                          |
```


## License

I am a regular contributor to the Project WhatsMyName, but I am not officially part of its creation. Check WhatsMyName project for more details:
https://github.com/WebBreacher/WhatsMyName