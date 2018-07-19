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
## if you leave my contact link in it.                                            ##
##                                                                                ##
## ============================================================================== ##


### TODO ###
# * read query string
# * let user set whole http request without parsing html
# * rewrite commands
# * add argparse
### END TODO ###


import os
import platform



### local modules ###
import htmlparser as hp
import bruteforce as bf
### end local modules ###




### aplication variables ###
target_url = str()
login_dict = str()
logins = []
password_dict = str()
passwords = []
### end definition ###


# ================================= TARGET CLASS ================================= #
"""
Class 'target' contains main information about html code of target page:
	* all html forms (<form method=...> ... </form>) found in code;
	* login_form that has login and password input (guessed by program or specified by user);
	* login_form_id that is actually its index in html_forms list;
	* login_var - name variable that holds login user input 
	* pass_var - the same as login_var, but holds password user input
"""
	
class target:
	def __init__(self, html_code):
		self.html_forms = hp.get_forms(html_code)
		self.login_form_id = hp.guess_login_form(self.html_forms)
		self.url = str()
		if self.login_form_id != -1:
			self.login_form = self.html_forms[self.login_form_id]
			self.login_var = hp.guess_login_variable(self.get_login_form_variables())
			self.pass_var = hp.guess_pass_variable(self.get_login_form_variables())
		self.forms_info = { }
		self.request_body = { }
		self.unsuccess_sign = str() # look ask_unsuccess_sign() function


	def set_login_form(self, login_form_id):
		if self.login_form_id == -1:
			return None
		self.login_form = self.html_forms[login_form_id]
		self.login_var = hp.guess_login_variable(self.get_login_form_variables())
		self.pass_var = hp.guess_pass_variable(self.get_login_form_variables())


	# returns input variables of login form
	def get_login_form_variables(self):
		if self.login_form_id == -1:
			return None
		login_form_data = hp.inspect_form(self.login_form)
		return login_form_data['Variables']
	

	# return all important information about login form
	# e.g. method type, class name, input variables, etc.
	def get_login_form_data(self):
		if self.login_form_id == -1:
			return None
		login_form_data = hp.inspect_form(self.login_form)
		return login_form_data

	def generate_request_body(self):
		"""
		 Function generates dictionary of input variables 
		 and its values (login form)
		"""
		input_variables = self.get_login_form_variables()
		for var in input_variables:
			value = input_variables[var][1]
			if value == 'none':
				value = ''
			self.request_body[var] = value


# ================================= CLASS END ================================= #		








# ================================= MAIN FUNCTION ================================= #

def main():
	global logins
	global passwords

	print('Http(s) cracker started. Type \'help\' for more information.')
	while(True):
		command = input("CRACKER > ")
		if command == 'help':
			print_help()
	
		elif command == 'exit':
			exit(0)
	
		elif command == 'clear':
			clear()
	
		elif command.split(' ')[0] == 'set':
			if len(command.split(' ')) < 3:
				print('Unknown command. Type \'help\' to get command list.')
				continue
			subcommand = command.split(' ')[1]
			arg = command.split(' ')[2]
			if not arg:
				print('Error. Argument is empty.')
			if subcommand == 'target':
				target_url = arg
			if subcommand == 'login':
				logins.append(arg)
			if subcommand == 'password':
				passwords.append(arg)
			if subcommand == 'login_list':
				login_dict = open(arg, 'r')
				logins = [login.replace('\n', '') for login in login_dict]
			if subcommand == 'password_list':
				password_dict = open(arg, 'r')
				passwords = [passwd.replace('\n', '') for passwd in password_dict]
	
		elif command == 'inspect':
			if target == '': 
				print('Error: target url is not specified.');
				continue
			resp = bf.make_empty_get_request(target_url)
			if resp == None:
				continues	
			inspect_page(resp.text)
	
		elif command == 'start':
			if target == '': 
				print('Error: target url is not specified.');
				continue
			if not logins:
				print('Set login / login dictionary first.')
				continue
			if not passwords:
				print('Set password / password dictionary first.')
				continue
			start(target_url)
		else:
			print('Unknown command. Type \'help\' to get command list.')

# ================================= END OF FUNCTION ================================= #	








# ================================= APPLICATION COMMANDS ================================= #

def print_help():
	help = """
List of commands:
help - get help
clear - clear application output
set login [login] - set auth login
set login_list [path/to/dict.txt] - set login dictionary (.txt)
set password [password] - set auth password
set password_list [path/to/dict.txt] - set password dictionaty (.txt)
set target [url] - set attack target (url or ip)
start - start attack
inspect - get information about page forms that contain http requests
exit - close http cracker

* unsuccess sign is string that is stored in html code of page
  if auth request was unsuccessful.
  e.g. "Failed login attemp.", "Error. Try again.", etc.
"""
	print(help)

	
def clear():
	sys_name = platform.system()
	if sys_name == 'Windows':
		os.system('cls')
	elif sys_name == 'Linux' or sys_name == 'Unix':
		os.system('clear')



def inspect_page(html_code):
	"""
	This function parses all html_code, finds html forms there (<form method=...> ... </form>), 
	its input variables, method types, etc. Function also provides (standart output) user with 
	parsed information and return object of 'target' class that contains all parsed data.
	"""
	def convert_for_output(value):
		return '\'' + value + '\''
	print('Parsing html...\n')
	t = target(html_code)
	for i in range(len(t.html_forms)):
		form_data = hp.inspect_form(t.html_forms[i])
		t.forms_info[t.html_forms[i]] = form_data
		print('Form number: ' + str(i))
		print('Method type: ', form_data['Method'])
		print('Form action: ', form_data['Action'])
		print('Form class: ', form_data['Class'])
		print('Form variables:')
		variables = form_data['Variables']
		for name in variables:
			var_type = variables[name][0]
			value = variables[name][1]
			if value != 'none':
				value = convert_for_output(value)
			if var_type != 'none':
				var_type = convert_for_output(var_type)
			name = convert_for_output(name)
			print('\tVariable ' + name + ' has', end = ' ')
			print(var_type + ' input type and ' + value + ' value.')
	print('Done.\n')
	return t



def start(url):
	"""
	Function 'start(url)' provides:
		* page inspection
		* information about:
			** login form
			** login variable
			** password varialbe
		* generation of http request pattern
		* brute force attack ability
	"""
	resp = bf.make_empty_get_request(url)

	target = inspect_page(resp.text)
	target.cookies = resp.cookies
	target.headers = resp.headers
	if not target.url:
		target.url = url

	ask_login_form(target)
	ask_login_var(target)
	ask_password_var(target)
	target.unsuccess_sign = ask_unsuccess_sign()
	num_threads = int(ask_num_threads())
	target.generate_request_body()	

	print('Starting brute force attack.')
	#bf.brute_force(target, logins, passwords, num_threads)

# ================================= END OF COMMANDS ================================= #
	











	

# ================================= USER INPUT FUNCTIONS ================================= #

# ask user whether he wants to specify login form 
def ask_login_form(target):
	print('Guessed login form number is: ', end = ' ')
	print(target.login_form_id)
	answer = input('Specify it? (y/n) ').lower()
	if answer == 'y':
		target.login_form_id = int(input('New login form number: '))
		target.set_login_form(target.login_form_id)

# ask user whether he wants to specify login variable
def ask_login_var(target):
	print('Guessed login variable is: ' + target.login_var)
	answer = input('Specify it? (y/n) ').lower()
	if answer == 'y':
		target.login_var = input('Login variable: ')

# ask user whether he wants to specify password variable
def ask_password_var(target):
	print('Guessed password variable is: ' + target.pass_var)
	answer = input('Specify it? (y/n) ').lower()
	if answer == 'y':
		target.pass_var = input('Password variable: ')



def ask_unsuccess_sign():
	"""
	 Function asks user to set unsuccess sign. 
	 unsuccess_sign is string that is stored in html code of page
	 if auth request was unsuccessful.
	 e.g. "Failed login attemp.", "Error. Try again.", etc.
	"""
	return input('Set unsuccess sign (look help for more info): ')



# ask how many threads to use
def ask_num_threads():
	print('Default number of threads is: 3')
	answer = input('Set another number (max = 16)? (y/n) ').lower()
	if answer == 'y':
		num = int(input('Threads number: '))
		if num > 16:
			print('Error. Max number of threads: 16.')
			return ask_num_threads()
		else:
			return num
	return 3

# ================================= END OF FUNCTIONS ================================= #


	

### START PROGRAM ###
if __name__ == "__main__":
	main()
### PROGRAM FINISHED ###

