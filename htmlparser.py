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

### RegExp module ###
import re
### END MODULE ###


def get_forms(html_code):
	"""
	 get list of forms (<form method=* ...> ... </form>) 
	 that contain some http request
	"""
	forms = []
	for match in re.finditer("<form.*\n?method", html_code):
		begin_index = match.start()
		end_index = html_code.find("</form>", begin_index) + 7
		form = html_code[begin_index:end_index]
		forms.append(form)
	return forms;


def get_html_variable_value(var, html_code):
	"""
	 e.g. <input name="smth" value="0">
	 if input var = 'smth' then function output = 'variable'
	 if input var = 'value' then function output = '0'
	"""
	end_pattern = re.compile("(\'|\")")
	value_index = html_code.find(var + '=')
	if value_index == -1:
		return -1
	value_index = value_index + len(var) + 2
	end_index = end_pattern.search(html_code, value_index).start()
	value = html_code[value_index:end_index]
	return value



def get_input_tags(html_form):
	"""
	 get list of <input ... > tags in html form
	"""
	input_tags = []
	for match in re.finditer("<input", html_form):
		end_pattern = re.compile('/?>')
		begin_index = match.start()
		end_index = end_pattern.search(html_form, begin_index).start()
		tag = html_form[begin_index : end_index + 2]
		input_tags.append(tag)
	return input_tags



def get_input_type(input_tag):
	"""
	 e.g. if input_tag = '<input type="hidden" name="smth" value="0">'
	 function will return 'hidden'
	"""
	input_type = get_html_variable_value('type', input_tag)
	return input_type



def get_input_variable_name(input_tag):
	"""
	 e.g. if input_tag = '<input name="smth" value="0">'
	 function will return 'smth'
	"""
	name = get_html_variable_value('name', input_tag)
	return name



def get_input_variable_value(input_tag):
	"""
	 e.g. if input_tag = '<input name="smth" value="0">'
	 function will return '0'
	"""
	value = get_html_variable_value('value', input_tag)
	return value



def get_form_method(html_form):
	"""
	 e.g. if html_form = '<form method="post"> ... </form>'
	 function will return 'post'
	"""
	method = get_html_variable_value('method', html_form)
	return method



def get_form_action(html_form):
	"""
	 e.g. if html_form = '<form method="post" action="/index.php"> ... </form>'
	 function will return '/index.php'
	"""
	action = get_html_variable_value('action', html_form)
	return action



def get_form_class(html_form):
	"""
	 e.g. if html_form = '<form class="some_form"> ... </form>'
	 function will return 'someform'
	"""
	form_class = get_html_variable_value('class', html_form)
	return form_class



# e.g. if input_tags = ['<input type="hidden" name="var1" value="0">', '<input type="hidden" name="var2">]
# function will return { 'var1' : ['hidden', '0'], 'var2' : ['hidden', 'none'] }
def get_input_variables(input_tags):
	"""
	 e.g. if input_tags = ['<input type="hidden" name="var1" value="0">', '<input type="hidden" name="var2">]
	 function will return { 'var1' : ['hidden', '0'], 'var2' : ['hidden', 'none'] }
	"""
	variables = { }
	for tag in input_tags:
		name = get_input_variable_name(tag)
		if name == -1:
			continue
		value = get_input_variable_value(tag)
		if value == -1 or value == '':
			value = 'none'
		input_type = get_input_type(tag)
		if input_type == -1 or input_type == '':
			input_type = 'none'
		variables[name] = [input_type, value]
	return variables
		
		
def inspect_form(html_form):
	"""
	 e.g. we have such html_form:
	 <form method="POST" class="log_form">
		<input name="login" type="text"/>
		<input name="password" type="password"/>
		<input name="csrf_token" value="token" type="hidden"/>
	 </form>
	 In that case function would return:
	{ 
	'Method': 'POST',
	'Class': 'log_form',
	'Action': 'none',
	'Variables' : { 
			'login': ['text', 'none'],
			'password': ['password', 'none'],
			'csrf_token': ['hidden', 'token']
	      	       }
	  }
	"""
 
	form_data = { }
	input_tags = get_input_tags(html_form)
	input_variables = get_input_variables(input_tags)
	form_method = get_form_method(html_form)
	form_action = get_form_action(html_form)
	form_class = get_form_class(html_form)
	if form_class != -1:
		form_data['Class'] = form_class
	else:
		form_data['Class'] = 'none'
	if form_action != -1:
		form_data['Action'] = form_action
	else:
		form_data['Action'] = 'none'
	form_data['Method'] = form_method
	form_data['Variables'] = input_variables
	return form_data



def guess_login_form(html_forms):
	"""
	 finds all matches of keywords (password, login, etc.)
	 and returns form_id (its position in html_forms list)
	 of form that have max number of matches
	"""
	pattern = "(password|login|username|pass|signin|user|.?mail)"
	guessed_form_id = -1
	max_matches = 0
	for form_id in range(len(html_forms)):
		matches = len(re.findall(pattern, html_forms[form_id], re.IGNORECASE))
		if matches > max_matches:
			max_matches = matches
			guessed_form_id = form_id
	return guessed_form_id

def guess_login_variable(input_variables):
	pattern = "(log|login|username|user|name|.?mail)"
	for var in input_variables:
		match = re.search(pattern, var, re.IGNORECASE)
		if match != None and input_variables[var][0].lower() != 'hidden':
			return var
	return 'no variable found'
		
def guess_pass_variable(input_variables):
	pattern = "(pass|pawd|pd|pwd)"
	for var in input_variables:
		match = re.search(pattern, var, re.IGNORECASE)
		if match != None or input_variables[var][0] == 'password':
			return var
	return 'no variable found'
