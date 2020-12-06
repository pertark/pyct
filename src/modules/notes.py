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
@click.option("--priority", "-p", required=False, default="1", type=click.Choice(str(i) for i in [1, 2, 3]),
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
  if clear.lower() == "y":
    homedir = os.path.expanduser("~")
    with open(homedir + "/.pyct/notes.json", "w") as f:
      json.dump({"notes":[]}, f)
    click.echo(c.GREEN + c.BOLD + "Cleared! " + c.END)

@click.command("ls", help="Lists notes")
@click.option("--priority", "-p", required=False, type=click.Choice(str(i) for i in [1, 2, 3]), help="Lists specific priority")
@click.option("--created", "-c", required=False, type=str, help="y/m/d format to find notes created on a specific date")
@click.option("--number", "-n", required=False, type=int, help="List out a specific number of notes")
@click.option("--all", "-a", required=False, is_flag=True, help="Lists all notes")
def ls(priority, created, number, all):
  notes = getnotes()["notes"]
  if number:
    num = number
  else:
    num = 10
  if created:
    datere = "(^(1|2)\d\d\d\/(0[1-9]|[1-9]|1[012])\/(0[1-9]|[1-9]|[12][0-9]|3[01])$)|(^(1|2)\d\d\d\/(0[1-9]|[1-9]|1[012])\/(0[1-9]|[1-9]|[12][0-9]|3[01]):(0[1-9]|[1-9]|1[0-9]|2[0-4]):([1-9]|0[1-9]|[1-5][0-9]):([1-9]|0[1-9]|[1-5][0-9])$)"
    set = re.compile(datere)
    if not set.fullmatch(created):
      click.echo(c.RED + c.BOLD + "Date in wrong format. " + c.END)
      return
    if ":" in created:
      click.echo(c.RED + c.BOLD + "Date in wrong format. " + c.END)
      return
    else:
      matched = []
      for i in notes:
        if i[0] == created:
          matched.append(i)
      matched = sorted(matched, key=lambda x: (x[3], x[2], x[1]))[::-1]
      if priority == "1":
        col = c.GREEN
      elif priority == "2":
        col = c.YELLOW
      elif priority == "3":
        col = c.RED
      if priority:
        matched = [x for x in matched if x[3] == priority]
        if all:
          num = len(matched)
        if num > len(matched):
          num = len(matched)
        for i in range(num):
          click.echo(c.BOLD + c.CYAN + str(i+1) + ". " + c.END, nl=False)
          click.echo(c.BOLD + c.CYAN + matched[i][0] + c.END + " " + c.BOLD + col + matched[i][2])
        return
      else:
        if all:
          num = len(matched)
        if num > len(matched):
          num = len(matched)
        for i in range(num):
          click.echo(c.BOLD + c.CYAN + str(i+1) + ". " + c.END, nl=False)
          if matched[i][3] == "1":
            click.echo(c.BOLD + c.CYAN + matched[i][0] + c.END + " " + c.BOLD + c.GREEN + matched[i][2])
          elif matched[i][3] == "2":
            click.echo(c.BOLD + c.CYAN + matched[i][0] + c.END + " " + c.BOLD + c.YELLOW + matched[i][2])
          else:
            click.echo(c.BOLD + c.CYAN + matched[i][0] + c.END + " " + c.BOLD + c.RED + matched[i][2])
        return
  elif priority:
    if priority == "3":
      col = c.RED
    elif priority == "2":
      col = c.YELLOW
    else:
      col = c.GREEN
    n = [x for x in sorted(notes, key=lambda x:(x[0], x[3], x[2], x[1]))[::-1] if x[3] == priority]
    if all:
      num = len(n)
    if num > len(n):
      num = len(n)
    for i in range(num):
      if n[i][3] == priority:
        click.echo(c.BOLD + c.CYAN + str(i+1) + ". " + c.END, nl=False)
        click.echo(c.BOLD + c.CYAN + n[i][0] + c.END + " " + c.BOLD + col + n[i][2])
    return
  elif all:
    n = sorted(notes, key=lambda x:(x[0], x[3], x[2], x[1]))[::-1]
    for i in range(len(n)):
      click.echo(c.BOLD + c.CYAN + str(i+1) + ". " + c.END, nl=False)
      if n[i][3] == "1":
        click.echo(c.BOLD + c.CYAN + n[i][0] + c.END + " " + c.BOLD + c.GREEN + n[i][2])
      elif n[i][3] == "2":
        click.echo(c.BOLD + c.CYAN + n[i][0] + c.END + " " + c.BOLD + c.YELLOW + n[i][2])
      else:
        click.echo(c.BOLD + c.CYAN + n[i][0] + c.END + " " + c.BOLD + c.RED + n[i][2])
    return
  else:
    n = sorted(notes, key=lambda x:(x[0], x[3], x[2], x[1]))[::-1]
    if num > len(n):
      num = len(n)
    for i in range(num):
      click.echo(c.BOLD + c.CYAN + str(i+1) + ". " + c.END, nl=False)
      if n[i][3] == "1":
        click.echo(c.BOLD + c.CYAN + n[i][0] + c.END + " " + c.BOLD + c.GREEN + n[i][2])
      elif n[i][3] == "2":
        click.echo(c.BOLD + c.CYAN + n[i][0] + c.END + " " + c.BOLD + c.YELLOW + n[i][2])
      else:
        click.echo(c.BOLD + c.CYAN + n[i][0] + c.END + " " + c.BOLD + c.RED + n[i][2])
    return

@click.command("rm", help="Removes notes based on pyct notes ls -a list. ")
@click.option("--force", "-f", required=False, is_flag=True, help="Forcefully removes notes. ")
@click.argument("number", type=int)
def rm(number, force):
  notes = getnotes()
  if not (len(notes["notes"]) >= number and number > 0):
    click.echo(c.BOLD + c.RED + "Incorrect note to remove. ")
    return
  if not force:
    q = input(c.BOLD + c.RED + "Do you really want to remove this? [y/n] " + c.END)
    if q.lower() != "y":
      return
  del notes["notes"][len(notes["notes"])-number]

  setnotes(notes)

@click.command("edit", help="Edits a specific note [Number is based on the pyct notes ls -a list] ")
@click.argument("number", type=int)
@click.argument("note", type=str)
def edit(number, note):
  notes = getnotes()
  if not (len(notes["notes"]) >= number and number > 0):
    click.echo(c.BOLD + c.RED + "Incorrect note to edit. ")
    return
  notes["notes"][len(notes["notes"])-number][2] = note
  setnotes(notes)

notes.add_command(add)
notes.add_command(ls)
notes.add_command(clear)
notes.add_command(rm)
notes.add_command(edit)


def load():
  return [notes]
