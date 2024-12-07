import os
import sys

args = sys.argv[1:]
source_path = args[0]

if not source_path:
    raise ValueError("No source file given")
if not os.path.isfile(source_path):
    raise ValueError(f"No file found at {source_path}")

with open(source_path, 'r') as file:
    plan = file.readlines()

DIRECTIONS = [
    (-1, 0),  # Top
    (0, 1),  # Right
    (1, 0),  # Bottom
    (0, -1),  # Left
]

visited = []
guard = None
for (i, line) in enumerate(plan):
    for (j, char) in enumerate(plan[i]):
        if char == '^':
            guard = ((i, j), 0)
            visited.append((i, j))
            break

print(f"Guard at {guard[0]} facing {DIRECTIONS[guard[1]]}")

while True:
    x = guard[0][0] + DIRECTIONS[guard[1]][0]
    y = guard[0][1] + DIRECTIONS[guard[1]][1]
    # Check for out of bonds
    if x < 0 or x >= len(plan) or y < 0 or y >= len(plan[0]):
        break

    # Check for occupied space
    if plan[x][y] == '#':
        guard = (guard[0], (guard[1] + 1) % 4)
        continue

    guard = ((x, y), guard[1])
    if not (x, y) in visited:
        visited.append((x, y))

print(len(visited))
