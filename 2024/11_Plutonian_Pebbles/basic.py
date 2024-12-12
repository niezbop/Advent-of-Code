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


def change(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    as_string = str(stone)
    if len(as_string) % 2 == 0:
        middle = int(len(as_string) / 2)
        return [int(as_string[:middle]), int(as_string[middle:])]

    return [stone * 2024]


def blink(stones: list[int]) -> list[int]:
    new_stones = []
    for stone in stones:
        new_stones += change(stone)

    return new_stones


for _ in range(25):
    stones = blink(stones)

print(len(stones))
