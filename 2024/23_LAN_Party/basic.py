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

three_computer_groups = set()
for node, neighbours in graph.items():
    if len(neighbours) < 2:
        continue
    for neighbour in neighbours:
        for other_neighbour in neighbours:
            if neighbour == other_neighbour:
                continue
            if other_neighbour in graph[neighbour]:
                three_computer_groups.add(
                    tuple(sorted((node, neighbour, other_neighbour))))

chief_candidates = {n for n in graph.keys() if n.startswith('t')}
count = 0
for group in three_computer_groups:
    if chief_candidates & set(group):
        count += 1

print(count)
