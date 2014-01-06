import planetPython as st
import simpleParser as sp


def planetMap(planetRoot, treeRoot):
  planet = planetRoot
  node = treeRoot
  planetNodeMap = dict()

  while planet or node:
    if not planet:
      planetFather = planetNodeMap[node.father]
      newPlanet = planetFather.append(node.content)
      planetNodeMap[node] = newPlanet
#      print 'insert', node.content
      node = nextN(node)
      continue

    elif not node:
#      print 'remove', planet.color()
      nextPlanetNode = nextN(planet.node)
      nextPlanet = nextPlanetNode.content if nextPlanetNode else None
      planet.remove()
      planet = nextPlanet
      continue
    else:
      planetColor = planet.color()
      nodeColor = node.content

      nextPlanetNode = nextN(planet.node)
      nextPlanet = nextPlanetNode.content if nextPlanetNode else None
      if planetColor == nodeColor and (node.father == planet.node.father or
          planetNodeMap[node.father] == planet.node.father.content):
        planetNodeMap[node] = planet
#        print 'link', planet.color(), node.c
        planet = nextPlanet
        node = nextN(node)
      else:
#        print 'remove', planet.color()
        planet.remove()
        planet = nextPlanet


def nextN(node):
  if(len(node.children) == 0):
    index = node.index()
    node = node.father

    while(node and index == len(node.children) - 1):
      index = node.index()
      node = node.father
    return node.children[index + 1] if node else None
  else:
    return node.children[0]
