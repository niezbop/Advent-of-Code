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


def validate_pattern(prefix: str, pattern: str, towels: list[str]) -> bool:
    if pattern == '':
        return True

    if (prefix, pattern) in memory:
        return memory[(prefix, pattern)]

    matching = list(reversed(sorted(filter(
        lambda towel: pattern.startswith(towel),
        towels), key=len)))

    ok = False
    for towel in matching:
        ok = ok or validate_pattern(
            prefix + pattern[:len(towel)], pattern[len(towel):], towels)

    memory[(prefix, pattern)] = ok
    return ok


ok_patterns = 0
for i, pattern in enumerate(patterns):
    sys.stdout.write(f"\rPattern {i+1}/{len(patterns)}")
    if validate_pattern('', pattern, towels):
        ok_patterns += 1

print('')
print(ok_patterns)
