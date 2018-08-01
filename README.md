# http-brute-forcer
HTTP(s) HTML login/pass  brute force cracker

### Dependencies

 * [Firefox browser](https://www.mozilla.org/en-US/firefox/)
 * Web driver for firefox - [geckodriver](https://github.com/mozilla/geckodriver/releases)
 * [Selenium](https://docs.seleniumhq.org/) module for python 3
 * [argparse](https://pypi.org/project/argparse/) module for python 3


### Features

* Cracker provides multithreading login/password pair dictionary attacks on different websites
* Program uses selenium browser automation so you can observe attack process
* It works with html forms that make HTTP(s) requests with login/pass data

### Usage
![example-gif](https://github.com/shmel3/http-brute-forcer/blob/master/example/example.gif)


### Warning

* Script works only with html based authentication
* It can't recognize captcha
* Do not use many threads for attack: your machine may fail with handling several webdrivers at the same time
