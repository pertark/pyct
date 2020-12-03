import click
import os.path, os
import json


@click.group("notes", help="Stores notes and dates")
def notes():
  pass


def getnotes():
  homedir = os.path.expanduser("~")
  try:
    with open(homedir + "/.pyct/notes.json", "r") as f:
      js = json.load(f)
    return js
  except IOError:
    os.mkdir(homedir + "/.pyct")
    with open(homedir + "/.pyct/notes.json", "w") as tmp:
      json.dump({}, tmp)
    return {}

def setnotes(js):
  homedir = os.path.expanduser("~")
  try:
    with open(homedir + "/.pyct/notes.json", "w") as f:
      json.dump(js, f)
  except IOError:
    os.mkdir(homedir + "/.pyct")
    with open(homedir + "/.pyct/notes.json", "w") as tmp:
      json.dump(js, tmp)


@click.command("add")
def add():
  click.echo(getnotes())


notes.add_command(add)


def load():
  return [notes]
