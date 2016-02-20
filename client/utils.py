import ConfigParser
import os
import subprocess
import platform

import requests

config = None
API_ENDPOINT = "http://52.34.230.77:9123/backend"


def init():
    global config
    if not config:
        config = ConfigParser.RawConfigParser()


def current_path():
    return os.getcwd()


def get_version(software):
    output = subprocess.check_output(
        software,
        stderr=subprocess.STDOUT, shell=True)
    if "command" in output:
        return "0"
    else:
        return output.strip()


def install_python_package(package_name):
    output = subprocess.check_output(
        "pip install %s" % package_name,
        stderr=subprocess.STDOUT, shell=True)
    if "No matching distribution" in output:
        return False
    else:
        return True


def install_node_package(package_name):
    output = subprocess.check_output(
        "npm install %s" % package_name,
        stderr=subprocess.STDOUT, shell=True)
    if "ERR!" in output:
        return False
    else:
        return True


def get_node_version():
    return get_version("node -v")


def get_python_version():
    return get_version("python --version")


def search_by_tag(tag):
    """
    Searches the database by tag.
    :param tag:
    :return: a list of dictionaries.
            Each dictionary represents one software configuration.
            If nothing is found, returns an empty list.
            If status is not 200 OK, returns None
    """
    response = requests.get("%s/search/?tag=%s" % (API_ENDPOINT, tag))
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_os():
    return platform.system().lower()


def get_arch():
    return platform.architecture()[0]


def get_property(section, property_name):
    init()
    prop = None
    if os.path.isfile('config.oscm'):
        config.read('config.oscm')
        try:
            prop = config.get(section, property_name)
        except ConfigParser.NoSectionError:
            config.add_section(section)
            prop = get_property(section, property_name)
        except ConfigParser.NoOptionError:
            pass
    return prop

def add_section(section_name):
    try:
        if os.path.isfile('config.oscm'):
            config.read('config.oscm')
            config.add_section(section_name)
    except:
        pass

def set_property(section, property_name, value):
    init()
    try:
        config.set(section, property_name, value)
    except ConfigParser.NoSectionError:
        config.add_section(section)
        set_property(section, property_name, value)
    with open('config.oscm', 'wb') as configfile:
        config.write(configfile)


if __name__ == '__main__':
    # print get_os()
    # print current_path()
    # print get_arch()
    # print get_python_version()
    # print get_node_version()
    # print search_by_tag("py")
    print install_python_package("fuzzywuzzy")
