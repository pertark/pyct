#
# class Aexp():
#   pass
#
# class IntAexp(Aexp):
#   def __init__(self, i):
#     self.i = i
#
#   def __repr__(self):
#     return 'IntAexp(%d)' % self.i
#
# class VarAexp(Aexp):
#   def __init__(self, name):
#     self.name = name
#
#   def __repr__(self):
#     return 'VarAexp(%s)' % self.name
#
# def aexp_value():
#   return (num ^ (lambda i: IntAexp(i))) | \
#          (id  ^ (lambda v: VarAexp(v)))


