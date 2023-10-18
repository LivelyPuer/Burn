import sys


class Graph(object):
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)

    def construct_graph(self, nodes, init_graph):
        '''
        Этот метод обеспечивает симметричность графика. Другими словами, если существует путь от узла A к B со значением V, должен быть путь от узла B к узлу A со значением V.
        '''
        graph = {}
        for node in nodes:
            graph[node] = {}

        graph.update(init_graph)

        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value

        return graph

    def get_nodes(self):
        "Возвращает узлы графа"
        return self.nodes

    def get_outgoing_edges(self, node):
        "Возвращает соседей узла"
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections

    def value(self, node1, node2):
        "Возвращает значение ребра между двумя узлами."
        return self.graph[node1][node2]


def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.get_nodes())

    # Мы будем использовать этот словарь, чтобы сэкономить на посещении каждого узла и обновлять его по мере продвижения по графику
    shortest_path = {}

    # Мы будем использовать этот dict, чтобы сохранить кратчайший известный путь к найденному узлу
    previous_nodes = {}

    # Мы будем использовать max_value для инициализации значения "бесконечности" непосещенных узлов
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    # Однако мы инициализируем значение начального узла 0
    shortest_path[start_node] = 0

    # Алгоритм выполняется до тех пор, пока мы не посетим все узлы
    while unvisited_nodes:
        # Приведенный ниже блок кода находит узел с наименьшей оценкой
        current_min_node = None
        for node in unvisited_nodes:  # Iterate over the nodes
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        # Приведенный ниже блок кода извлекает соседей текущего узла и обновляет их расстояния
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node

        # После посещения его соседей мы отмечаем узел как "посещенный"
        unvisited_nodes.remove(current_min_node)

    return previous_nodes, shortest_path


def print_result(previous_nodes, shortest_path, start_value, start_node, target_node):
    path = []
    node = target_node

    while node != start_node:
        path.append(node)
        node = previous_nodes[node]

    # Добавить начальный узел вручную
    path.append(start_node)

    print("Найден следующий лучший маршрут с ценностью {}.".format(start_value + shortest_path[target_node]))
    print(list(reversed(path)))


file = open("QLearnRealdata.csv")
file.readline()
lines = file.readlines()
nodes = list(map(lambda x: tuple(map(float, x.rstrip().split(",")))[:2], lines))
data = list(map(lambda x: tuple(map(float, x.rstrip().split(","))), lines))
data_b = data.copy()
min_nox = min(data, key=lambda x: x[2])
print(min_nox)

file.close()

adj = dict()

while 0 < len(data):
    adj[tuple(data[0])] = list(filter(
        lambda x: (x[0] - 5 == data[0][0] and x[1] == data[0][1]) != (x[1] - 2 == data[0][1] and x[0] == data[0][0]),
        data))
    del data[0]


def get_nox(node):
    return list(filter(lambda x: x[0] == node[0] and x[1] == node[1], data_b))[0][2]


init_graph = {}
for node in nodes:
    init_graph[node] = {}
for k, v in adj.items():
    for value in v:
        init_graph[k[:2]][value[:2]] = value[2]

print(init_graph)
start_node = (215.0, 30.0)
graph = Graph(nodes, init_graph)
previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=start_node)
print_result(previous_nodes, shortest_path, start_value=get_nox(start_node), start_node=start_node,
             target_node=min_nox[:2])
