import click

@click.group()
def cli():
    pass

@cli.command()
@click.option('--name', '-n', 'name',
    prompt = 'Enter the software name',
    help='The software name')
@click.option('--version', '-v', 'version',
    prompt = 'Enter the software version',
    help='Version number, not version name')
@click.option('--url', '-u', 'url',
    prompt = 'Enter the download url, press n for none',
    help = 'The url which points to download binary for a particular OS and architecture.')
@click.option('--os', '-o', 'os',
    prompt = 'Enter the os for which the url/command is valid',
    help = 'Operating System name; darwin for macs, linux and windows; for which \
        for which the download url/command is pointing to.')
@click.option('--cmd', '-c', 'cmd',
    prompt = 'Enter the install command, press n for none',
    help = 'The install command like npm module name or \"apt-get xyz\" or \"pip install xyz\"')
@click.option('--tag', '-t', 'tag',
    prompt = 'Enter the tag for software, enter comma seperated tags for multiple values',
    help = 'Tags are used to help prompt for softwares under a category\n \
            Example : JDK, JRE etc will come under java tag\n\
            Enter multiple tags by seperating them with commas, making sure no\
            space is added before or after the comma.')
@click.option('--architecture', '-a', 'arch',
    prompt = 'Enter the architecture for which the download url/command is pointing to.\
        Enter n for both x86 and 64 bit.',
    help = '32 bit or 64 bit')
def addsoftware(name=None, version=None, url=None, os=None, cmd=None, tag=None, arch=None):
    print name, version, url, os, cmd, tag, arch
    add_software(name, version, url, os, cmd, tag, arch)

def add_software(name=None, version=None, url=None, os=None, cmd=None, tag=None, arch=None):
    print 'calling like a boss'

@cli.command()
def dummy():
    print "Hey"



#addsoftware(name="CallTest", version="None", url="None", os="None", cmd="hi", tag="great", arch="64")