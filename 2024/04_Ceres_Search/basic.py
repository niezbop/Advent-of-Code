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
    (0, -1),  # Top
    (1, -1),  # Top-right
    (1, 0),  # Right
    (1, 1),  # Bottom-right
    (0, 1),  # Bottom
    (-1, 1),  # Bottom-left
    (-1, 0),  # Left
    (-1, -1),  # Top-left
]

count = 0
for i in range(height):
    for j in range(width):
        character = data[i][j]
        if character != 'X':
            continue

        for (u, v) in NEIGHBOURS:
            i_n = i + u
            j_n = j + v

            for letter in ['M', 'A', 'S']:
                # Check for out of bonds
                if i_n < 0 or i_n >= height or j_n < 0 or j_n >= width:
                    break
                if data[i_n][j_n] != letter:
                    break
                if letter == 'S':
                    count += 1
                    break

                i_n += u
                j_n += v

print(count)
