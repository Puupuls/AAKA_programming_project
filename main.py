import re

def minimum_spanning_tree(graph, start):
    # O(E log E)
    mst = set()
    visited = set([start])
    edges = [
        (cost, start, to)
        for to, cost in graph[start].items()
    ]
    while edges:
        edges.sort()
        cost, frm, to = edges.pop(0)
        if to not in visited:
            visited.add(to)
            mst.add((frm, to, cost))
            for to_next, cost2 in graph[to].items():
                if to_next not in visited:
                    edges.append((cost2, to, to_next))
    return mst


def find_cycles(mst, N):
    # O(V + E)
    graph = [[] for _ in range(N)]
    for frm, to, _ in mst:
        graph[frm].append(to)
        graph[to].append(frm)
    cycle = set()
    visited = [0]*N

    def dfs(v, parent):
        visited[v] = 1
        for to in graph[v]:
            if to == parent:
                continue
            if visited[to] == 1:
                cycle.add((min(v, to), max(v, to)))
            elif visited[to] == 0:
                dfs(to, v)
        visited[v] = 2

    dfs(0, -1)
    return cycle


def place_honey_pots(edges, cycle):
    # O(E)
    dp = [0]*(len(edges)+1)
    edges.sort(key=lambda x: x[2])
    cycle = set(cycle)
    for i in range(1, len(edges)+1):
        dp[i] = dp[i-1]
        if (edges[i-1][0], edges[i-1][1]) in cycle:
            dp[i] = min(dp[i], dp[i-1]+edges[i-1][2])
    return dp[-1]


with open('in.txt', 'r') as f:
    input_data = f.read()
    input_data = re.sub(r'[\n\r]+', ' ', input_data)
    input_data = re.sub(r'\t+', ' ', input_data)
    input_data = re.sub(r' +', ' ', input_data)
input_data = input_data.split(' ')
input_data = [int(i) for i in input_data]

N = input_data[0]
input_data = input_data[1:]

graph = {}
while len(input_data) > 0:
    u, v, w = input_data[:3]
    input_data = input_data[3:]
    u -= 1
    v -= 1
    if u not in graph:
        graph[u] = {}
    if v not in graph:
        graph[v] = {}
    graph[u][v] = w
    graph[v][u] = w

mst = minimum_spanning_tree(graph, 0)
cycle = find_cycles(mst, N)
result = place_honey_pots(list(mst), cycle)
print(result)
