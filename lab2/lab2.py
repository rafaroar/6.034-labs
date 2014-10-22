# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    # init
    visited = []
    path = [start]
    queue = [path]
    visited.append(start)

    # procedure
    while (len(queue) > 0):
        #print 'queue', queue
        path = queue.pop(0)
        #print 'path', path
        current = path[-1]
        #print 'current', current
        if current == goal:
            return path
        
        neighbors = graph.get_connected_nodes(current)
        #print 'neighbors', neighbors
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.append(neighbor)
                #print 'path', path
                newpath = path[:]
                newpath.append(neighbor)
                #print 'newpath', newpath
                queue.append(newpath)

    return []

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    # init
    visited = []
    path = [start]
    queue = [path]
    visited.append(start)

    # procedure
    while (len(queue) > 0):
        #print 'queue', queue
        path = queue.pop()
        #print 'path', path
        current = path[-1]
        #print 'current', current
        if current == goal:
            return path
        
        neighbors = graph.get_connected_nodes(current)
        #print 'neighbors', neighbors
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.append(neighbor)
                #print 'path', path
                newpath = path[:]
                newpath.append(neighbor)
                #print 'newpath', newpath
                queue.append(newpath)

    return []


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    # init
    #visited = []
    path = [start]
    queue = [path]
    #visited.append(start)

    # procedure
    while (len(queue) > 0):
        heur = []
        #print 'queue', queue
        path = queue.pop()
        #print 'path', path
        current = path[-1]
        #print 'current', current
        if current == goal:
            return path

        #visited.append(current)
        
        neighbors = graph.get_connected_nodes(current)
        #print 'neighbors', neighbors
        for neighbor in neighbors:
            #if neighbor not in visited:
            if neighbor not in path:
                #print 'path', path
                newpath = path[:]
                newpath.append(neighbor)
                h = graph.get_heuristic(neighbor, goal)# + graph.get_edge(current, neighbor).length
                #print 'newpath', newpath
                #queue.append(newpath)
                heur.append((h, newpath))

        sort_heur = sorted(heur)
        sort_heur.reverse()

        queue += [tup[1] for tup in sort_heur]

        #print 'queue'
        #for element in queue:
#            print element
        #queue.sort(key = lambda path: path[0]) works for second            
        #queue.sort(reverse=True)
        #queue.sort(key = lambda path: path[0], reverse=True)
#        print 'sorted queue'
#        for element in queue:
#            print element

    return []

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    # init
#    print "beam_width", beam_width
    #visited = []
    path = [900, start]
    max_path_len = 2
    queue = [path]
    #visited.append(start)

    # procedure
    while (len(queue) > 0):
        #heur = []
        #print 'queue', queue
        path = queue.pop(0)
        #print 'path', path
        current = path[-1]
        #print 'current', current
        if current == goal:
            path.pop(0)
            return path
        
        neighbors = graph.get_connected_nodes(current)
        #print 'neighbors', neighbors
        for neighbor in neighbors:
            if neighbor not in path:
                #visited.append(neighbor)
                #print 'path', path
                newpath = path[:]
                newpath.append(neighbor)
                h = graph.get_heuristic(neighbor, goal)
                newpath[0] = h
#                print 'len', len(newpath)
                if len(newpath) > max_path_len:
                    max_path_len = len(newpath)
                #print 'newpath', newpath
                #queue.append(newpath)
                #heur.append((h, newpath))
                queue.append(newpath)

#        sort_heur = sorted(heur)
#        sort_heur.reverse()

#        queue += [tup[1] for tup in sort_heur]
#        queue.sort(key = lambda path: path[0])
        sorted_queue = sorted(queue)
#        print 'sorted queue'
#        for element in sorted_queue:
#            print element

    #getting rid of paths
        for le in xrange(2, max_path_len + 1):
#            print 'first loop', 'le', le
            counter = 0
            for pa in sorted_queue:
#                print 'second loop', 'pa', pa
                if le == len(pa):
                    
                    counter = counter + 1
#                    print le, pa, counter
                    if counter > beam_width:
                        queue.remove(pa)
#                        print 'PATH WAS REMOVED WAAAAAAAAAAAAAAAAAAAAAAAAA'
#        print 'pruned queue'
#        for element in queue:
#            print element

    return []

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    path_len = 0
    if len(node_names) < 2:
        return path_len
    for i in xrange(len(node_names)-1):
        path_len += graph.get_edge(node_names[i], node_names[i+1]).length
    return path_len
        

def branch_and_bound(graph, start, goal):
    # init
    path = [900, start]
    queue = [path]

    # procedure
    while (len(queue) > 0):
        #heur = []
        path = queue.pop(0)
        current = path[-1]
        if current == goal:
            path.pop(0)
            return path
        
        neighbors = graph.get_connected_nodes(current)
        for neighbor in neighbors:
            if neighbor not in path:
                newpath = path[:]
                newpath.append(neighbor)
                h = path_length(graph, newpath[1:])
                newpath[0] = h
                queue.append(newpath)
                #heur.append((h, newpath))

        #sort_heur = sorted(heur)
        #sort_heur.reverse()

        #queue += [tup[1] for tup in sort_heur]
        queue = sorted(queue)
        #queue.reverse()
#        print "queue"
#        for element in queue:
#            print element

    return []

def a_star(graph, start, goal):
    # init
    path = [900, start]
    queue = [path]
    extended = []

    # procedure
    while (len(queue) > 0):
        #heur = []
        path = queue.pop(0)
        current = path[-1]
        if current == goal:
            path.pop(0)
            return path
        
        neighbors = graph.get_connected_nodes(current)
        for neighbor in neighbors:
            if neighbor not in path and neighbor not in extended:
                extended.append(neighbor)
                newpath = path[:]
                newpath.append(neighbor)
                h = path_length(graph, newpath[1:]) + graph.get_heuristic(neighbor, goal)
                newpath[0] = h
                queue.append(newpath)
                #heur.append((h, newpath))

        #sort_heur = sorted(heur)
        #sort_heur.reverse()

        #queue += [tup[1] for tup in sort_heur]
        queue = sorted(queue)
        #queue.reverse()
        #print "queue"
        #for element in queue:
            #print element

    return []


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    for i in xrange(len(graph.nodes) - 1):
        node = graph.nodes[i]
        path = bfs(graph, node, goal)
        if graph.get_heuristic(node, goal) > path_length(graph, path):
            return False

    return True

def is_consistent(graph, goal):
    for i in xrange(len(graph.nodes) - 1):
        node = graph.nodes[i]
        if node != goal:
            path = bfs(graph, node, goal)
            diff = abs(graph.get_heuristic(node, goal) - graph.get_heuristic(path[1], goal))
            if diff > path_length(graph, [node, path[1]]):
                return False

    return True

HOW_MANY_HOURS_THIS_PSET_TOOK = '7'
WHAT_I_FOUND_INTERESTING = 'implementing bfs from scratch'
WHAT_I_FOUND_BORING = 'debugging'
