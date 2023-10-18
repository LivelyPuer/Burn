from pprint import pprint

file = open("QLearnRealdata.csv")
file.readline()
lines = file.readlines()
data = list(map(lambda x: tuple(map(float, x.rstrip().split(",")))[:2], lines))
file.close()
adj = {}

while 0 < len(data):
    adj[tuple(data[0])] = list(filter(
        lambda x: (x[0] - 5 == data[0][0] and x[1] == data[0][1]) != (x[1] - 2 == data[0][1] and x[0] == data[0][0]),
        data))
    del data[0]
pprint(adj)

visited = []  # List to keep track of visited nodes.
queue = []  # Initialize a queue


def bfs(visited, graph, node):
    global queue
    visited.append(node)
    queue.append(node)
    while queue:
        s = queue.pop(0)
        print(s, end=" ")
        for neighbour in graph[s]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)


# Driver Code
bfs(visited, adj, (180.0, 0.0))
