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

total = 0

for update in updates:
    pages_to_produce = list(map(int, update.split(',')))
    in_order = True
    for (a, b) in constraints:
        try:
            i_a = pages_to_produce.index(a)
            i_b = pages_to_produce.index(b)

            if i_a > i_b:
                in_order = False
                break
        except ValueError:
            continue

    if in_order:
        half_point = int(len(pages_to_produce) / 2.0)
        total += pages_to_produce[half_point]

print(total)
