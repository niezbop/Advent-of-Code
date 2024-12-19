from collections import defaultdict
from math import inf, sqrt
import os
import sys

Map = list[list[str]]
Vector2 = tuple[int, int]

args = sys.argv[1:]
source_path = args[0]

if not source_path:
    raise ValueError("No source file given")
if not os.path.isfile(source_path):
    raise ValueError(f"No file found at {source_path}")

with open(source_path, 'r') as file:
    maze = list(map(lambda line: list(line.strip()), file.readlines()))


DIRECTIONS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]


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


def estimate_distance(a: Vector2, b: Vector2) -> float:
    ia, ja = a
    ib, jb = b
    return sqrt((ia-ib)**2 + (ja-jb)**2)


start, end = locate_start_end(maze)

# A* implementation
open_set = set()
start_vector = (start, (0, 1))
open_set.add(start_vector)

came_from = dict()

g_score = defaultdict(lambda: inf)
g_score[start_vector] = 0

f_score = defaultdict(lambda: inf)
f_score[start_vector] = estimate_distance(start, end)

shortest_route = None
while open_set:
    current = min(open_set, key=lambda node: f_score[node])
    if current[0] == end:
        shortest_route = g_score[current]
        break

    open_set.remove(current)
    position, orientation = current
    neighbours = []
    neighbours.append(
        ((position[0] + orientation[0], position[1] + orientation[1]), orientation))
    orientation_index = DIRECTIONS.index(orientation)
    for i in [-1, 1]:
        neighbours.append((position, DIRECTIONS[(orientation_index + i) % 4]))

    for neighbour in neighbours:
        neighbour_p, neighbour_o = neighbour
        x, y = neighbour_p
        if maze[x][y] == '#':
            continue

        neighbour_distance = 1 if orientation == neighbour_o else 1000
        tentative_g_score = g_score[current] + neighbour_distance
        if tentative_g_score < g_score[neighbour]:
            came_from[neighbour] = current
            g_score[neighbour] = tentative_g_score
            f_score[neighbour] = tentative_g_score + \
                estimate_distance(neighbour[0], end)
            open_set.add(neighbour)

if shortest_route is None:
    raise ValueError

print(shortest_route)
