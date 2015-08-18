## INFO ##
## INFO ##

# Import python modules
import itertools

#------------------------------------------------------------------------------#
class DAGCycleError(Exception):

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self, *message_args):
        # Format message arguments and pass it to parent class
        Exception.__init__(self, ' '.join(str(item) for item in message_args))



#------------------------------------------------------------------------------#
def topo_sort(graph, debug=False):
    """ Topological sort of direct acyclic graph """
    # Necessary 'marks'
    FLAGS = 'done', 'idle'
    # Declare a list for tracking
    path = []

    # Create a recursively callable helper function
    def visit(vertex):
        # If vertex was visited before
        if vertex.idle:
            # Print out the path we have
            print(*[v._id for v in path], sep='->')
            # Raise
            raise DAGCycleError('Graph has at least one cycle at', vertex._id)

        # If vertex is not sorted yet
        if not vertex.done:
            vertex.idle = True
            for neighbor in vertex.vertices():
                visit(neighbor)
            vertex.done = True
            vertex.idle = False
            path.append(vertex)

    # Attach flags
    for _, vertex in graph.vertices():
        for flag in FLAGS:
            setattr(vertex, flag, False)

    # Create a list of all vertices that not sorted
    queue = [vertex for vid, vertex in graph.vertices() if not vertex.done]

    # Test and sort vertices in queue
    while queue:
        visit(queue.pop(0))

    # If debug mode is 'ON'
    if debug:
        print(*[v._id for v in reversed(path)], sep=' -> ')

    # Detach properties
    for _, vertex in graph.vertices():
        for flag in FLAGS:
            delattr(vertex, flag)

    # Return iterator
    return reversed(path)



#------------------------------------------------------------------------------#
def a_star(graph, start_id, goal_id):
    """ A* shortest path algorithm  in direct acyclic graph """
    # Get vertices
    start = graph.vertex(start_id)
    goal  = graph.vertex(goal_id)
    # Initialize
    closed_set = set()
    open_set   = {start}
    path       = {}

    start.g_score = 0
    start.f_score = start.g_score + 1

    def reconstruct_path(path, current_vertex):
        if current_vertex in path:
            p = reconstruct_path(path, path[current_vertex])
            return p + [current_vertex]
        else:
            return [current_vertex]

    while open_set:
        current = min(open_set, key=lambda vertex: vertex.f_score)
        if current is goal:
            return reconstruct_path(path, current)
        open_set.remove(current)
        closed_set.add(current)
        if current._vertices:
            for vertex in current.vertices():
                tentative_g_score = current.g_score + 1
                if vertex not in closed_set or tentative_g_score < vertex.g_score:
                    path[vertex] = current
                    vertex.g_score = tentative_g_score
                    vertex.f_score = vertex.g_score + 1
                    open_set.add(vertex)
    return []
