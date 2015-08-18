## INFO ##
## INFO ##

from dagger.graph import Graph
from dagger.tools import topo_sort, a_star

g = Graph()

g.add_vertex('root')
g.add_vertex('A')
g.add_vertex('B')
g.add_vertex('C')
g.add_vertex('D')
g.add_vertex('E')
g.add_vertex('F')
g.add_vertex('G')
g.add_vertex('H')
g.add_vertex('I')
g.add_vertex('J')
g.add_vertex('K')
g.add_vertex('L')
g.add_vertex('M')
g.add_vertex('N')
g.add_vertex('O')

g.add_edge('root', 'A')
g.add_edge('root', 'B')
g.add_edge('A', 'C')
g.add_edge('A', 'D')
g.add_edge('B', 'E')
g.add_edge('B', 'F')
g.add_edge('C', 'G')
g.add_edge('C', 'H')
g.add_edge('D', 'I')
g.add_edge('D', 'J')
g.add_edge('E', 'K')
g.add_edge('F', 'L')
g.add_edge('F', 'M')
g.add_edge('H', 'N')
g.add_edge('L', 'O')

g.print_graph()
print(*[v._id for v in topo_sort(g)])

# N -> H -> C -> A -> root
print(*reversed([v._id for v in a_star(g, 'root', 'N')]), sep=' -> ')
# root -> B -> F -> L -> O
print(*[v._id for v in a_star(g, 'root', 'O')], sep=' -> ')
