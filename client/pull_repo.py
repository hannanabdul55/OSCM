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

conf = None
conf_path = "config.oscm"
bak_path = "config.bak"


def init():
    global conf, conf2
    if not conf or not conf2:
        conf = ConfigParser.RawConfigParser()
        conf2 = ConfigParser.RawConfigParser()


def compare():
    global conf_path, bak_path
    # utils.create_backup(conf_path)
    init()
    conf.read(conf_path)
    original_secs = conf.sections()
    print 'original_secs'
    print original_secs
    subprocess.call("git pull", shell=True)
    conf2.read(conf_path)
    updated_secs = conf2.sections()
    print 'updated_secs'
    print updated_secs
    for sec in updated_secs:
        print sec
        if sec not in original_secs:
            download_sec(sec, conf2)
        if sec.strip() == 'eclipse':
            plugins = conf.get(sec, "plugins").split(",")
            if conf.has_option(sec, "plugins"):
                plugins = conf.get(sec, "plugins").split(",")
                if conf2.has_option(sec, "plugins"):
                    new_plugins = conf2.get(sec, "plugins").split(",")
                    for p in new_plugins:
                        if p not in plugins:
                            if sec == 'eclipse':
                                if conf2.has_option(sec, "plugins"):
                                    plugins = conf2.get(sec, "plugins").split(
                                        ",")
                                    if os.path.isdir(
                                            os.path.join(os.getcwd(), sec,
                                                         "dropins")):
                                        for plugin in plugins:
                                            f = download_file(plugin)
                                            if len(
                                                    f) > 0 and zipfile.is_zipfile(
                                                    f):
                                                z = zipfile.ZipFile(
                                                    open(f, "rb"))
                                                path = os.path.join(os.getcwd(),
                                                                    "eclipse",
                                                                    "dropins",
                                                                    os.path.splitext(
                                                                        f)[0])
                                                if not os.path.exists(path):
                                                    os.makedirs(path)
                                                z.extractall(path)
                else:
                    pass
    os.remove(bak_path)


def download_sec(sec, config_file):
    v = "0"
    if config_file.has_option(sec, "version"):
        v = config_file.get(sec, "version")
    OS = utils.get_os()
    arch = utils.get_arch()
    d = utils.get_info({
        "name": sec,
        "os": OS,
        "version": v,
        "arch": arch
    })
    for software in d:
        if len(software['command']) > 0:
            subprocess.call(software['command'], shell=True)
        elif len(software["url"]) > 0:
            if os.path.isfile(os.path.basename(software["url"])):
                print 'Downloading ' + sec + '...'
                r = requests.get(software["url"], stream=True)
                if r.status_code == 200:
                    with open(os.path.basename(software["url"]), 'wb') as f:
                        for chunk in r:
                            f.write(chunk)
                        if tarfile.is_tarfile(f.name):
                            tfile = tarfile.open(
                                os.path.basename(software["url"]), "r:gz")
                            tfile.extractall(sec)
                        elif zipfile.is_zipfile(f.name):
                            z = zipfile.ZipFile(f)
                            z.extractall(sec)
                else:
                    print 'Error downloading package, Please download ' + sec + ' on your own!'
            else:
                print sec + ' already present in folder, extracting...'
            print 'Running command ' + str(
                ['tar', '-xvf', os.path.basename(software["url"])])
            subprocess.call(['tar', '-xvf', os.path.basename(software["url"])])


def pull(repo=None):
    global conf, conf_path
    init()
    # cfg file exists
    if os.path.isfile(conf_path) or os.path.exists(".git"):
        compare()
        conf.read(conf_path)
        parse_config(conf)
    else:
        print 'Downloading repo'
        subprocess.call('git clone ' + repo, shell=True)
        # todo: Bro
        conf_path = os.path.join(os.path.basename(repo).split('.git')[0],
                                 conf_path)
        print conf_path
        if os.path.isfile(conf_path):
            conf.read(conf_path)
            parse_config(conf)


def download_file(url):
    r = requests.get(url, stream=True)
    ret = ""
    if r.status_code == 200:
        with open(os.path.basename(url), 'wb') as f:
            for chunk in r:
                f.write(chunk)
            ret = f.name
    return ret


def parse_config(config_file):
    secs = config_file.sections()
    v = "0"
    for sec in secs:
        if config_file.has_option(sec, "version"):
            v = config_file.get(sec, "version")
        OS = utils.get_os()
        arch = utils.get_arch()
        d = utils.get_info({
            "name": sec,
            "os": OS,
            "version": v,
            "arch": arch
        })
        print d, str({"name": sec, "os": OS, "version": v, "arch": arch})
        for software in d:
            if len(software.get('command', '')) > 0:
                subprocess.call(software['command'], shell=True)
            elif len(software["url"]) > 0:
                print software["url"]
                if not os.path.isfile(os.path.basename(software["url"])):
                    print 'Downloading ' + sec + '...'
                    r = requests.get(software["url"], stream=True)
                    if r.status_code == 200:
                        with open(os.path.basename(software["url"]), 'wb') as f:
                            for chunk in r:
                                f.write(chunk)
                            # if tarfile.is_tarfile(f.name):
                            #     tfile = tarfile.open(os.path.basename(software["url"]), "r:gz")
                            #     tfile.extractall(sec)
                            # elif zipfile.is_zipfile(f.name):
                            #     z = zipfile.ZipFile(f)
                            #     z.extractall(sec)
                            subprocess.call('tar -xvf ' + f.name, shell=True)
                    else:
                        print 'Error downloading package, Please download ' + sec + ' on your own!'
                else:
                    print sec + ' already present in folder, extracting...'
                subprocess.call('tar -xvf ' + os.path.basename(software["url"]),
                                shell=True)
                # if tarfile.is_tarfile(os.path.basename(software["url"])):
                #     tfile = tarfile.open(os.path.basename(software["url"]), "r:gz")
                #     tfile.extractall(sec)
                # elif zipfile.is_zipfile(os.path.basename(software["url"])):
                #     z = zipfile.ZipFile(os.path.basename(software["url"]))
                #     z.extractall(sec)
        if not os.path.exists(sec):
            os.mkdir(sec)
        if sec == 'eclipse':
            if config_file.has_option(sec, "plugins"):
                plugins = config_file.get(sec, "plugins").split(",")
                if os.path.isdir(os.path.join(os.getcwd(), sec, "dropins")):
                    for plugin in plugins:
                        f = download_file(plugin)
                        if len(f) > 0 and zipfile.is_zipfile(f):
                            z = zipfile.ZipFile(open(f, "rb"))
                            path = os.path.join(os.getcwd(), "eclipse",
                                                "dropins",
                                                os.path.splitext(f)[0])
                            if not os.path.exists(path):
                                os.makedirs(path)
                            z.extractall(path)
