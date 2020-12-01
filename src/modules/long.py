import click
from colors import Colors as c
import requests
import json

@click.command("long", help="Gives all redirects from a URL")
@click.argument("url")
def long(url):
  try:
    response = requests.get(url)
    if response.history:
      click.echo(c.BLUE + c.BOLD + "Original: " + c.END + c.BLUE + c.UNDERLINE + url + c.END)
      for resp in range(len(response.history)):
        if resp != 0:
          click.echo(c.LIGHT_GREEN + c.BOLD + "Redirect: " + c.END + c.BLUE + c.UNDERLINE + response.history[resp].url + c.END)
      click.echo(c.GREEN + c.BOLD + "Final: " + c.END + c.BLUE + c.UNDERLINE + response.url + c.END)
    else:
      click.echo(c.RED + c.BOLD + "URL was not redirected. " + c.END)
  except requests.exceptions.MissingSchema:
    click.echo(c.RED + c.BOLD + "Invalid URL. ")

def load():
  return [long]