# http-brute-forcer
HTTP(s) login/pass brute forcer 

### Setup

  Before launching the cracker.py (main script) make sure that you have python3 with requests and re modules installed.
  To start script just launch it with python intepreter.

### Features

* Cracker provides multithreading login/password pair dictionary attacks on different websites 
* Program makes pattern HTTP request based on page html code parsing
* Brute force works with both HTTP and HTTPS because script does not sniff any packets to intercept them

### To do

* Add ability to execute script with arguments
* Provide command of setting whole HTTP request pattern without program participating
* Expand and write clear 'help'
* Ability to find Query string params and add them to HTTP request pattern
