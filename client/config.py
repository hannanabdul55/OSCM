import ConfigParser
import os

configfile = ConfigParser.RawConfigParser()


def get_property(section, property_name):
    prop = None
    if os.path.isfile('config.oscm'):
        configfile.read('config.oscm')
        try:
            prop = configfile.get(section, property_name)
        except ConfigParser.NoSectionError:
            configfile.add_section(section)
            prop = get_property(section, property_name)
        except ConfigParser.NoOptionError:
            pass
    return prop


def add_section(section_name):
    if os.path.isfile('config.oscm'):
        configfile.read('config.oscm')
        configfile.add_section(section_name)
        return True
    else:
        return False


def set_property(section, property_name, value):
    try:
        configfile.set(section, property_name, value)
    except ConfigParser.NoSectionError:
        configfile.add_section(section)
        set_property(section, property_name, value)
    with open('config.oscm', 'wb') as configfile1:
        configfile.write(configfile1)
