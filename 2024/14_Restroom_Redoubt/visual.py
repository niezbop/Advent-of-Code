from time import sleep
import os
import sys

WIDTH = 101
HEIGHT = 103

Vector2 = tuple[int, int]

args = sys.argv[1:]
PLAY = '--play'
OFFSET = '--offset'
should_play = False
if PLAY in args:
    should_play = True
    args.remove(PLAY)
offset = 0
if OFFSET in args:
    offset_arg = args[args.index(OFFSET) + 1]
    offset = int(offset_arg)
    args.remove(OFFSET)
    args.remove(offset_arg)

source_path = args[0]

if not source_path:
    raise ValueError("No source file given")
if not os.path.isfile(source_path):
    raise ValueError(f"No file found at {source_path}")

with open(source_path, 'r') as file:
    lines = list(map(lambda line: line.strip(), file.readlines()))


def parse_robot(line: str) -> tuple[Vector2, Vector2]:
    position_statement, speed_statement = line.split(' ')
    _, position_statement = position_statement.split('p=')
    _, speed_statement = speed_statement.split('v=')

    return (
        tuple(map(int, position_statement.split(','))),
        tuple(map(int, speed_statement.split(',')))
    )


def move_robot(position: Vector2, speed: Vector2) -> Vector2:
    (x, y), (u, v) = (position, speed)
    return ((x+u) % WIDTH, (y+v) % HEIGHT)


def move_robots(robots: list[Vector2], speeds: list[Vector2]) -> None:
    for i, robot in enumerate(robots):
        robots[i] = move_robot(robot, speeds[i])


def print_state(robots: list[Vector2], frame: int, refresh: bool) -> None:
    if refresh:
        sys.stdout.write(f"\x1b[{HEIGHT + 1}A\x1b[{HEIGHT + 1}K")
    payload = list()
    for _ in range(HEIGHT):
        payload.append(['.'] * WIDTH)
    for robot in robots:
        i, j = robot
        payload[j][i] = 'X'

    print(frame)
    print("\n".join(list(map(lambda row: ''.join(row), payload))))


robots = list()
speeds = list()
for line in lines:
    position, speed = parse_robot(line)
    robots.append(position)
    speeds.append(speed)

frame = 0
for frame in range(offset):
    move_robots(robots, speeds)

print_state(robots, frame, False)
if should_play:
    while True:
        sleep(0.1)
        move_robots(robots, speeds)
        frame += 1
        print_state(robots, frame, True)
