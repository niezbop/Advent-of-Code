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

perimeters = defaultdict(lambda: 0)
areas = defaultdict(lambda: 0)
empty_row = [None] * len(garden[0])
indexed_garden = []
for i in range(len(garden)):
    indexed_garden.append(empty_row[:])
crops = []


def propagate_index(i: int, j: int, crop_index: int) -> None:
    if garden[i][j] != crops[crop_index]:
        perimeters[crop_index] += 1
        return

    if indexed_garden[i][j] is not None:
        return

    indexed_garden[i][j] = crop_index
    areas[crop_index] += 1
    for (u, v) in DIRECTIONS:
        i_n, j_n = (i+u, j+v)
        if i_n < 0 or i_n >= len(garden) or j_n < 0 or j_n >= len(garden[0]):
            perimeters[crop_index] += 1
            continue
        propagate_index(i_n, j_n, crop_index)


for (i, row) in enumerate(garden):
    for (j, char) in enumerate(row):
        if indexed_garden[i][j] is None:
            crops.append(garden[i][j])
            crop_index = len(crops) - 1
            propagate_index(i, j, crop_index)

total = 0
for (i, crop) in enumerate(crops):
    # print(f"Crop {crop}: area {areas[i]}, perimeter {perimeters[i]}")
    total += perimeters[i] * areas[i]

print(total)
