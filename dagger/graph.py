## INFO ##
## INFO ##

# Import python modules
import itertools


#------------------------------------------------------------------------------#
class Vertex:

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self, vertex_id):
        """Create a new Vertex object."""
        # Store property
        self._id = vertex_id
        # Create a container for neighbors
        self._vertices = set()


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __contains__(self, vertex) -> bool:
        """Return True if self is connected to the given vertex."""
        return vertex in self._vertices


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def add_vertex(self, vertex) -> 'vertex_id':
        """Connect self to the given vertex."""
        self._vertices.add(vertex)
        return vertex._id


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def rem_vertex(self, vertex):
        """Remove connection between self and the given vertex."""
        self._vertices.discard(vertex)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def vertices(self) -> set:
        """Return all vertices self connected to."""
        return self._vertices



#------------------------------------------------------------------------------#
class Edge:

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self, edge_id, source_vertex, target_vertex):
        """Create a new Edge object."""
        # Store properties
        self._id = edge_id
        self._source = source_vertex
        self._target = target_vertex
        # Connect vertices
        source_vertex.add_vertex(target_vertex)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def source(self) -> Vertex:
        """Return the source vertex of edge."""
        return self._source


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def target(self) -> Vertex:
        """Return the target vertex of edge."""
        return self._target


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def vertices(self) -> tuple:
        """Return both source and target vertices of edge."""
        return self._source, self._target



#------------------------------------------------------------------------------#
class Graph:

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self):
        """Create an empty Graph object."""
        self._vertices = {}
        self._edges = {}
        self._gen_edge_id = itertools.count()


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __contains__(self, vertex_id) -> bool:
        """Return True if vertex with the given id is in graph."""
        return vertex_id in self._vertices


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def add_vertex(self, vertex_id) -> Vertex:
        """
        Add vertex with vertex id to graph.
        If vertex does not exist creates it first
        and then add it to graph.
        """
        return self._vertices.setdefault(vertex_id, Vertex(vertex_id))


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def rem_vertex(self, vertex_id):
        """
        Remove vertex with the given id and
        all connected edges from the graph.
        """
        # Get each edges in graph
        for edge_id, edge in list(self.edges()):
            # If source or target vertex of
            # the edge is the given vertex
            if (edge.source()._id == vertex_id or
                edge.target()._id == vertex_id):
                    # Remove edge
                    self.rem_edge(edge_id)
        # Remove edge from graph
        self._vertices.pop(vertex_id, None)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def vertex(self, vertex_id) -> Vertex:
        """
        Return Vertex object with the given id from graph.
        If vertex is not in graph, return None.
        """
        return self._vertices.get(vertex_id, None)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def add_edge(self, source_id, target_id) -> 'edge_id':
        """
        Add new edge between the given vertices to graph.
        If vertices do not exist, then create and add new vertices to graph.
        If edge already in graph return its id, if not, creat and store new
        edge object and return the new id.
        """
        # If vertices are not in graph create them
        source = self._vertices.setdefault(source_id, Vertex(source_id))
        target = self._vertices.setdefault(target_id, Vertex(target_id))
        # If edge does exist in graph
        edges = [e for i, e in self.edges() if (e.source() == source and
                                                e.target() == target)]
        if edges:
            # Return id of existing edge
            return edges[0]._id
        # If edge does not exists
        else:
            # Generate id
            edge_id = next(self._gen_edge_id)
            # Create and store a new edge object
            self._edges[edge_id] = Edge(edge_id, source, target)
            # Return id of new edge
            return edge_id


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def rem_edge(self, edge_id):
        """Remove edge with the given id from graph."""
        # Remove edge from graph
        edge = self._edges.pop(edge_id, None)
        # If edge was in graph
        if edge:
            # Disconnect source and target vertices
            edge.source().rem_vertex(edge.target())


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def edge(self, edge_id):
        """
        Return Edge object with the given id from graph.
        If edge is not in graph, return None.
        """
        return self._edges.get(edge_id, None)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def vertices(self):
        """Return all vertex ids and vertex objects in graph."""
        yield from self._vertices.items()


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def edges(self):
        """Return all edge ids and edge objects in graph."""
        yield from self._edges.items()


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def print_graph(self, message=None):
        """Print out connections in graph."""
        if message:
            print(message)
        for vertex_id, vertex in self._vertices.items():
            vertices = [v._id for v in vertex.vertices()]
            if vertices:
                print(vertex_id, '->', ', '.join(map(str, vertices)))
            else:
                print(vertex_id, '-|')
