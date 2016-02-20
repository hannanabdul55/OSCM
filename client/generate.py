from glob import glob
import utils
import os
SOFTWARE_CONFIG_NAME = "package.oscm"
def app_list_filter(item):
    return not (str(item).startswith(".") or str(item) == "node_modules")

def generate(initial=True):
    #get system config
    app_list = [p[:-1] for p in glob('*/') ]
    app_list = filter(app_list_filter,app_list)
    for app in app_list:
        app_ret = Application()
        app_ret.resolve(app)
        utils.add_section(app)
        utils.set_property(app_ret.name,"version",app_ret.version)
    



def determine_version(app):
    application = get_app(app)
    
def fetch_conf_dict(f_name):
    ret = {}
    f = open(f_name,"r")
    f_lines = map(lambda x : list(x.strip().split(",")),f.readlines())
    for i in f_lines:
        ret[str(i[0])] = str(i[1])
    return ret


def get_app(name):
    pass
    
def eclipseVersion(name):
    v_path = os.path.join(os.getcwd(),name,".eclipseproduct")
    if not os.path.isfile(v_path):
        return "0"
    else:
        return filter(lambda x : x[0] == "version",map(lambda x: x.strip().split("="),open(v_path,"r").readlines()))[0][1]
        #return str(list(filter( lambda a: a[0] == "version" , list(map(lambda x: x.strip().split("="),open(v_path,"r").readlines()))))[1])
    
def intellijVersion(name):
    return "0"
    
def perforceVersion(name):
    return "0"
    
def studioVersion(name):
    return "0"

class Application:
    """A class specifying what application it is"""
    applist = ["eclipse","intellij","perforce","android_studio"]
    appVersionFinder = {
        "eclipse": eclipseVersion,
        "intellij" : intellijVersion,
        "perforce" : perforceVersion,
        "android_studio": studioVersion
    }
    
    def __init__(self):
        self.name = ""
        self.version = "0"
        self.is_custom = False
    
    def set_version(self,version):
        self.version = version
    
    def resolve_version(self,name):
        self.version = self.appVersionFinder.get(self.name,lambda x: "0")(name)
    def resolve(self,name):
        a = list(filter(lambda x : x in name,self.applist))
        if len(a)>0:
            self.name = a[0]
            self.resolve_version(name)
        else:
            conf_file = os.path.join(os.getcwd(),name,SOFTWARE_CONFIG_NAME)
            if os.path.isfile(conf_file):
                con = fetch_conf_dict(conf_file)
                self.is_custom = True
                self.custom_conf = con
                self.name = con['name']
                self.version = con['version']
                #TODO: Add into db @narendranathjoshi
            else:
                #TODO: prompt by @ravisvi
                print "RAVI BC! Complete Kar"

if __name__ == "__main__":
    generate()