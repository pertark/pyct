import click
import requests

@click.command("search", help="search ")
@click.argument("company", nargs=-1)
def search(company):
  click.echo(str(len(company)))

def load():
  return [search]
