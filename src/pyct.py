#!/usr/bin/env python3

import click
import json
import importlib
import colorama


@click.group("pyct")
def cli():
  pass


class Pyct:
  def __init__(self, modules):
    self.modules = modules
    self.load()
    cli()

  def load(self):
    for name in self.modules["modules"]:
      module = importlib.import_module("modules." + name)
      for i in module.load():
        cli.add_command(i)


def main():
  fil = json.load(open('/'.join(__file__.split("/")[:-1]) + "/modules.json"))
  Pyct(fil)

if __name__ == "__main__":
    main()
