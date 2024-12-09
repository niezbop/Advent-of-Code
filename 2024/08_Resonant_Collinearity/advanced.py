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
    lines = list(map(lambda line: line.strip(), file.readlines()))

antennas = defaultdict(list)
for (i, line) in enumerate(lines):
    for (j, char) in enumerate(line.strip()):
        if char != '.':
            antennas[char].append((i, j))

height, width = (len(lines), len(lines[0]))
antinodes = set()
for frequency in antennas:
    positions = antennas[frequency]
    for (i0, j0) in positions:
        for (i1, j1) in positions:
            if (i0, j0) == (i1, j1):
                continue

            u, v = (i1 - i0, j1 - j0)
            ia, ja = (i0, j0)
            while True:
                ia, ja = (ia + u, ja + v)
                if ia < 0 or ia >= height or ja < 0 or ja >= width:
                    break
                antinodes.add((ia, ja))

print(len(antinodes))
