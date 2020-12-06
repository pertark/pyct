import click
import requests
from bs4 import BeautifulSoup
import sys
import json


@click.command('search', help="search with various engines")
@click.option("--engine", "-e", default='ddg', nargs=1,
              help="Selects an engine to search. ", type=str)
@click.argument("query", nargs=-1)
def search(engine, query):
  engine = engine.lower()
  if engine == 'ddg' or engine == 'duckduckgo':
    ddg(query)
  elif engine == 'stackoverflow' or engine == 'so':
    click.echo('wip')
  else:
    click.echo(f'No engine "{engine}". Defaulting to DuckDuckGo.')
    ddg(query)

# @click.argument("query", nargs=-1)


#@search.command('ddg', help="search duck duck go")
#@click.argument("query", nargs=-1)
def ddg(query):
  query = ' '.join(query)
  p = requests.get(f'https://api.duckduckgo.com/?q={query}&format=json')
  response = json.loads(p.text)
  
  result = ''
  answer = response["Answer"]
  if answer and type(answer) == str:
    result += answer
    
  abstract = response["Abstract"]
  if abstract:
    result += '\n'*(bool(answer)) + abstract
  
  if not result:
    if response["RelatedTopics"]:
      result = response["RelatedTopics"][0]['Text']
    else:
      result = 'No results :('
    

  click.echo(result)
  # print(result.encode())
  
  

#@search.command('stack_overflow', help="search stack overflow")
#@click.argument("query", nargs=-1)
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
