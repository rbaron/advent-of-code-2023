import fileinput
import itertools
from collections import defaultdict, deque


def parse():
    res = {}
    for l in fileinput.input():
        node, children = l.split(": ")
        res[node] = set(c.strip() for c in children.split(" "))
    fixed = defaultdict(set)
    # May not be necessary.
    for node, children in res.items():
        for child in children:
            fixed[node].add(child)
            fixed[child].add(node)
    return fixed


def get_edges(graph):
    edges = set()
    for node, children in graph.items():
        for child in children:
            edges.add(tuple(sorted((node, child))))
    return edges


def get_visitable(graph, edges_to_ignore):
    # Start from any node.
    start = next(iter(graph.keys()))
    visited = set()
    q = deque([start])
    while q:
        node = q.popleft()
        if node in visited:
            continue
        visited.add(node)
        for child in graph[node]:
            if tuple(sorted((node, child))) not in edges_to_ignore:
                q.append(child)
    return len(visited)


def get_dot(graph):
    print("graph connections {")
    for node, children in graph.items():
        for child in children:
            print(f"{node} -- {child};")
    print("}")


G = parse()
edges = get_edges(G)

# Pipe to a file to visualize it.
# get_dot(G)

# By visual inspection I see these two edges connect two clusters. Let's find the other one.
edges_to_ignore = set([("dbt", "tjd"), ("mgb", "plt")])
for e in edges:
    n_visited = get_visitable(G, edges_to_ignore | {e})
    if n_visited != len(G):
        print(n_visited * (len(G) - n_visited))
        break
