import re
from planetPython import Tree


def parse(source):
  f = open(source, 'r')

  res = []
  for line in f:
    if not line.strip() or line.strip()[0] == '#':
      continue
    m = re.search('(\s*)(.*)', line)
    res.append((len(m.group(1)), get_color(m.group(2))))

  return res


def get_color(line):
  if re.match('(if|else|elif).*:', line):
    return (1, 0, 0)
  elif re.match('while.*:', line):
    return (0, 1, 0)
  elif re.match('for.*:', line):
    return (0, 0, 1)
  elif re.match('class.*:', line):
    return (1, 1, 0)
  elif re.match('def.*:', line):
    return (1, 0, 1)
  else:
    return (1, 1, 1)


def createTreeFromParse(parse, color, father):
  tree = Tree(father, color)

  if len(parse) == 0:
    return tree

  height = parse[0][0]
  color = parse[0][1]

  i = 0
  j = 0

  for height2 in parse[1:]:
    j += 1
    if height2[0] == height:
      createTreeFromParse(parse[i + 1:j], color, tree)
      i = j
      color = height2[1]

  createTreeFromParse(parse[i + 1:], color, tree)
  return tree


if __name__ == '__main__':
  res = parse('toParse.py')
  print res
  tree = createTreeFromParse(res, (1, 1, 1), None)
  print tree
