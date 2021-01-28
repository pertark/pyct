import re
import sys

def lex(string, tokens):
  position = 0
  tok = []
  while position < len(string):
    match = None
    for expr in tokens:
      pattern, tag = expr
      regex = re.compile(pattern)
      match = regex.match(string, position)
      if match:
        t = match.group(0)
        if t:
          tokn = (t, tag)
          tok.append(tokn)
        break
    if not match:
      sys.stderr.write("Error: Illegal character " + string[position] + " at position " + str(position))
      sys.exit(1)
    else:
      position = match.end(0)
  return tok