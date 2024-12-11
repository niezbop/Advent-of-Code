import os
import sys

args = sys.argv[1:]
source_path = args[0]

if not source_path:
    raise ValueError("No source file given")
if not os.path.isfile(source_path):
    raise ValueError(f"No file found at {source_path}")

with open(source_path, 'r') as file:
    line = file.read().strip()

current_id = 0
disk_map = []
is_file = True
for char in line:
    value = int(char)
    if is_file:
        disk_map += [current_id] * value
        current_id += 1
    else:
        disk_map += [None] * value
    is_file = not is_file

for i in range(len(disk_map)):
    if disk_map[i] is not None:
        continue

    j = next(j for j in reversed(range(len(disk_map)))
             if disk_map[j] is not None)

    if i + 1 >= j:
        break

    disk_map[i], disk_map[j] = (disk_map[j], disk_map[i])

total = 0
for (i, value) in enumerate(disk_map):
    if value is None:
        break

    total += i * value

print(total)
