# http-brute-forcer
HTTP(s) login/pass brute forcer 

### Setup

  Before launching the cracker.py (main script) make sure that you have python3 with requests and argparse modules installed.
  To start script just launch it with python intepreter.
### Usage

cracker [-h] (-l LOGIN | -L dict.txt) (-p PASSWORD | -P dict.txt) -m  HTTP_METHOD [-t THREADS] [--reverse]  target

# positional arguments:
  target          set target host (specify login action if it exists) e.g. https://target.com/login.php

# optional arguments:
  * -h, --help      show this help message and exit
  * -l LOGIN        set attack login
  * -L dict.txt     set login dictionary
  * -p PASSWORD     set attack password
  * -P dict.txt     set password dictionary
  * -m HTTP_METHOD  set http request method (POST, GET, etc.)
  * -t THREADS      set number of threads to use (default: 3)
  * --reverse, -r   set brute force attack type


### Features

* Cracker provides multithreading login/password pair dictionary attacks on different websites 
* Program makes pattern HTTP request based on user input
* Brute force works with both HTTP and HTTPS because script does not sniff any packets to intercept them

### To do

* Add colored output
