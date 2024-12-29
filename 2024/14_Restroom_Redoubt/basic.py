import os
import sys

WIDTH = 101
HEIGHT = 103

args = sys.argv[1:]
source_path = args[0]

if not source_path:
    raise ValueError("No source file given")
if not os.path.isfile(source_path):
    raise ValueError(f"No file found at {source_path}")

with open(source_path, 'r') as file:
    lines = list(map(lambda line: line.strip(), file.readlines()))


def parse_robot(line: str) -> tuple[tuple[int, int], tuple[int, int]]:
    position_statement, speed_statement = line.split(' ')
    _, position_statement = position_statement.split('p=')
    _, speed_statement = speed_statement.split('v=')

    return (
        tuple(map(int, position_statement.split(','))),
        tuple(map(int, speed_statement.split(',')))
    )


def move_robot(robot: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    (x, y), (u, v) = robot
    return (
        ((x+u) % WIDTH, (y+v) % HEIGHT),
        (u, v),
    )


def print_state(robots: tuple[tuple[int, int], tuple[int, int]]) -> None:
    for j in range(HEIGHT):
        row = map(lambda i: len(
            list(filter(lambda r: r[0] == (i, j), robots))), range(WIDTH))
        line = map(lambda count: '.' if count == 0 else str(count), row)
        print(''.join(line))


robots = list(map(parse_robot, lines))
for _ in range(100):
    robots = list(map(move_robot, robots))

mid_width = WIDTH // 2
mid_height = HEIGHT // 2
quadrants = [0] * 4
for (x, y), _ in robots:
    if x == mid_width or y == mid_height:
        continue

    index = 0
    if x > mid_width:
        index += 1
    if y > mid_height:
        index += 2
    quadrants[index] += 1


safety_factor = 1
for i in quadrants:
    safety_factor *= i

print(safety_factor)
