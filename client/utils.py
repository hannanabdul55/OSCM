import os
import subprocess
import platform
from os.path import expanduser

config = None

def init():
	global config
	if not config:
		config = ConfigParser.RawConfigParser()

def current_path():
	return os.getcwd()

def get_version(software):
	output = subprocess.check_output( 
		software,
		stderr = subprocess.STDOUT, shell=True)
	if "command" in output:
		return "0"
	else:
		return output.strip()
def get_node_version():
	return get_version("node -v")

def get_python_version():
	return get_version("python --version")

def get_os():
	return platform.system().lower()

def get_arch():
	return platform.architecture()[0]

def getProperty(section, propertyName):
	init()
	prop = None
	if os.path.isfile('config.oscm'):
		config.read('config.oscm')
		try: 
	    	prop = config.get(section, propertyName)
	    except ConfigParser.NoSectionError:
	    	config.add_section(section)
	    	prop = getProperty(section, propertyName) 
		except ConfigParser.NoOptionError:
			pass
	return prop

def setProperty(section, propertyName, value):
	init()
	try:
		config.set(section, propertyName, value)
	except ConfigParser.NoSectionError:
		config.add_section(section)
		setProperty(section, propertyName, value)
	with open('config.oscm', 'wb') as configfile:
		config.write(configfile)

if __name__ == '__main__':
	print get_os()
	print current_path()
	print get_arch()
	print get_python_version()
	print get_node_version()
