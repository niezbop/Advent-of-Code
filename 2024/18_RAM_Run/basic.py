from collections import defaultdict
from math import inf, sqrt
import os
import sys

Map = list[list[bool]]
Vector2 = tuple[int, int]

args = sys.argv[1:]
source_path = args[0]
dimension = int(args[1]) if len(args) >= 2 else 70
obstacle_count = int(args[2]) if len(args) >= 3 else 1024

if not source_path:
    raise ValueError("No source file given")
if not os.path.isfile(source_path):
    raise ValueError(f"No file found at {source_path}")

with open(source_path, 'r') as file:
    obstacles = list(map(
        lambda line: reversed(tuple(map(int, line.strip().split(',')))),
        file.readlines()))

maze = list(map(
    lambda _: list(map(
        lambda _: True,
        range(dimension + 1))),
    range(dimension + 1)))

start = (0, 0)
end = (dimension, dimension)

for (i, j) in obstacles[:obstacle_count]:
    maze[i][j] = False


def print_maze(maze: Map) -> None:
    for row in maze:
        line = list(map(lambda b: '.' if b else '#', row))
        print(''.join(line))


print_maze(maze)


DIRECTIONS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]


def estimate_distance(a: Vector2, b: Vector2) -> float:
    ia, ja = a
    ib, jb = b
    return sqrt((ia-ib)**2 + (ja-jb)**2)


# A* implementation
open_set = set()
open_set.add(start)

came_from = dict()
came_from[start] = None

g_score = defaultdict(lambda: inf)
g_score[start] = 0

f_score = defaultdict(lambda: inf)
f_score[start] = estimate_distance(start, end)

shortest_route = None
while open_set:
    current = min(open_set, key=lambda node: f_score[node])
    if current == end:
        shortest_route = g_score[current]
        break

    open_set.remove(current)
    i, j = current
    for (u, v) in DIRECTIONS:
        x, y = neighbour = (i+u, j+v)
        if x < 0 or x > dimension or y < 0 or y > dimension:
            continue
        if not maze[x][y]:
            continue
        if neighbour == came_from[current]:
            continue

        tentative_g_score = g_score[current] + 1
        if tentative_g_score < g_score[neighbour]:
            came_from[neighbour] = current
            g_score[neighbour] = tentative_g_score
            f_score[neighbour] = tentative_g_score + \
                estimate_distance(neighbour, end)
            open_set.add(neighbour)

if shortest_route is None:
    raise ValueError

print(shortest_route)
