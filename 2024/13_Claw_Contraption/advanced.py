from collections import defaultdict
from operator import itemgetter
import os
import sys


OFFSET = 10000000000000

args = sys.argv[1:]
source_path = args[0]

if not source_path:
    raise ValueError("No source file given")
if not os.path.isfile(source_path):
    raise ValueError(f"No file found at {source_path}")

with open(source_path, 'r') as file:
    lines = file.readlines()

arcades = []
for i in range((len(lines) + 1) // 4):
    arcade = defaultdict(dict)
    for j in range(2):
        line = lines[i * 4 + j].strip()
        prefix, values = line.split(': ')
        button = prefix.split('Button ')[1]
        for value in values.split(', '):
            axis, amount = value.split('+')
            arcade[button][axis] = int(amount)

    line = lines[i * 4 + 2]
    _, values = line.split(': ')
    for value in values.split(', '):
        axis, position = value.split('=')
        arcade['Prize'][axis] = int(position) + OFFSET

    arcades.append(arcade)

position_getter = itemgetter('X', 'Y')


# Given a pushes of A and b pushes of B
# i = xa * a + xb * b
# j = ya * a + yb * b
def solve(a: tuple[int, int], b: tuple[int, int], prize: tuple[int, int]) -> tuple[int, int]:
    xa, ya = a
    xb, yb = b
    i, j = prize

    det_main = xa * yb - xb * ya
    if det_main == 0:
        return None

    det_a = i * yb - j * xb
    det_b = j * xa - i * ya

    solution = (det_a / det_main, det_b / det_main)
    if not all(value.is_integer() for value in solution):
        return None

    return tuple(map(int, solution))


tokens = 0
for arcade in arcades:
    solution = solve(
        position_getter(arcade['A']),
        position_getter(arcade['B']),
        position_getter(arcade['Prize'])
    )

    if solution is None:
        continue
    a, b = solution
    tokens += a * 3 + b

print(tokens)
