import os
import sys

args = sys.argv[1:]
source_path = args[0]

if not source_path:
    raise ValueError("No source file give")
if not os.path.isfile(source_path):
    raise ValueError(f"No file found at {source_path}")

with open(source_path, 'r') as file:
    lines = file.readlines()
    reports = list(map(
        lambda line: list(map(lambda x: int(x), line.split(' '))),
        lines))


def is_safe(report: list[int]) -> bool:
    suite = list(zip(report[:-1], report[1:]))
    increasing = suite[0][0] < suite[0][1]
    for (item, following) in suite:
        if increasing ^ (item < following):
            return False
        difference = abs(item - following)
        if difference < 1 or difference > 3:
            return False

    return True


print(len(list(filter(is_safe, reports))))
