import click
<<<<<<< HEAD
from click.testing import CliRunner
import requests
import urllib

endpoint_url = "http://52.34.230.77:9123/backend/"
put = "put/?"
get = "get/?"

=======
import initialize
>>>>>>> 8b4abac8d7db134fddb2c01fcec721556e5de50c
@click.group()
def cli():
    pass

@cli.command()
@click.option('--name', '-n', 'name',
    prompt = 'Enter the software name',
    help='The software name',
    required=True)
@click.option('--version', '-v', 'version',
    prompt = 'Enter the software version',
    help='Version number, not version name',
    required=True)
@click.option('--url', '-u', 'url',
    prompt = 'Enter the download url, press n for none',
    help = 'The url which points to download binary for a particular OS and architecture.')
@click.option('--os', '-o', 'os',
    prompt = 'Enter the os for which the url/command is valid',
    help = 'Operating System name; darwin for macs, linux and windows; for which \
        for which the download url/command is pointing to.',
    required=True)
@click.option('--cmd', '-c', 'cmd',
    prompt = 'Enter the install command, press n for none',
    help = 'The install command like npm module name or \"apt-get xyz\" or \"pip install xyz\"')
@click.option('--tag', '-t', 'tag',
    prompt = 'Enter the tag for software, enter comma seperated tags for multiple values',
    help = 'Tags are used to help prompt for softwares under a category\n \
            Example : JDK, JRE etc will come under java tag\n \
            Enter multiple tags by seperating them with commas, making sure no\
            space is added before or after the comma.')
@click.option('--architecture', '-a', 'arch',
    prompt = 'Enter the architecture for which the download url/command is pointing to.\n \
            Enter `both` for both x86 and 64 bit., 32 for 32 bit and 64 for 64 bit.',
    help = '32 bit or 64 bit; x86 is 32 bit.',
    required=True)
def addsoftware(name=None, version=None, url=None, os=None, cmd=None, tag=None, arch=None):
    print name, version, url, os, cmd, tag, arch
    add_software(name, version, url, os, cmd, tag, arch)

def add_software(name=None, version=None, url=None, os=None, cmd=None, tag=None, arch=None):
    global endpoint_url, put
    endpoint = endpoint_url + put
    params = {"name": name, "version": version, "os": os, "arch": arch, "command": cmd, "url": url, "tag": tag}
    params = dict((k,v) for k,v in params.items() if v.lower() != 'n')
    response = requests.get("%s%s" %(endpoint, urllib.urlencode(params)))
    print_status(response) 



@cli.command()
def init():
    initialize.initialize()

def print_status(response):
    if response.status_code == 201:
        click.echo("Software added successfully.")
    else:
        click.echo("Software wasn't added. Network error.")

def call_command(cmdname):
    runner = CliRunner()
    result = runner.invoke(cli, [cmdname])
    return result.output.strip()