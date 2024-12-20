from collections import defaultdict
from math import inf, sqrt
from time import sleep
import os
import sys

Map = list[list[bool]]
Vector2 = tuple[int, int]

args = sys.argv[1:]
source_path = args[0]
preview = False
if '--preview' in args:
    args.remove('--preview')
    preview = True
dimension = int(args[1]) if len(args) >= 2 else 70
obstacle_count = int(args[2]) if len(args) >= 3 else 1024

if not source_path:
    raise ValueError("No source file given")
if not os.path.isfile(source_path):
    raise ValueError(f"No file found at {source_path}")

with open(source_path, 'r') as file:
    obstacles = list(map(
        lambda line: tuple(reversed(tuple(map(int, line.strip().split(','))))),
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


def print_maze(maze: Map, refresh=False, path: list[Vector2] = None) -> None:
    if refresh:
        sys.stdout.write(f"\x1b[{dimension + 1}A\x1b[{dimension}K")
    payload = []
    for row in maze:
        payload.append(list(map(lambda b: '.' if b else '#', row)))
    if path:
        for (i, j) in path:
            payload[i][j] = 'O'
    print("\n".join(list(map(lambda row: ''.join(row), payload))))


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


def get_path(head: Vector2, history: dict[Vector2]) -> list[Vector2]:
    path = [head]
    parent = came_from[head]
    if parent in came_from.keys():
        path += get_path(parent, history)
    return path


if preview:
    print_maze(maze)
last_path = None
for new_obstacle in obstacles[obstacle_count:]:
    x, y = new_obstacle
    maze[x][y] = False
    if preview:
        print_maze(maze, refresh=True, path=last_path)
        sleep(0.1)
    if last_path and (x, y) not in last_path:
        continue
    try:
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
                last_path = get_path(end, came_from)
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

    except ValueError:
        print(f"Failed at {new_obstacle} ({obstacles.index(new_obstacle)})")
        break
