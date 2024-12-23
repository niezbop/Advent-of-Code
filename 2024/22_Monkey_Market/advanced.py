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


sequences = set()
sell_prices = dict()
for secret in initial_secrets:
    running_sequence = list()
    new_secret = secret
    sell_prices[secret] = dict()
    for _ in range(steps):
        previous_price = new_secret % 10
        new_secret = evolve(new_secret)
        price = new_secret % 10
        price_change = price - previous_price
        if preview:
            print(f"{new_secret} -> {price} {price_change}")

        running_sequence.append(price_change)
        if len(running_sequence) < 4:
            continue

        if len(running_sequence) == 5:
            running_sequence = running_sequence[1:]

        sequence = tuple(running_sequence)
        if sequence not in sell_prices[secret].keys():
            sequences.add(sequence)
            sell_prices[secret][sequence] = price

if preview:
    print(sell_prices)

max = ([None] * 4, -20)
for sequence in sequences:
    total_sell_value = 0
    for secret in initial_secrets:
        if sequence in sell_prices[secret].keys():
            total_sell_value += sell_prices[secret][sequence]

    if total_sell_value > max[1]:
        max = (sequence, total_sell_value)

print(max)
