import os
import click
from utils import current_path


@click.command()
@click.option('--repo', '-r', 'repo',
              prompt='Enter the repo clone URL',
              help='The repo clone URL')
def pull():
    pass
