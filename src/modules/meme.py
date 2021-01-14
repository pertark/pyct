import click
import requests
import json
from colors import Colors as c
import os

@click.group("meme", help="Creates memes")
def meme():
  pass

def get_templates():
  homedir = os.path.expanduser("~")
  try:
    with open(homedir+'/.pyct/meme_templates.json') as f:
      templates = json.loads(f.read())
  except:
    try:
      os.mkdir(homedir + "/.pyct")
    except:
      templates = json.loads(requests.get('https://api.memegen.link/templates/').text)
      with open(homedir+'/.pyct/meme_templates.json','w') as f:
        json.dump(templates, f)

  return templates

def sanitize(text):
  # sanitize
  text = text.replace('-','--').replace('_','__').replace(' ', '_')
  text = text.replace('\n','~n').replace('"',"''")
  # reserved url characters
  sanitized = text.replace('?','~q').replace('&','~a').replace('%','~p')
  sanitized = sanitized.replace('#','~h').replace('/','~s').replace('\\','~b')
  return sanitized

@click.command("generate", help="Generate a meme using the memegen.link api")
@click.option("--template", "-t", required=True,
              help="Meme template key")
@click.option("--filetype", "-f", required=False, default='',
              help="Filetype of meme", type=click.Choice(['','png','jpg']))
@click.option("--output", "-o", required=False, default='meme',
              help="Output file")
@click.option("--width", "-w", required=False, default=0,
              help="width of meme", type=int)
@click.option("--height", "-h", required=False, default=0,
              help="height of meme", type=int)
def generate(template, filetype, output, width, height):
  templates = get_templates()
  keys = [tp['key'] for tp in templates]
  if template not in keys:
    click.echo('No meme template with key \''+template+'\'')
    return
  lines = templates[keys.index(template)]['lines']
  click.echo(str(lines)+" lines total: ")
  content = [sanitize(input('Line '+str(n+1)+': ')) for n in range(lines)]
  content = '/'.join(content)
  if '.' not in output:
    if filetype == '':
      filetype = 'png'
    output = output + '.' + filetype
  else:
    if output[output.rindex('.')+1:] not in ['png','jpg']:
      if filetype == '':
        filetype = 'png'
      output = output + '.' + filetype
    else:
      filetype = output[output.rindex('.')+1:]

  url = 'https://api.memegen.link/images/'+template+'/'+content+'.'+filetype
  
  dimensions = {}
  if width > 0:
    dimensions['width'] = width
  if height > 0:
    dimensions['height'] = height
  
  p = requests.get(url, params=dimensions)
  if not os.path.exists(output):
    if output.count('/') != 0:
      os.makedirs(output[:output.rindex('/')])
  with open(output,'wb') as f:
    f.write(p.content)

@click.command("list", help="list all meme templates and styles supported")
@click.argument("template", nargs=-1)
def list_(template):
  templates = get_templates()
      
  if len(template) == 0:
    click.echo('\n'.join([tp["key"]+": "+tp["name"] for tp in templates]))
    return

  template = ' '.join(template)
  keys = [tp['key'] for tp in templates]
  names = [tp['name'] for tp in templates]
  if template in keys:
    styles = templates[keys.index(template)]["styles"]
    if len(styles) > 0:
      click.echo(', '.join(styles))
    else:
      click.echo(templates[keys.index(template)]['name'] + ' has no styles.')
    return
  if template in names:
    styles = templates[names.index(template)]["styles"]
    if len(styles) > 0:
      click.echo(', '.join(styles))
    else:
      click.echo(templates[names.index(template)]['name'] + ' has no styles.')
    return

  click.echo('No meme template found with name or key \''+template+' :\'(')
    
    

  
  

meme.add_command(generate)
meme.add_command(list_)

def load():
  return [meme]
