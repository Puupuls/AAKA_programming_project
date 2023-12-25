import heapq
import re


class Graph:
    def __init__(self, file, out_file):
        self.file = file
        self.out_file = out_file
        file_data = self.read_file()
        self.N = file_data[0]
        self.graph = self.create_graph(file_data[1:])
        self.pot_edges = set()
        self.pot_negative_edges()
        self.remove_potted_edges()
        self.remove_branches()
        self.find_MST()
        self.add_edges_not_in_MST()
        print(self.potted_difficulty())

    def pot_negative_edges(self):
        for node in self.graph:
            for node1 in self.graph[node]:
                if node < node1 and self.graph[node][node1] <= 0:
                    self.pot_edges.add((node, node1, self.graph[node][node1]))

    def potted_difficulty(self):
        difficulty = 0
        for edge in self.pot_edges:
            difficulty += edge[2]

        return difficulty

    def remove_potted_edges(self):
        for edge in self.pot_edges:
            if edge[0] in self.graph and edge[1] in self.graph[edge[0]]:
                del self.graph[edge[0]][edge[1]]
            if edge[1] in self.graph and edge[0] in self.graph[edge[1]]:
                del self.graph[edge[1]][edge[0]]

    def remove_branches(self):
        # Remove all branches that do not loop
        for node in list(self.graph.keys()):
            if node in self.graph and len(self.graph[node]) == 1:
                self.remove_branch(node)

    def remove_branch(self, node):
        # Remove the branch that starts at node
        while len(self.graph[node]) == 1:
            next_node = list(self.graph[node].keys())[0]
            del self.graph[node]
            del self.graph[next_node][node]
            node = next_node

    def find_MST(self):
        start_node = 0

        # Initialize a priority queue
        pq = [(0, start_node, start_node)]
        in_mst = set()
        mst_edges = []

        while pq:
            weight, node, source = heapq.heappop(pq)
            if node in in_mst:
                continue

            in_mst.add(node)

            if weight != 0:  # To exclude the starting node's weight
                mst_edges.append((node, source))

            for adjacent, w in self.graph[node].items():
                if adjacent not in in_mst:
                    heapq.heappush(pq, (-w, adjacent, node))

        self.mst_edges = mst_edges

    def add_edges_not_in_MST(self):
        edges = set()
        for e in self.mst_edges:
            s, f = e
            if s < f:
                edges.add((s, f))
            else:
                edges.add((f, s))
        for node in self.graph:
            for node1 in self.graph[node]:
                if node < node1:
                    if (node, node1) not in edges:
                        self.pot_edges.add((node, node1, self.graph[node][node1]))

    def create_graph(self, input_data):
        graph = {}
        for i in range(0, len(input_data), 3):
            node1, node2, difficulty = int(input_data[i]), int(input_data[i + 1]), int(input_data[i + 2])
            node1, node2 = (node1-1, node2-1)
            if node1 not in graph:
                graph[node1] = {}
            if node2 not in graph:
                graph[node2] = {}

            # Add the edge in both directions, as it's an undirected graph
            graph[node1][node2] = difficulty
            graph[node2][node1] = difficulty
        return graph

    def read_file(self):
        with open(self.file, 'r') as f:
            input_data = f.read()
            input_data = re.sub(r'[\n\r]+', ' ', input_data)
            input_data = re.sub(r'\t+', ' ', input_data)
            input_data = re.sub(r' +', ' ', input_data)
        input_data = input_data.split(' ')
        input_data = [int(i) for i in input_data]
        return input_data

    def write_file(self, result):
        with open(self.out_file, 'w') as f:
            f.write(str(result))


Graph('ex3.in', 'ex3.rez')
