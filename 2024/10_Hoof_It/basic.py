import os
import sys

args = sys.argv[1:]
source_path = args[0]

if not source_path:
    raise ValueError("No source file given")
if not os.path.isfile(source_path):
    raise ValueError(f"No file found at {source_path}")

with open(source_path, 'r') as file:
    height_map = list(map(
        lambda line: list(map(int, line.strip())), file.readlines()))

DIRECTIONS = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1)
]


def follow_path(i: int, j: int, height_map: list[str]) -> set[tuple[int, int]]:
    value = height_map[i][j]
    paths = set()
    for (u, v) in DIRECTIONS:
        i_n, j_n = (i + u, j + v)
        if i_n < 0 or i_n >= len(height_map) or j_n < 0 or j_n >= len(height_map[0]):
            continue

        if height_map[i_n][j_n] == value + 1:
            if value == 8:
                paths.add((i_n, j_n))
            else:
                paths = paths.union(follow_path(i_n, j_n, height_map))

    return paths


trails = 0
for i in range(len(height_map)):
    for j in range(len(height_map[i])):
        if height_map[i][j] == 0:
            trailheads = follow_path(i, j, height_map)
            trails += len(trailheads)

print(trails)
