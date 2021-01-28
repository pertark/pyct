class Result:
  def __init__(self, value, pos):
    self.value = value
    self.pos = pos

  def __repr__(self):
    return f'Result({self.value}, {self.pos})'

class Parser:
  def __call__(self, tokens, pos):
    return None

  def __add__(self, other):
    return Add(self, other)

  def __or__(self, other):
    return Or(self, other)

  def __xor__(self, function):
    return Xor(self, function)

class Add(Parser):
  def __init__(self, left, right):
    self.left = left
    self.right = right
  def __call__(self, tokens, pos):
    left_fx = self.left(tokens, pos)
    if left_fx:
      right_fx = self.right(tokens, left_fx.pos)
      if right_fx:
        combined = (left_fx.value, right_fx.value)
        return Result(combined, right_fx.pos)
    return None

class Xor(Parser):
  def __init__(self, parser, function):
    self.parser = parser
    self.function = function
  def __call__(self, tokens, pos):
    result = self.parser(tokens, pos)
    if result:
      result.value = self.function(result.value)
      return result # ty

class Reserved(Parser):
  def __init__(self, v, t):
    self.val = v
    self.tag = t
  def __call__(self, t, p):
    if p < len(t) and t[p][1] is self.tag and t[p][0] == self.value:
      return Result(t[p][0], p+1)
    else:
      return None

class Tag(Parser):
  def __init__(self, tag):
    self.tag = tag
  def __call__(self, t, p):
    if p < len(t) and t[p][1] is self.tag:
      return Result(t[p][0], p + 1)
    else:
      return None

class Or(Parser):
  def __init__(self, left, right):
    self.left = left
    self.right = right

  def __call__(self, tokens, pos):
    lr = self.left(tokens, pos)
    if lr:
      return lr
    else:
      rr = self.right(tokens, pos)
      return rr


