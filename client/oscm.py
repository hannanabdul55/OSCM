import os
import click
from click.testing import CliRunner
import requests
import urllib
import initialize
import pull_repo
import six
import subprocess
import json

endpoint_url = "http://52.34.230.77:9123/backend/"
put = "put/?"
get = "get/?"
param_file = "my_file"


@click.group()
def cli():
    pass


@cli.command()
@click.option('--name', '-n', 'name',
              prompt='Enter the software name',
              help='The software name',
              required=True)
@click.option('--version', '-v', 'version',
              prompt='Enter the software version',
              help='Version number, not version name',
              required=True)
@click.option('--url', '-u', 'url',
              prompt='Enter the download url, press n for none',
              help='The url which points to download binary for a particular OS and architecture.')
@click.option('--os', '-o', 'os',
              prompt='Enter the os for which the url/command is valid',
              help='Operating System name; darwin for macs, linux and windows; for which \
        for which the download url/command is pointing to.',
              required=True)
@click.option('--cmd', '-c', 'cmd',
              prompt='Enter the install command, press n for none',
              help='The install command like npm module name or \"apt-get xyz\" or \"pip install xyz\"')
@click.option('--tag', '-t', 'tag',
              prompt='Enter the tag for software, enter comma seperated tags for multiple values',
              help='Tags are used to help prompt for softwares under a category\n \
            Example : JDK, JRE etc will come under java tag\n \
            Enter multiple tags by seperating them with commas, making sure no\
            space is added before or after the comma.')
@click.option('--architecture', '-a', 'arch',
              prompt='Enter the architecture for which the download url/command is pointing to.\n \
            Enter `both` for both x86 and 64 bit., 32 for 32 bit and 64 for 64 bit.',
              help='32 bit or 64 bit; x86 is 32 bit.',
              required=True)
def addsoftware(name=None, version=None, url=None, os=None, cmd=None, tag=None,
                arch=None):
    add_software(name, version, url, os, cmd, tag, arch)


def add_software(name=None, version=None, url=None, os=None, cmd=None, tag=None,
                 arch=None):
    global endpoint_url, put, param_file
    endpoint = endpoint_url + put
    params = {"name": name, "version": version, "os": os, "arch": arch,
              "command": cmd, "url": url, "tag": tag}
    params = dict((k, v) for k, v in params.items() if v.lower() != 'n')
    response = requests.get("%s%s" % (endpoint, urllib.urlencode(params)))
    print_status(response)
    print params

    # save to file:
    with open(param_file, 'w') as f:
        json.dump(params, f)


@cli.command()
@click.option('--url', '-u', 'url',
              prompt='Enter the repo URL',
              help='The repo clone URL')
def init(url):
    initialize.initialize()
    subprocess.call("git init", shell=True)
    subprocess.call("git remote add origin %s" % url, shell=True)


@cli.command()
@click.option('--repo', '-r', 'repo',
              help='The repo clone URL')
def pull(repo):
    pull_repo.pull(repo)


@cli.command()
def push(repo):
    subprocess.call("git push", shell=True)


@cli.command()
@click.option('--message', '-m', 'message',
              prompt='Enter the commit message',
              help='The commit message')
def commit(message):
    subprocess.call("git add conf/config.oscm", shell=True)
    subprocess.call("git commit -m '%s'" % message, shell=True)


def tester():
    call_command('addsoftware')
    global param_file
    data = None
    with open(param_file, 'r') as f:
        try:
            data = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            data = {}
    print data


def print_status(response):
    if response.status_code == 201:
        click.echo("Software added successfully.")
    else:
        click.echo("Software wasn't added. Network error.")


def call_command(cmdname):
    '''runner = CliRunner()
    result = runner.invoke(cli, [cmdname])'''
    cmdname = 'oscm ' + cmdname
    # result,error = subprocess.Popen(cmdname,stdout = subprocess.PIPE, stderr= subprocess.PIPE).communicate()
    subprocess.call(cmdname, shell=True)

    '''if isinstance(result, six.string_types):
        return result.output.strip()    
    else:
        return result.output
        '''
