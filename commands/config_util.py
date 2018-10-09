#
# Config Util
# 
import os
import json
import fileinput

def load_config():
	with open('config.json') as data_file:
		data = json.load(data_file)
	return data

def save_config(json_data):
	with open('config.json', 'w') as data_file:
		data_file.write(json.dumps(json_data, indent=2, sort_keys=True))

def get_slack_root():
	return load_config()['slack']['root']

def set_slack_root_id(id):
	json_data = load_config()
	json_data['slack']['root']['id'] = id
	save_config(json_data)

def get_slack_admins():
	return load_config()['slack']['admins']

def add_slack_admin(id, username):
	json_data = load_config()
	admins = json_data['slack']['admins']
	for admin in admins:
		if admin['id'] == id:
			return 'Error: User is already set as an admin.'
	count = len(admins)
	admins[count]['id'] = id
	admins[count]['username'] = username
	json_data['slack']['admins'] = admins
	save_config(json_data)

def remove_slack_admin(username):
	json_data = load_config()
	admins = json_data['slack']['admins']
	for admin in admins:
		if admin['username'] == username:
			admins.remove(admin)
	json_data['slack']['admins'] = admins
	save_config(json_data)

def set_slack_admin_id(username, id):
	json_data = load_config()
	admins = json_data['slack']['admins']
	for admin in admins:
		if admin['username'] == username:
			admin['id'] = id
	json_data['slack']['admins'] = admins
	save_config(json_data)
	
def get_slack_server_channel():
	return load_config()['slack']['channels']['server']

def set_slack_server_channel(name, id):
	json_data = load_config()
	server_channel = json_data['slack']['channels']['server']
	server_channel['name'] = name
	server_channel['id'] = id
	json_data['slack']['channels']['server'] = server_channel
	save_config(json_data)

def get_slack_report_channel():
	return load_config()['slack']['channels']['report']

def set_slack_report_channel(name, id):
	json_data = load_config()
	report_channel = json_data['slack']['channels']['report']
	report_channel['name'] = name
	report_channel['id'] = id
	json_data['slack']['channels']['report'] = report_channel
	save_config(json_data)

def get_project():
	return load_config()['project']

def set_project_root(name, dir):
	json_data = load_config()
	project = json_data['project']
	project['name'] = name
	project['dir'] = dir
	json_data['project'] = project
	save_config(json_data)

def get_project_services():
	return load_config()['project']['services']

def get_project_service_count():
	return len(load_config()['project']['services'])

def add_project_service(dir, name, delay, order):
	currentCount = get_project_service_count()
	if order > currentCount:
		order = currentCount
	elif order < 0:
		order = 0
	json_data = load_config()
	services = json_data['project']['services']
	service = {}
	service['name'] = name
	service['dir'] = dir
	service['delay'] = delay
	services.insert(order, service)
	json_data['project']['services'] = services
	save_config(json_data)

def remove_project_service(name):
	json_data = load_config()
	services = json_data['project']['services']
	for service in services:
		if service['name'] == name:
			services.remove(service)
	json_data['project']['services'] = services
	save_config(json_data)

def get_display():
	return load_config()['display']

def set_display_terminals(height, width):
	json_data = load_config()
	terminals = json_data['display']['terminals']
	terminals['perHeight'] = height
	terminals['perWidth'] = width
	json_data['display']['terminals'] = terminals
	save_config(json_data)

def set_display_window(top, right, bottom, left):
	json_data = load_config()
	window = json_data['display']['window']
	window['topPadding'] = top
	window['rightPadding'] = right
	window['bottomPadding'] = bottom
	window['leftPadding'] = left
	json_data['display']['window'] = window
	save_config(json_data)

def calculate():
	project = get_project()
	display = get_display()
	terminals = display['terminals']
	servicesCount = len(project['services'])
	terminalsCount = terminals['perHeight'] * terminals['perWidth']
	if servicesCount > terminalsCount:
		print('Warning: Services outnumber Terminals, some terminals will be hidden')
	window = display['window']
	monitor = display['monitor']
	w_width = monitor['width'] - window['rightPadding']
	w_height = monitor['height'] - window['bottomPadding']
	t_width = w_width / terminals['perWidth'] / 10
	t_height = w_height / terminals['perHeight'] / 30
	col = 0
	row = terminals['perHeight'] - 1
	for index, service in enumerate(project['services']):
		project['services'][index]['t_x'] = col * t_width * 10
		project['services'][index]['t_y'] = row * t_height * 30
		col = col + 1
		if col >= terminals['perWidth']:
			col = 0
			row = row - 1
	project['t_size'] = {}
	project['t_size']['width'] = t_width
	project['t_size']['height'] = t_height

	config = load_config()
	config['project'] = project
	save_config(config)
