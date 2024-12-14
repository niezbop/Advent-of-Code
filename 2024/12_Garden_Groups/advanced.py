from collections import defaultdict
import os
import sys

args = sys.argv[1:]
source_path = args[0]

if not source_path:
    raise ValueError("No source file given")
if not os.path.isfile(source_path):
    raise ValueError(f"No file found at {source_path}")

with open(source_path, 'r') as file:
    garden = list(map(lambda line: line.strip(), file.readlines()))

DIRECTIONS = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1)
]

angles = defaultdict(lambda: 0)
areas = defaultdict(lambda: 0)
empty_row = [None] * len(garden[0])
indexed_garden = []
for i in range(len(garden)):
    indexed_garden.append(empty_row[:])
crops = []


def propagate_index(i: int, j: int, crop_index: int) -> None:
    if garden[i][j] != crops[crop_index]:
        return

    if indexed_garden[i][j] is not None:
        return

    indexed_garden[i][j] = crop_index
    areas[crop_index] += 1
    for (u, v) in DIRECTIONS:
        i_n, j_n = (i+u, j+v)
        if i_n < 0 or i_n >= len(garden) or j_n < 0 or j_n >= len(garden[0]):
            continue
        propagate_index(i_n, j_n, crop_index)


def indexed_garden_at(i: int, j: int, fallback: int = None) -> int:
    if i < 0 or i >= len(garden) or j < 0 or j >= len(garden[0]):
        return fallback

    return indexed_garden[i][j]


def parse_shape(i: int, j: int) -> None:
    crop = indexed_garden[i][j]
    angles = 0
    for offset in range(len(DIRECTIONS)):
        u = DIRECTIONS[offset]
        v = DIRECTIONS[(offset + 1) % 4]
        outer_angle = [u, (u[0]+v[0], u[1]+v[1]), v]
        outer = list(map(lambda d: indexed_garden_at(
            i+d[0], j+d[1]), outer_angle))

        if outer[0] != crop and outer[2] != crop:
            angles += 1  # Inner angle
        elif outer[0] == crop and outer[2] == crop and outer[1] != crop:
            angles += 1  # Outer angle

    return angles


for (i, row) in enumerate(garden):
    for (j, char) in enumerate(row):
        if indexed_garden[i][j] is None:
            crops.append(garden[i][j])
            crop_index = len(crops) - 1
            propagate_index(i, j, crop_index)

for i in range(len(garden)):
    for j in range(len(garden[i])):
        crop_index = indexed_garden[i][j]
        angles[crop_index] += parse_shape(i, j)


total = 0
for (i, crop) in enumerate(crops):
    total += angles[i] * areas[i]

print(total)
