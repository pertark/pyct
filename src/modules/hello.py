import click
from colors import Colors as c

@click.command("hello", help="Greets you")
@click.option("--name", "-n", help="The person to greet", required=False)
def hello(name):
  if name:
    click.echo(c.BOLD + c.LIGHT_CYAN + 'Hello %s!' % name + c.END)
  else:
    click.echo(c.BOLD + c.LIGHT_CYAN + "Hello world!" + c.END)


def load():
  return [hello]
