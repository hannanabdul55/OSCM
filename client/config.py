import ConfigParser

def getProperty(section, propertyName):
   prop = None
   if os.path.isfile('deploy.cfg'):
      config.read('deploy.cfg')
      try: 
         prop = config.get(section, propertyName)
      except ConfigParser.NoSectionError:
         config.add_section(section)
         prop = getProperty(section, propertyName) 
      except ConfigParser.NoOptionError:
         pass
   return prop

def setProperty(section, propertyName, value):
   try:
      config.set(section, propertyName, value)
   except ConfigParser.NoSectionError:
      config.add_section(section)
      setProperty(section, propertyName, value)    
   with open('deploy.cfg', 'wb') as configfile:
      config.write(configfile)