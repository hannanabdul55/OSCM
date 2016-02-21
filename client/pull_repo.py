import os
import click
import requests
import utils
from git import Repo
import ConfigParser
import gzip
import tarfile
import zipfile
import subprocess

def pull(repo=None):
    if repo != None:
        Repo.clone_from(repo,"conf")
        conf = ConfigParser.RawConfigParser()
        if os.path.isfile('conf/config.oscm'):
            conf.read('conf/config.oscm')
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
        OS = utils.get_os()
        arch = utils.get_arch()
        d = utils.get_info({
            "name" : sec,
            "os" : OS,
            "version" : v,
            "arch" : arch
        })
        for software in d:
            if len(software["url"])>0:
                if os.path.isfile(os.path.basename(software["url"])):
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
                else:
                    print sec + ' already present in folder, extracting...'
                subprocess.call(['tar','-xvf',os.path.basename(software["url"])])
        if not os.path.exists(sec):
            os.mkdir(sec)
        if sec == 'eclipse':
            if config_file.has_option(sec,"plugins"):
                plugins = config_file.get(sec,"plugins").split(",")
                if os.path.isdir(os.path.join(os.getcwd(),sec,"dropins")):
                    for plugin in plugins:
                        f = download_file(plugin)
                        if len(f)>0 and zipfile.is_zipfile(f):
                            z = zipfile.ZipFile(open(f,"rb"))
                            z.extractall(os.path.join(os.getcwd(),sec,"dropins"),os.path.splitext(f)[0])
        