import os
import click
import requests
import utils
from git import Repo
import ConfigParser
import gzip
import tarfile
import zipfile

conf = None
conf_path = "conf/config.oscm"
bak_path = "conf/config.bak"

def init():
    global conf, conf2
    if not conf or not conf2:
        conf = ConfigParser.RawConfigParser()
        conf2 = ConfigParser.RawConfigParser()

def compare():
    global conf_path, bak_path
    #utils.create_backup(conf_path)
    #subprocess.call("git pull", shell=True)
    init()
    conf.read(conf_path)
    original_secs = conf.sections()
    print 'original_secs'
    print original_secs
    conf2.read(bak_path)
    updated_secs = conf2.sections()
    print 'updated_secs'
    print updated_secs
    for sec in updated_secs:
        print sec
        if sec not in original_secs:
            print 'abdul bc will write install thingy for software ' + sec
            #download_sec_install_add_plugins()
        if sec.strip() == 'eclipse':
            plugins = conf.get(sec,"plugins").split(",")
            if conf.has_option(sec,"plugins"):
                plugins = conf.get(sec,"plugins").split(",")
                if conf2.has_option(sec,"plugins"):
                    new_plugins = conf2.get(sec,"plugins").split(",")
                    for p in new_plugins:
                        if p not in plugins:
                            print 'abdul bc will write install thingy for plugin ' + p
                else:
                    #remove plugins
                    pass

def pull(repo=None):
    global conf
    init()
    # cfg file exists
    if os.path.isfile(conf_path):
        compare()
        conf.read(conf_path)
        parse_config(conf)
    elif not repo :
        Repo.clone_from(repo,"conf")
        if os.path.isfile(conf_path):
            conf.read(conf_path)
            parse_config(conf)

def download_file(url):
    r = requests.get(url, stream=True)
    ret = ""
    if r.status_code == 200:
        with open(os.path.basename(software["url"]), 'wb') as f:
            for chunk in r:
                f.write(chunk)
            ret = f.name
    return ret

def parse_config(config_file):
    secs = config_file.sections()
    v = "0"
    for sec in secs:
        if config_file.has_option(sec,"version"):
            v = config_file.get(sec,"version")
        os = utils.get_os()
        arch = utils.get_arch()
        d = utils.get_info({
            "name" : sec,
            "os" : os,
            "version" : v,
            "arch" : arch
        })
        os.mkdir(sec)
        for software in d:
            if len(software["url"])>0:
                print 'Downloading ' +sec +'...'
                r = requests.get(software["url"], stream=True)
                if r.status_code == 200:
                    with open(os.path.basename(software["url"]), 'wb') as f:
                        for chunk in r:
                            f.write(chunk)
                        if tarfile.is_tarfile(f.name):
                            tfile = tarfile.open(os.path.basename(software["url"]), "r:gz")
                            tfile.extractall(sec)
                        elif zipfile.is_zipfile(f.name):
                            z = zipfile.ZipFile(f)
                            z.extractall(sec)
                else:
                    print 'Error downloading package, Please download ' + sec + ' on your own!'
        if sec == 'eclipse':
            if config_file.has_option(sec,"plugins"):
                plugins = config_file.get(sec,"plugins").split(",")
                if os.path.isdir(os.path.join(os.getcwd(),sec,"dropins")):
                    for plugin in plugins:
                        f = download_file(plugin)
                        if len(f)>0 and zipfile.is_zipfile(f):
                            z = zipfile.ZipFile(open(f,"rb"))
                            z.extractall(os.path.join(os.getcwd(),sec,"dropins"),os.path.splitext(f)[0])
        