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

i = 0
j = len(disk_map) - 1
block_start = block_end = None

while True:
    if disk_map[j] is None:
        j -= 1
        continue

    reading = disk_map[j]
    block_end = j
    while True:
        j -= 1
        if disk_map[j] is None or disk_map[j] != reading:
            break

    required_space = block_end - j
    i = 0
    while True:
        if i >= j:
            break

        if disk_map[i] is not None:
            i += 1
            continue

        block_start = i
        while True:
            i += 1
            if i >= len(disk_map) or disk_map[i] is not None:
                break

        available_space = i - block_start

        if required_space <= available_space:
            for k in range(required_space):
                disk_map[block_start + k], disk_map[block_end - k] = (
                    disk_map[block_end - k],
                    disk_map[block_start + k]
                )
            break

    if j <= 0:
        break

total = 0
for (i, value) in enumerate(disk_map):
    if value is None:
        continue

    total += i * value

print(total)
