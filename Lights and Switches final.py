"""
CS 445: Algorithms
Lights and Switches Implementation
Philip Park
April 9, 2019
"""
global graph

# Reference: http://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
# Return true if line segments AB and CD intersect
# Borrowed off Daniel's Tardos 7.6.py
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
def visible(pt1,pt2,Walls):
    x1,y1 = pt1
    x2,y2 = pt2
    for i,wall in enumerate(Walls[:-1]):
        x3,y3 = wall
        x4,y4 = Walls[i+1]
        if intersect((x1,y1),(x2,y2),(x3,y3),(x4,y4)):
            return False
    return True

def edges_graph(L,M):
    graph['sink'] = []
    for i in range(0, len(L)):
        graph[M[i]] = []
    for switch in range(0, len(M)): 
        for light in range(0, len(M)):
            if visible(M[switch],L[light],Walls) == True:
                graph[M[switch]].append(L[light])
                
    graph['source'] = []
    for switch in range(0, len(M)):   # source node to switch
        graph['source'].append(M[switch])
    for light in range(0, len(L)):   # lights to sink node
        graph[L[light]] = ['sink']
    return graph

def maximum_flow(graphs):
        graph = edges_graph(Lights, Switches)
        path, z = bfs(graph,'source','sink')

        while z == True:
            #Remove nodes as they are not available for connection
            #https://www.geeksforgeeks.org/python-remove-discard-sets/
            for i in graph['source']:
                if i in path:
                    graph['source'].remove(i)  
            for newnode in graph[path[1]]:
                if newnode in path:
                    graph[path[1]].remove(newnode)  
            for othernode in graph[path[2]]:
                    if othernode in path:
                        graph[path[2]].remove(othernode)
                        residual = graph
            return residual

#Referenced: https://www.geeksforgeeks.org/find-if-there-is-a-path-between-two-vertices-in-a-given-graph/
def bfs(graphs, s, t): 
    visited = []
    queue = [[s]]
    
    # path checking loop
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node not in visited:
            new_node = graph[node]
            for other_existing in new_node:
                new_edge = list(path)
                new_edge.append(other_existing)
                queue.append(new_edge)
                if other_existing == t:
                    print ("")
                    return new_edge, True
            visited.append(node)

    # if there is no path between nodes
    print ("")
    return False

Walls = [(1,2),(1,5),(8,5),(8,3),(11,3),(11,1),(5,1),(5,3),(4,3),(4,1),(1,1),(1,2)]
Lights = [(2,4),(2,2),(5,4)]
Switches = [(6,2),(7,4),(6,3)]
graph = {}
residual = {}
print ("Walls:", Walls)
print ("Lights:", Lights)
print("Switches:", Switches)
    
print(maximum_flow(graph))
print(bfs(graph,'source', 'sink'))
