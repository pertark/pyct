import click
import os.path, os
import json


@click.group("notes", help="Stores notes and dates")
def notes():
  pass


def notesconfig():
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


@click.command("add")
def add():
  click.echo(notesconfig())


notes.add_command(add)


def load():
  return [notes]
