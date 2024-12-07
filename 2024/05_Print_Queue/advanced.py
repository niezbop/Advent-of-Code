from functools import cmp_to_key
import os
import sys

args = sys.argv[1:]
source_path = args[0]

if not source_path:
    raise ValueError("No source file given")
if not os.path.isfile(source_path):
    raise ValueError(f"No file found at {source_path}")

with open(source_path, 'r') as file:
    constraints = []
    while True:
        line = file.readline()
        if line.isspace():
            break

        constraints.append(tuple(map(int, line.split('|'))))

    updates = file.readlines()


def constraints_comparator(x, y):
    if (x, y) in constraints:
        return -1
    elif (y, x) in constraints:
        return 1
    else:
        return 0


total = 0
for update in updates:
    pages_to_produce = list(map(int, update.split(',')))
    sorted_pages = sorted(
        pages_to_produce, key=cmp_to_key(constraints_comparator))

    if pages_to_produce == sorted_pages:
        continue

    half_point = int(len(sorted_pages) / 2.0)
    total += sorted_pages[half_point]

print(total)
