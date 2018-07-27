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

### TODO ###
# * read query string - done
# * let user set whole http request without parsing html - done
# * rewrite commands - done (commands removed)
# * add argparse - done
# * add colors
### END TODO ###



### IMPORT MODULES ###
import bruteforce as bf
import argparse
### END MODULES ###




# ================================= TARGET_INFO CLASS ==================== #
"""
Class TargetInfo stores information about target website
for brute force attack (url, login variable name, etc.)
It also provides substitute login/password functions for dictionary attack
"""

class TargetInfo:
	def __init__(self):
		self.url = str()
		self.login_var_name = str()
		self.password_var_name = str()
		self.unsuccess_sign = str()

# ================================= CLASS END ================================ #





# ================================= MAIN FUNCTION =========================== #
def main(args):
	# get args' values #
	logins, passwords = [], []
	login = args['l']
	login_dict_path = args['L']
	password = args['p']
	password_dict_path = args['P']
	num_threads = 1
	url = args['target']
	reverse = args['reverse']


	# set brute force login(s) #
	if login_dict_path:
		login_dict = open(login_dict_path, 'r')
		logins = [login.replace('\n', '') for login in login_dict]
	elif login:
		logins.append(login)

	# set brute force password(s) #
	if password_dict_path:
		password_dict = open(password_dict_path, 'r')
		passwords = [passwd.replace('\n', '') for passwd in password_dict]
	elif password:
		passwords.append(password)

	# specify number of threads to use #
	if 't' in args:
		num_threads = args['t']


	print('Starting brute force attack.')
	# generating TargetInfo with user input #
	target_info = get_target_info()
	target_info.url = url

	# brute force attack #
	bf.brute_force(target_info, logins, passwords, num_threads, reverse)



# ================================= END OF FUNCTION ========================== #








# ================================= APPLICATION COMMANDS ===================== #

def ask_failure_sign():
	"""
	 Function asks user to set failure sign.
	 failure_sign is string that is stored in html code of page
	 if auth request was unsuccessful.
	 e.g. "Failed login attemp.", "Error. Try again.", etc.
	"""
	return input('Set failure sign (look help for more info): ')

def ask_login_var():
	login_var = input('Login variable: ')
	return login_var

def ask_password_var():
	pass_var = input('Password variable: ')
	return pass_var

def get_target_info():
	"""
	Get information about attack target:
		* login varaible name,
		* password variable name,
		* failure sign.
	And return object of TargetInfo class.
	"""
	info = TargetInfo()
	info.login_var_name = ask_login_var()
	info.password_var_name = ask_password_var()
	info.failure_sign = ask_failure_sign()
	return info

# ================================= END OF COMMANDS ========================== #




# ================================ DEFINE ARGS =============================== #
def define_args():
	parser = argparse.ArgumentParser(prog = 'cracker')

	login_group = parser.add_mutually_exclusive_group(required = True)
	define_login_group(login_group)
	password_group = parser.add_mutually_exclusive_group(required = True)
	define_password_group(password_group)

	parser.add_argument('-t'
						, metavar = 'THREADS'
						, type = int
						, default = 1
						, help = 'set number of threads to use (default: 3)')

	parser.add_argument('target'
						, help = 'set target website (specify login action)' \
						' e.g. https://target.com/login.php')

	parser.add_argument('--reverse'
						, '-r'
						, action = 'store_true'
						, help = 'set brute force attack type')
	return parser


def define_login_group(login_group):
		login_group.add_argument('-l'
								, metavar = 'LOGIN'
								, help = 'set attack login')

		login_group.add_argument('-L'
		 						, metavar = 'dict.txt'
								, help = 'set login dictionary')


def define_password_group(password_group):
		password_group.add_argument('-p'
									, metavar = 'PASSWORD'
									, help = 'set attack password')

		password_group.add_argument('-P'
									, metavar = 'dict.txt'
									, help = 'set password dictionary')

# ================================= END ARGS ================================= #



### START PROGRAM ###
if __name__ == "__main__":
	parser = define_args()
	args = vars(parser.parse_args())
	main(args)
### PROGRAM FINISHED ###
