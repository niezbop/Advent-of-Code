import os
import sys

args = sys.argv[1:]
source_path = args[0]

if not source_path:
    raise ValueError("No source file given")
if not os.path.isfile(source_path):
    raise ValueError(f"No file found at {source_path}")


def concatenate(a: int, b: int) -> int:
    return (a * (10**len(str(b))) + b)


def parse_calibration(line: str) -> tuple[int, list[int]]:
    test_value, rest = line.split(': ', 1)
    test_value = int(test_value)

    calibrations = list(map(int, rest.split(' ')))
    return (test_value, calibrations)


def get_possibilities(calibrations: list[int]) -> list[int]:
    if len(calibrations) < 2:
        raise ValueError
    if len(calibrations) == 2:
        return [
            calibrations[0] * calibrations[1],
            calibrations[0] + calibrations[1],
            concatenate(calibrations[0], calibrations[1]),
        ]

    last = calibrations[-1]
    sub_possibilities = map(
        lambda x: [x * last, x + last, concatenate(x, last)],
        get_possibilities(calibrations[:-1]))
    return [i for j in sub_possibilities for i in j]


with open(source_path, 'r') as file:
    equations = list(map(parse_calibration, file.readlines()))

total = 0
for (value, calibrations) in equations:
    if value not in get_possibilities(calibrations):
        continue

    total += value

print(total)
