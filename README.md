dagger
======

*Directed Acyclic Graph and Tools*

Description
-----------

`dagger` is a tiny and very light directed acyclic graph module.


Dependencies
------------

None.

Installation
------------

On Linux and Macintosh:

```
$ git clone https://github.com/petervaro/dagger.git
$ cd dagger
$ sudo python3 setup.py install
```

Usage
-----

Create graph and topologically sort it:

```python
from dagger.graph import Graph
from dagger.tools import topo_sort

#     (root)   (B)
#       /|      |
#      / v     /
#     / (A) <-'
#    /   |\
#   /    | `-> (C)
#  /     |      |
#  \     v     /
#   `-> (D) <-'

# Create graph
g = Graph()

# Create graph's vertices
g.add_vertex('root')
g.add_vertex('A')
g.add_vertex('B')
g.add_vertex('C')
g.add_vertex('D')

# Connect vertices
g.add_edge('root', 'A')
g.add_edge('root', 'D')
g.add_edge('A', 'C')
g.add_edge('A', 'D')
g.add_edge('B', 'A')
g.add_edge('C', 'D')

# Print relations
g.print_graph()

# Print topological sort
print()
topo_sort(g, debug=True)
"""

And the output is:

```
root -> D, A
D -|
C -> D
A -> C, D
B -> A

B -> root -> A -> C -> D
```
