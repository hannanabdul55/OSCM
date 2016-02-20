import os
import click
import utils
from git import Repo
import ConfigParser


def pull(repo=None):
    if repo != None:
        Repo.clone_from(repo,"conf")
        conf = ConfigParser.RawConfigParser()
        if os.path.isfile('conf/config.oscm'):
            conf.read('conf/config.oscm')
            parse_config(conf)

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