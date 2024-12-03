import functools
import os
import sys

args = sys.argv[1:]
source_path = args[0]

if not source_path:
    raise ValueError("No source file given")
if not os.path.isfile(source_path):
    raise ValueError(f"No file found at {source_path}")

left = []
right = []
with open(source_path, 'r') as file:
    for line in file.readlines():
        l, r = map(lambda x: int(x), line.split('   '))
        left.append(l)
        right.append(r)


def reductor(acc: int, tup: tuple[int, int]) -> int:
    l, r = tup
    return acc + abs(l-r)


print(functools.reduce(reductor, zip(sorted(left), sorted(right)), 0))
