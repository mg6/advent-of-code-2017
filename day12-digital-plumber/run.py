#!/usr/bin/env python3


from collections import defaultdict


def complete_neighbours(graph):
    for node, neighbours in graph.items():
        for neighbour in neighbours:
            if node not in graph[neighbour]:
                graph[neighbour].add(node)
    return graph


def flood(graph, start_node, visited=None):
    if not visited:
        visited = set([start_node])

    for neighbour in graph[start_node]:
        if neighbour not in visited:
            visited.add(neighbour)
            flood(graph, neighbour, visited)

    return visited


def groups(graph, start_node=0):
    while len(graph):
        node = next(iter(graph))
        fl = flood(graph, node)
        yield fl
        for neighbour in fl:
            del graph[neighbour]


def count_groups(graph):
    return sum(1 for group in groups(graph))


completed = {0: {2, 3}, 2: {0, 3}, 3: {0, 2}}
assert complete_neighbours(completed) == completed

actual = complete_neighbours({0: {2}, 2: {3}, 3: set()})
expected = {0: {2}, 2: {0, 3}, 3: {2}}
assert actual == expected

actual = complete_neighbours({0: {2}, 2: {3}, 3: {0}})
expected = {0: {2, 3}, 2: {0, 3}, 3: {0, 2}}
assert actual == expected

g = {
    0: {2},
    1: {1},
    2: {0, 3, 4},
    3: {2, 4},
    4: {2, 3, 6},
    5: {6},
    6: {4, 5},
}

assert flood(g, 0) == {0, 2, 3, 4, 5, 6}
assert flood(g, 1) == {1}

assert count_groups(g) == 2


if __name__ == '__main__':
    with open('input') as f:
        s = f.read().strip()

        graph = defaultdict(set)
        edges = s.split('\n')

        for edge in edges:
            vertex, neighbours = edge.split(' <-> ')
            vertex, neighbours = int(vertex), map(int, neighbours.split(', '))
            graph[vertex].update(neighbours)

        graph = complete_neighbours(graph)
        print(len(flood(graph, 0)))
        print(count_groups(graph))
