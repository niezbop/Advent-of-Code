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
    towels = file.readline().strip().split(', ')
    file.readline()
    patterns = list(map(lambda line: line.strip(), file.readlines()))


memory = defaultdict(lambda: False)


def arrangements(prefix: str, pattern: str, towels: list[str]) -> int:
    if pattern == '':
        return 1

    if (prefix, pattern) in memory:
        return memory[(prefix, pattern)]

    matching = list(reversed(sorted(filter(
        lambda towel: pattern.startswith(towel),
        towels), key=len)))

    ok = 0
    for towel in matching:
        ok += arrangements(
            prefix + pattern[:len(towel)], pattern[len(towel):], towels)

    memory[(prefix, pattern)] = ok
    return ok


all_arrangements = 0
for i, pattern in enumerate(patterns):
    sys.stdout.write(f"\rPattern {i+1}/{len(patterns)}")
    all_arrangements += arrangements('', pattern, towels)

print('')
print(all_arrangements)
