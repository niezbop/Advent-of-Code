from collections import defaultdict
import functools
import os
import sys

args = sys.argv[1:]
source_path = args[0]

if not source_path:
    raise ValueError("No source file give")
if not os.path.isfile(source_path):
    raise ValueError(f"No file found at {source_path}")

left = []
right = defaultdict(lambda: 0)
with open(source_path, 'r') as file:
    for line in file.readlines():
        l, r = map(lambda x: int(x), line.split('   '))
        left.append(l)
        right[r] += 1


def reductor(acc: int, value: int) -> int:
    return acc + value * right[value]


print(functools.reduce(reductor, left, 0))
