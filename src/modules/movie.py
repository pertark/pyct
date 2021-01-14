import click
import requests
import json
from colors import Colors as c

@click.command("movie", help="Get information about a movie")
@click.argument("name")
def movie(name):
  click.echo(get_profile(name))


API_KEY = '946f500a' # totally not just copied from bash snippets
def get_profile(name):
  params = {'t': name, 'apikey': API_KEY}
  p = requests.get('http://www.omdbapi.com/', params=params)
  profile = p.json()
  template = '{}: {}'
  content = ['Year','Runtime','Rated','Genre','Director','Actors','Plot']
  display = c.BOLD + 'Title: ' + profile['Title'] + c.END + '\n'
  display += '\n'.join([template.format(c, profile[c]) for c in content])
             
  return display

def load():
  return [movie]
