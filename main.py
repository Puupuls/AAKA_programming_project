import heapq
import re


class Graph:
    def __init__(self, file, out_file):
        self.file = file
        self.out_file = out_file
        self.pot_edges = set()
        file_data = self.read_file()
        self.N = file_data[0]
        self.graph = self.create_graph(file_data[1:])
        self.pot_negative_edges()
        self.remove_potted_edges()
        self.remove_branches()
        self.find_MST()
        self.add_edges_not_in_MST()
        self.write_file()

    def read_file(self):
        # Atver un nolasa ievaddatus, pārvēršot tos skaitļos
        # Laika sarežģītība O(E)
        with open(self.file, 'r') as f:
            input_data = f.read()
        input_data = input_data.split()
        input_data = [int(i) for i in input_data]
        return input_data

    def create_graph(self, input_data):
        # Izveido grafu no ievaddatiem
        # Grafu glabā kā vādnīcu kur katram mezglam piekārtota vārdnīca
        # ar no tā izejošajiem ceļiem un šo ceļu sarežģītība
        # Laika sarežģītība O(E)
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

    def pot_negative_edges(self):
        # Atrod visas šķautnes ar ne-pozitīvu sarežģītību
        # un atzīmē tās kā medus podu vietas
        # Laika sarežģītība O(V^2)
        for node in self.graph:
            for node1 in self.graph[node]:
                if node < node1 and self.graph[node][node1] <= 0:
                    self.pot_edges.add((node, node1, self.graph[node][node1]))

    def remove_potted_edges(self):
        # Nodzēš visas šķautnes, kuras jau paslēpti medus podi
        # Laika sarežģītība O(E)
        for edge in self.pot_edges:
            if edge[0] in self.graph and edge[1] in self.graph[edge[0]]:
                del self.graph[edge[0]][edge[1]]
            if edge[1] in self.graph and edge[0] in self.graph[edge[1]]:
                del self.graph[edge[1]][edge[0]]

    def remove_branches(self):
        # Nodzes visus zarus
        # Laika sarežģītība O(N^2)
        for node in list(self.graph.keys()):
            if node in self.graph and len(self.graph[node]) == 1:
                while len(self.graph[node]) == 1:
                    next_node = list(self.graph[node].keys())[0]
                    del self.graph[node]
                    del self.graph[next_node][node]
                    node = next_node

    def find_MST(self):
        # Atrod Maksimālo pārklājošo koku
        # Heapq datu struktūra ir binārais koks kur vērtības ir sakārtotas
        # Tuple objekti tiek kārtoti pēc pirmās vērtības, tad otrās, utt.
        # Laika sarežģītība O(E logE)
        start_node = 0

        pq = [(0, start_node, start_node)]
        in_mst = set()
        mst_edges = []

        while pq:
            # Pop = O(logN)
            weight, node, source = heapq.heappop(pq)
            if node in in_mst:
                continue

            in_mst.add(node)

            if weight != 0:  # To exclude the starting node's weight
                mst_edges.append((node, source))

            for adjacent, w in self.graph[node].items():
                if adjacent not in in_mst:
                    # Push = O(logN)
                    heapq.heappush(pq, (-w, adjacent, node))

        self.mst_edges = mst_edges

    def add_edges_not_in_MST(self):
        # Pievieno medus sarakstam visas šķautnes, kuras nav Maksimālajā pārklājošajā kokā
        # Pievieno tikai šķautnes kurās sākums ir mazāks par beigām,
        # lai izvairītos no dublikātiem datu struktūras dēļ
        # Laika sarežģītība O(E)
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

    def potted_difficulty(self):
        # Atrod izvēlēto šķautņu kopējo sarežģītību
        # Laika sarežģītība O(E)
        difficulty = 0
        for edge in self.pot_edges:
            difficulty += edge[2]

        return difficulty

    def write_file(self):
        # Raksta izvaddatus
        # Laika sarežģītība O(E)
        with open(self.out_file, 'w') as f:
            f.write(str(self.potted_difficulty()))
            f.write('\n')
            for edge in self.pot_edges:
                f.write(str(edge[0] + 1) + ' ' + str(edge[1] + 1))
                f.write('\n')


Graph('sample_input_2023_3.txt', 'file.out')
