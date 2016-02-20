import ConfigParser
import os

configfile = ConfigParser.RawConfigParser()


def getProperty(section, propertyName):
   prop = None
   if os.path.isfile('config.oscm'):
      configfile.read('config.oscm')
      try: 
         prop = configfile.get(section, propertyName)
      except ConfigParser.NoSectionError:
         configfile.add_section(section)
         prop = getProperty(section, propertyName) 
      except ConfigParser.NoOptionError:
         pass
   return prop

def addSection(section_name):
    if os.path.isfile('config.oscm'):
      configfile.read('config.oscm')
      configfile.add_section(section_name)
      return True
    else:
      return False  

def setProperty(section, propertyName, value):
   try:
      configfile.set(section, propertyName, value)
   except ConfigParser.NoSectionError:
      configfile.add_section(section)
      setProperty(section, propertyName, value)    
   with open('config.oscm', 'wb') as configfile1:
      configfile.write(configfile1)