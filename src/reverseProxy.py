"""Reverse proxy for Next Bus server"""
from ConfigParser import ConfigParser

def load_config(path):
	"""Load config from a config file"""
	config = ConfigParser()
	try:
		config.read(path)
	except Exception as e:
		print("Bad configuration file name %s %s" % (path, e))

	config_dict = {s:dict(config.items(s)) for s in config.sections()}

	return config_dict
		 
if __name__ == '__main__':
	print load_config("../config.ini")
 
