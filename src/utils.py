import json, functools, operator
from pygments import highlight, lexers, formatters

def flatten(nested_arr):
  return functools.reduce(operator.add, nested_arr)

def color_print(dct):
  formatted_json = json.dumps(dct, sort_keys=True, indent=4)
  return highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
