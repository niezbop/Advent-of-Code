import os
import sys

args = sys.argv[1:]
source_path = args[0]

if not source_path:
    raise ValueError("No source file given")
if not os.path.isfile(source_path):
    raise ValueError(f"No file found at {source_path}")

with open(source_path, 'r') as file:
    data = list(map(list, file.readlines()))

width = len(data[0])
height = len(data)

NEIGHBOURS = [
    (1, -1),  # Top-right
    (1, 1),  # Bottom-right
    (-1, 1),  # Bottom-left
    (-1, -1),  # Top-left
]

count = 0
for i in range(1, height - 1):
    for j in range(1, width - 1):
        character = data[i][j]
        if character != 'A':
            continue

        is_pattern = False
        for n in range(len(NEIGHBOURS)):
            u, v = NEIGHBOURS[n]
            if data[i + u][j + v] != 'M':
                continue
            if data[i - u][j - v] != 'S':
                continue
            u, v = NEIGHBOURS[(n + 1) % 4]
            if data[i + u][j + v] != 'M':
                continue
            if data[i - u][j - v] == 'S':
                is_pattern = True
                break

        if is_pattern:
            count += 1

print(count)
