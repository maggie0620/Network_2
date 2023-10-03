import re
import collections
file1 = open('D:/Network/Network 1.txt', 'r')
net1 = file1.read()
file2 = open('D:/Network/Network 2.txt', 'r')
net2 = file2.read()

## 2-1
# Network 1 in-degree sequence / out-degree sequence       
split1 = re.split('\n', net1)
split1.remove('')
edge1 = []
for i in range(0,len(split1)):
    num1 = re.sub('\t','',split1[i])
    edge1.append(num1)

ind1 = []
outd1 = []
for j in range(0,len(edge1)):
    ind1.append(edge1[j][1])
    outd1.append(edge1[j][0])

c = collections.Counter(ind1)    
in_values1, in_counts1 = zip(*c.most_common())
in_seq1 = in_counts1[::-1]
print("Net1 in-degree seq:", in_seq1)

c = collections.Counter(outd1)    
out_values1, out_counts1 = zip(*c.most_common())
out_seq1 = out_counts1[::-1]
print("Net1 out-degree seq:", out_seq1)

# Network 2 in-degree sequence / out-degree sequence
split2 = re.split('\n', net2)
split2.remove('')
edge2 = []
for i in range(0,len(split2)):
    num2 = re.sub('\t','',split2[i])
    edge2.append(num2)
        
ind2 = []
outd2 = []
for j in range(0,len(edge2)):
    ind2.append(edge2[j][1])
    outd2.append(edge2[j][0])
    
c = collections.Counter(ind2)    
in_values2, in_counts2 = zip(*c.most_common())
in_seq2 = in_counts2[::-1]
print("Net2 in-degree seq:", in_seq2)

c = collections.Counter(outd2)    
out_values2, out_counts2 = zip(*c.most_common())
out_seq2 = out_counts2[::-1]
print("Net2 out-degree seq:", out_seq2)

## 2-2
from collections import defaultdict

class Graph:
    def __init__(self, nodes):
        self.graph = defaultdict(list)
        self.nodes = nodes
        
    def add_edge(self, u, v):
        self.graph[u].append(v)
            
    def add_undict_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def DFS(self, v, visited):
        key = self.nodes.index(v)
        visited[key] = True
        for i in self.graph[v]:
            k = self.nodes.index(i)
            if not visited[k]:
                self.DFS(self.nodes[k], visited)

    def strongly_connected(self):               
        # Initialize all nodes as not visited
        visited = [False] * len(self.nodes)

        # Find a vertex with non-zero degree
        v = None
        for key in self.graph:
            if len(self.graph[key]) > 0:
                v = key
                break
        
        # A single vertex is considered strongly connected.   
        if v is None:
            return True
        
        # Check if the graph is strongly connected
        self.DFS(v, visited)

        # If any node is not reachable, the graph is not strongly connected
        if any(not visited[i] for i in range(0,len(visited))):
            return False

        # Reverse the graph
        reversed_graph = defaultdict(list)
        for u in self.graph:
            for v in self.graph[u]:
                reversed_graph[v].append(u)

        # Reset visited array
        visited = [False] * len(self.nodes)

        # Find a new starting node in the reversed graph
        v_reversed = None
        for key in reversed_graph:
            if len(reversed_graph[key]) > 0:
                v_reversed = key
                break
            
        # Check if the reversed graph is strongly connected
        self.DFS(v_reversed, visited)

        # If any node is not reachable, the graph is not strongly connected
        if any(not visited[i] for i in range(0,len(visited))):
            return False

        return True
    
    def weakly_connected(self):            
        visited = [False] * len(self.nodes)

        # Find a starting node to start DFS
        v = None
        for v in self.graph:
            if self.graph[v]:
                start_node = v
                break            
        
        # A single vertex is considered strongly connected. (Not weakly connected)  
        if v is None:
            return False
        
        # Check if the graph is weakly connected
        self.DFS(start_node, visited)
        
        # Check if all nodes are reachable
        if any(not visited[i] for i in range(0,len(visited))):
            return False

        return True

# Network 1 Connectivity
mylist1 = []
for k in ind1:
    if k not in mylist1:
        mylist1.append(k)
for k in outd1:
    if k not in mylist1:
        mylist1.append(k)
#print(mylist1)

path1 = Graph(mylist1)
path1_un = Graph(mylist1)
for e in range(0,len(edge1)):
    path1.add_edge(edge1[e][0],edge1[e][1])
    path1_un.add_undict_edge(edge1[e][0],edge1[e][1])
#print(path1.graph)
#print(path1_un.graph)

if path1.strongly_connected():
    print("Network 1 is strongly connected.")
elif path1_un.weakly_connected():
    print("Network 1 is weakly connected.")
else:
    print("Network 1 is neither strongly connected nor weakly connected.")

    
# Network 2 Connectivity
mylist2 = []
for k in ind2:
    if k not in mylist2:
        mylist2.append(k)
for k in outd2:
    if k not in mylist2:
        mylist2.append(k)
#print(mylist2)

path2 = Graph(mylist2)
path2_un = Graph(mylist2)
for e in range(0,len(edge2)):
    path2.add_edge(edge2[e][0],edge2[e][1])
    path2_un.add_undict_edge(edge2[e][0],edge2[e][1])
#print(path2.graph)
#print(path2_un.graph)

if path2.strongly_connected():
    print("Network 2 is strongly connected.")
elif path2_un.weakly_connected():
    print("Network 2 is weakly connected.")
else:
    print("Network 2 is neither strongly connected nor weakly connected.")

## 2-3              
class Distance:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def find_dis(self, start_node, end_node):
        visited = set()
        depth = {}

        def DFS(node, current_depth):
            visited.add(node)
            depth[node] = current_depth

            if node == end_node:
                return

            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    DFS(neighbor, current_depth + 1)

        DFS(start_node, 0)

        if end_node in depth:
            return depth[end_node]
        else:
            return -1  # Return -1 if there's no path between the nodes

# Distance between node a and node i (Net1) 
# Node a to Node i
path1 = Distance()
for e in range(0,len(edge1)):
    path1.add_edge(edge1[e][0],edge1[e][1])

if path1.find_dis("a", "i") != -1:
    print("Net1: The distance from a to i is", path1.find_dis("a", "i"))
else:
    print("Net1: The distance from a to i is NA")    

# Node i to Node a
if path1.find_dis("i", "a") != -1:
    print("Net1: The distance from i to a is", path1.find_dis("i", "a"))
else:
    print("Net1: The distance from i to a is NA")    

# Distance between node a and node i (Net2)
# Node a to Node i
path2 = Distance()
for e in range(0,len(edge2)):
    path2.add_edge(edge2[e][0],edge2[e][1])

if path2.find_dis("a", "i") != -1:
    print("Net2: The distance from a to i is", path2.find_dis("a", "i"))
else:
    print("Net2: The distance from a to i is NA")    

# Node i to Node a
if path2.find_dis("i", "a") != -1:
    print("Net2: The distance from i to a is", path2.find_dis("i", "a"))
else:
    print("Net2: The distance from i to a is NA")    

## 2-4
# List one weakly connected subgraph containing at least 5 nodes
class Subgraph:
    def __init__(self, nodes):
        self.graph = defaultdict(list)
        self.nodes = nodes
        
    def add_edge(self, u, v):
        self.graph[u].append(v)
        
    def DFS(self, v, visited):
        key = self.nodes.index(v)
        visited[key] = True
        for i in self.graph[v]:
            k = self.nodes.index(i)
            if not visited[k]:
                self.DFS(self.nodes[k], visited)
                
    def DFS_sub(self, v, visited, path, sub):
        key = self.nodes.index(v)
        visited[key] = True
        sub.append(v)  # Store nodes in the subgraph
        for i in self.graph[v]:
            k = self.nodes.index(i)
            if not visited[k]:                
                path.append(v+i)  # Store the direct edge in the path
                self.DFS_sub(self.nodes[k], visited, path, sub)
                
    def strongly_connected(self):               
        # Initialize all nodes as not visited
        visited = [False] * len(self.nodes)

        # Find a vertex with non-zero degree
        v = None
        for key in self.graph:
            if len(self.graph[key]) > 0:
                v = key
                break
            
        if v is None:
            return True
        
        # Check if the graph is strongly connected
        self.DFS(v, visited)

        # If any node is not reachable, the graph is not strongly connected
        if any(not visited[i] for i in range(0,len(visited))):
            return False

        # Reverse the graph
        reversed_graph = defaultdict(list)
        for u in self.graph:
            for v in self.graph[u]:
                reversed_graph[v].append(u)

        # Reset visited array
        visited = [False] * len(self.nodes)

        # Find a new starting node in the reversed graph
        v_reversed = None
        for key in reversed_graph:
            if len(reversed_graph[key]) > 0:
                v_reversed = key
                break
            
        # Check if the reversed graph is strongly connected
        self.DFS(v_reversed, visited)

        # If any node is not reachable, the graph is not strongly connected
        if any(not visited[i] for i in range(0,len(visited))):
            return False

        return True
    
    def subgraph(self):
        visited = [False] * len(self.nodes)
        subgraphs = []
        subnodes = []

        # Run DFS
        for node in self.nodes:
            if not visited[self.nodes.index(node)]:
                sub = []  # Initialize a subgraph
                path = []
                self.DFS_sub(node, visited, path, sub)
                #print(path)
                subgraphs.append(path)
                subnodes.append(sub)

        # Check if there's a subgraph with at least 5 nodes
        for subnode in subnodes:
            if len(subnode) >= 5:
                print("Subgraph node list:", subnode)
                s = subnodes.index(subnode)
                subgraph = subgraphs[s]
                print("Subgraph edge list:", subgraph)
                # Check the subgraph is not strongly connected
                subpath = Subgraph(subnode)
                for e in range(0,len(subgraph)):
                    subpath.add_edge(subgraph[e][0],subgraph[e][1])
                if not subpath.strongly_connected():
                    #print(subpath.graph)
                    return True

        return False

# For Network 1
path1 = Subgraph(mylist1)
for e in range(0,len(edge1)):
    path1.add_edge(edge1[e][0],edge1[e][1])
#print(path1.graph)

if path1.subgraph():
    print("Net1 exists a subgraph which is weakly connected.")
else:
    print("Net1 has no weakly connected subgraph with at least 5 nodes.")

# For Network 2
path2 = Subgraph(mylist2)
for e in range(0,len(edge2)):
    path2.add_edge(edge2[e][0],edge2[e][1])
#print(path2.graph)

if path2.subgraph():
    print("Net2 exists a subgraph which is weakly connected.")
else:
    print("Net2 has no weakly connected subgraph with at least 5 nodes.")
    