import click
import requests
from bs4 import BeautifulSoup
import sys


@click.group("search", help="search various search engines",
             invoke_without_command=True)
@click.pass_context
def search(ctx):
  if ctx.invoked_subcommand is None:
    click.echo(stack_overflow('joe'))

# @click.argument("query", nargs=-1)


@search.command('stack_overflow', help="search stack overflow")
@click.argument("query", nargs=-1)
def stack_overflow(query):
  query = '+'.join(query)
  p = requests.get(f'https://stackoverflow.com/search?q={query}&sort=relevance')
  soup = BeautifulSoup(p.text, 'html.parser')
  a_tag = soup.find('a', {'class':'answer-title'})
  question = a_tag.get_text()
  question_url = a_tag['href']
  print(question)
  print(question_url)

def load():
  return [search]
