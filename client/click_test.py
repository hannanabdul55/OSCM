import click
from click.testing import CliRunner


@click.command()
@click.prompt("prompt")
def command1():
    click.echo("Command 1")


def normal1():
    runner = CliRunner()
    result = runner.invoke(command1)
    return result


print normal1().output
