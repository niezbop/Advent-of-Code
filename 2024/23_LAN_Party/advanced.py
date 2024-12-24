from collections import defaultdict
import os
import sys

args = sys.argv[1:]
source_path = args[0]
preview = '--preview' in args

if not source_path:
    raise ValueError("No source file given")
if not os.path.isfile(source_path):
    raise ValueError(f"No file found at {source_path}")

with open(source_path, 'r') as file:
    lines = list(map(lambda line: line.strip(), file.readlines()))

graph = defaultdict(set)
for line in lines:
    a, b = line.split('-')
    graph[a].add(b)
    graph[b].add(a)


def hashable(group: set[str]) -> tuple[str]:
    return tuple(sorted(group))


def add_to_network(
        node: str,
        network: set[str],
        graph: dict[str, set[str]],
        networks: set[tuple[str]]) -> bool:
    # If at least one neighbour isn't in the budding network,
    # this node isn't part of the network
    if network & graph[node] != network:
        return False

    network.add(node)

    any_added = False
    for neighbour in graph[node]:
        any_added = any_added or add_to_network(
            neighbour,
            network,
            graph,
            networks)

    if any_added:
        return True

    networks.add(tuple(sorted(network)))
    return True


networks = set()
for i, (node, neighbours) in enumerate(graph.items()):
    if preview:
        print(f"{node} ({i+1}/{len(graph)})")
    network = set()
    add_to_network(node, network, graph, networks)

if preview:
    print(networks)

biggest_network = sorted(networks, key=len)[-1]
print(','.join(biggest_network))
