from collections import defaultdict
from math import inf, sqrt, copysign
from time import sleep
import os
import sys

Map = list[list[str]]
Vector2 = tuple[int, int]
Node = tuple[Vector2, Vector2]

args = sys.argv[1:]
source_path = args[0]
preview = '--preview' in args

if not source_path:
    raise ValueError("No source file given")
if not os.path.isfile(source_path):
    raise ValueError(f"No file found at {source_path}")

with open(source_path, 'r') as file:
    maze = list(map(lambda line: list(line.strip()), file.readlines()))

DIRECTION_SYMBOLS = {
    (1, 0): '^',
    (0, 1): '>',
    (-1, 0): 'v',
    (0, -1): '<'
}

DIRECTIONS = list(DIRECTION_SYMBOLS.keys())


def locate_start_end(maze: Map) -> tuple[Vector2, Vector2]:
    start_tile = end_tile = None
    for (i, row) in enumerate(maze):
        for (j, char) in enumerate(row):
            if char == 'E':
                end_tile = (i, j)
            elif char == 'S':
                start_tile = (i, j)

            if end_tile and start_tile:
                return (start_tile, end_tile)
    raise ValueError


def estimate_distance(
        source: Vector2,
        target: Vector2,
        facing: Vector2 = None) -> float:

    vertical = target[0] - source[0]
    horizontal = target[1] - source[1]
    distance = sqrt(horizontal**2 + vertical**2)
    if facing:
        if vertical and copysign(1, facing[0]) != copysign(1, vertical):
            distance += 1000
        if horizontal and copysign(1, facing[1]) != copysign(1, horizontal):
            distance += 1000
        pass

    return distance


def reached_tiles(history: dict[list[Node]], node: Node) -> set[Vector2]:
    tiles = {node[0]}
    for parent in history[node]:
        tiles = tiles.union(reached_tiles(history, parent))
    return tiles


def print_map(
        maze: Map,
        heads: set[Node] = set(),
        reached: set[Vector2] = set(),
        refresh: bool = False):
    if refresh:
        amount = len(maze)
        sys.stdout.write(f"\x1b[{amount}A\x1b[{amount}K")

    clone = []
    for row in maze:
        clone.append(row.copy())

    for (i, j) in list(reached):
        clone[i][j] = 'O'

    for ((i, j), _) in list(heads):
        clone[i][j] = 'H'

    print("\n".join(map(lambda row: ''.join(row), clone)))


if preview:
    print_map(maze)

start, end = locate_start_end(maze)

open_set = set()
start_node = (start, (0, 1))
open_set.add(start_node)

came_from = defaultdict(list)

g_score = defaultdict(lambda: inf)
g_score[start_node] = 0

f_score = defaultdict(lambda: inf)
f_score[start_node] = estimate_distance(start, end)

shortest_route = None
while open_set:
    current = min(open_set, key=lambda node: f_score[node])
    if preview:
        sleep(0.1)
        print_map(
            maze,
            heads=open_set,
            reached=reached_tiles(came_from, current),
            refresh=True)

    open_set.remove(current)
    if current[0] == end:
        shortest_route = g_score[current]
        continue

    if shortest_route and g_score[current] > shortest_route:
        continue

    position, orientation = current
    neighbours = []
    neighbours.append(
        ((position[0] + orientation[0], position[1] + orientation[1]), orientation))
    orientation_index = DIRECTIONS.index(orientation)
    for i in [-1, 1]:
        u, v = new_orientation = DIRECTIONS[(orientation_index + i) % 4]
        if maze[position[0] + u][position[1] + v] != '#':
            neighbours.append((position, new_orientation))

    for neighbour in neighbours:
        neighbour_p, neighbour_o = neighbour
        x, y = neighbour_p
        if maze[x][y] == '#':
            continue

        neighbour_distance = 1 if orientation == neighbour_o else 1000
        tentative_g_score = g_score[current] + neighbour_distance
        if tentative_g_score < g_score[neighbour]:
            came_from[neighbour] = [current]
            g_score[neighbour] = tentative_g_score
            f_score[neighbour] = tentative_g_score + \
                estimate_distance(neighbour[0], end)
            open_set.add(neighbour)
        elif tentative_g_score == g_score[neighbour]:
            came_from[neighbour].append(current)

if not shortest_route:
    raise ValueError

print(shortest_route)

tiles = set()
final_nodes = list()
for node in came_from.keys():
    if node[0] == end:
        final_nodes.append(node)

for node in final_nodes:
    tiles = tiles.union(reached_tiles(came_from, node))

if preview:
    print_map(maze, reached=tiles, refresh=True)

print(len(tiles))
