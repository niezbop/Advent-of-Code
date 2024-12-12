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
    line = file.read().strip()

stones = list(map(int, line.split(' ')))

memory = defaultdict(dict)


def change(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    as_string = str(stone)
    if len(as_string) % 2 == 0:
        middle = int(len(as_string) / 2)
        return [int(as_string[:middle]), int(as_string[middle:])]

    return [stone * 2024]


def recursive_blink(value: int, steps: int) -> int:
    count = 0
    if steps in memory[value]:
        return memory[value][steps]

    sub_stones = change(value)
    if steps == 1:
        count = len(sub_stones)
    else:
        for sub_value in sub_stones:
            count += recursive_blink(sub_value, steps - 1)

    memory[value][steps] = count
    return count


total = 0
for value in stones:
    total += recursive_blink(value, 75)

print(total)
