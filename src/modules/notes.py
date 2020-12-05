import click
import os.path, os
import json
import datetime
from colors import Colors as c
import re


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
      json.dump({"notes": []}, tmp)
    return {"notes": []}


def setnotes(js):
  homedir = os.path.expanduser("~")
  try:
    with open(homedir + "/.pyct/notes.json", "w") as f:
      json.dump(js, f)
  except IOError:
    os.mkdir(homedir + "/.pyct")
    with open(homedir + "/.pyct/notes.json", "w") as tmp:
      json.dump(js, tmp)


@click.command("add", help="Adds a note")
@click.argument("note")
@click.option("--priority", "-p", required=False, default="3", type=click.Choice(str(i) for i in [1, 2, 3]),
              help="Dictates priority on notes")
def add(note, priority):
  gnot = getnotes()
  today = datetime.datetime.today()
  spec = f"{today.year}/{today.month}/{today.day}"
  spect = f"{today.hour}:{today.minute}:{today.second}"
  gnot["notes"].append([spec, spect, note, priority])
  setnotes(gnot)
  click.echo(c.LIGHT_GREEN + c.BOLD + spec + " " + spect + c.END + c.LIGHT_CYAN + " :  Note added! " + c.END)

@click.command("clear", help="Clears all notes")
def clear():
  clear = input(c.RED + c.BOLD + "Are you sure you want to clear? [y/n] " + c.END)
  if clear == "y":
    homedir = os.path.expanduser("~")
    with open(homedir + "/.pyct/notes.json", "w") as f:
      json.dump({"notes":[]}, f)
    click.echo(c.GREEN + c.BOLD + "Cleared! " + c.END)

@click.command("ls", help="Lists notes")
@click.option("--priority", "-p", required=False, type=click.Choice(str(i) for i in [1, 2, 3]), help="Lists specific priority")
@click.option("--created", "-c", required=False, type=str, help="y/m/d:h:m:s - use * for any value, only doing y/m/d also works")
@click.option("--number", "-n", required=False, type=int, help="List out a specific number of notes")
@click.option("--all", "-a", required=False, help="Lists all notes")
def ls(priority, created, number, all):
  notes = getnotes()["notes"]
  if number:
    num = number
  elif all:
    num = len(notes)
  else:
    num = 10
  if created:
    datere = "(^(1|2)\d\d\d\/(0[1-9]|[1-9]|1[012])\/(0[1-9]|[1-9]|[12][0-9]|3[01])$)|(^(1|2)\d\d\d\/(0[1-9]|[1-9]|1[012])\/(0[1-9]|[1-9]|[12][0-9]|3[01]):(0[1-9]|[1-9]|1[0-9]|2[0-4]):([1-9]|0[1-9]|[1-5][0-9]):([1-9]|0[1-9]|[1-5][0-9])$)"
    set = re.compile(datere)
    if not set.fullmatch(created):
      click.echo(c.RED + c.BOLD + "Date in wrong format. " + c.END)
      return
    if ":" in created:
      date = [created.split(":")[0], ':'.join(created.split(":")[1:])]
      matched = []
      for i in notes:
        if i[0] == date[0] and i[1] == date[1]:
          pass
    else:
      pass




notes.add_command(add)
notes.add_command(ls)
notes.add_command(clear)


def load():
  return [notes]
