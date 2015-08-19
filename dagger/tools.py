## INFO ##
## INFO ##

# Import python modules
import itertools

#------------------------------------------------------------------------------#
class DAGCycleError(Exception): pass



#------------------------------------------------------------------------------#
def topo_sort(graph, debug=False, tracking=False):
    """Topological sort of directed acyclic graph"""
    # Necessary 'marks'
    FLAGS = 'done', 'idle'
    # Create a list for the processed output
    sorted = []

    # If tracking
    if tracking:
        # Create a list for tracking
        tracked = []
        # Create recursive helper function
        def visit(vertex):
            tracked.append(vertex)

            # If vertex was visited before
            if vertex.idle:
                raise DAGCycleError(tuple(v.id for v in tracked))

            # If vertex is not yet sorted
            if not vertex.done:
                vertex.idle = True
                for neighbor in vertex.vertices():
                    visit(neighbor)
                vertex.done = True
                vertex.idle = False
                sorted.append(vertex)
                tracked.pop()
    # If not tracking
    else:
        # Create recursive helper function
        def visit(vertex):
            # If vertex was visited before
            if vertex.idle:
                raise DAGCycleError(vertex.id)

            # If vertex is not yet sorted
            if not vertex.done:
                vertex.idle = True
                for neighbor in vertex.vertices():
                    visit(neighbor)
                vertex.done = True
                vertex.idle = False
                sorted.append(vertex)

    # Attach flags
    for _, vertex in graph.vertices():
        for flag in FLAGS:
            setattr(vertex, flag, False)

    # Create a list of all vertices that not sorted
    queue = [vertex for _, vertex in graph.vertices() if not vertex.done]

    # Test and sort vertices in queue
    while queue:
        visit(queue.pop(0))

    # If debug mode is 'ON'
    if debug:
        print(*[v._id for v in reversed(sorted)], sep=' -> ')

    # Detach properties
    for _, vertex in graph.vertices():
        for flag in FLAGS:
            delattr(vertex, flag)

    # Return iterator
    return reversed(sorted)



#------------------------------------------------------------------------------#
def a_star(graph, start_id, goal_id):
    """A* shortest path algorithm  in directed acyclic graph"""
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
