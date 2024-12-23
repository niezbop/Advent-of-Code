import os
import sys

args = sys.argv[1:]
preview = False
if '--preview' in args:
    args.remove('--preview')
    preview = True
source_path = args[0]
steps = int(args[1]) if len(args) >= 2 else 2_000

if not source_path:
    raise ValueError("No source file given")
if not os.path.isfile(source_path):
    raise ValueError(f"No file found at {source_path}")

with open(source_path, 'r') as file:
    initial_secrets = list(map(
        lambda line: int(line.strip()),
        file.readlines()))


def mix(secret: int, value: int) -> int:
    return secret ^ value


def prune(secret: int) -> int:
    return secret % 16777216


def evolve(secret: int) -> int:
    # First step
    output = prune(mix(secret, secret * 64))
    # Second step
    output = prune(mix(output, output // 32))
    # Third step
    output = prune(mix(output, output * 2048))

    return output


total = 0
for secret in initial_secrets:
    new_secret = secret
    for _ in range(steps):
        new_secret = evolve(new_secret)
        if preview:
            print(new_secret)

    total += new_secret
    print(f"{secret}: {new_secret}")

print(total)
