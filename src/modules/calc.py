import click
from .calco.lexer import lex
from math import *

@click.command("calc", help="Calculates calculations  ")
@click.argument("equation", nargs=-1)
def calc(equation):
  eq = " ".join(equation)
  click.echo(peepeega_calc(eq))

def peepeega_calc(equation):
  if (equation == ""):
    print("Invalid input.")
    exit(1)
  return eval(equation)

def load():
  return [calc]


if __name__ == "__main__":
  tokens = [
    (r'[ \n\t]+',              None),
    (r'[0-9]+',              "NUMBER"),
    (r'\(',                    "PAREN"),
    (r'\)',                    "PAREN"),
    (r'\+',                    "RESERVED"),
    (r'\^',                    "RESERVED"),
    (r'-',                     "RESERVED"),
    (r'\*',                    "RESERVED"),
    (r'/',                     "RESERVED"),
  ] # + [(fx, "FUNCTION") for fx in ['sin', 'cos', 'tan', 'csc', 'sec', 'cot', "log"]]\
          #  + [('arc' + fx, "FUNCTION") for fx in ['sin', 'cos', 'tan', 'csc', 'sec', 'cot', "log"]]  # arclog fully intentional
  i = input()
  print(lex(i, tokens))
