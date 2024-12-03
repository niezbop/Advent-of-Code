import re
import os
import sys

args = sys.argv[1:]
source_path = args[0]

if not source_path:
    raise ValueError("No source file given")
if not os.path.isfile(source_path):
    raise ValueError(f"No file found at {source_path}")

with open(source_path, 'r') as file:
    data = file.read()

query = 'mul\([0-9]+,[0-9]+\)'

total = 0
for match in re.findall(query, data):
    a, b = map(lambda x: int(x), match[4:-1].split(','))
    total += a * b

print(total)
