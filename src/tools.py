"""Reverse proxy for Next Bus server"""
from ConfigParser import ConfigParser
import requests 

def load_config(path):
#    """Load config from a config file"""
	config = ConfigParser()
	try:
		config.read(path)
	except Exception as e:
		print("Bad configuration file name %s %s" % (path, e))

	config_dict = {s:dict(config.items(s)) for s in config.sections()}

	return config_dict

def http_request(url):
    """Makes the Https requests"""
    headers = {'accept': 'application/xml;q=0.9, */*;q=0.8'}
    response = requests.get(url, headers=headers)
    return response.text 

if __name__ == '__main__':
	print load_config("../config.ini")
	config_dict  = load_config(path)
 
