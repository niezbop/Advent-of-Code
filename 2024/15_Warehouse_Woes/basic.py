import os
import sys

args = sys.argv[1:]
source_path = args[0]

if not source_path:
    raise ValueError("No source file given")
if not os.path.isfile(source_path):
    raise ValueError(f"No file found at {source_path}")

with open(source_path, 'r') as file:
    rows = list(map(lambda line: list(line.strip()), file.readlines()))

empty_line = rows.index([])
warehouse = rows[:empty_line]

DIRECTIONS = {
    'v': (1, 0),
    '^': (-1, 0),
    '>': (0, 1),
    '<': (0, -1)
}

moves = []
for row in rows[empty_line + 1:]:
    for char in row:
        moves.append(DIRECTIONS[char])


def move(position: tuple[int, int], direction: tuple[int, int]) -> tuple[int, int]:
    x, y = position
    u, v = direction

    xf, yf = (x+u, y+v)
    if warehouse[xf][yf] == '#':
        return None

    if warehouse[xf][yf] == 'O' and not move((xf, yf), direction):
        return None

    warehouse[xf][yf], warehouse[x][y] = (warehouse[x][y], warehouse[xf][yf])
    return (xf, yf)


def find_robot() -> tuple[int, int]:
    for (i, row) in enumerate(warehouse):
        for (j, char) in enumerate(row):
            if char == '@':
                return (i, j)
    raise ValueError


def print_warehouse() -> None:
    for row in warehouse:
        print(''.join(row))


robot = find_robot()
for direction in moves:
    new_position = move(robot, direction)
    if new_position:
        robot = new_position

coordinates = 0
for (i, row) in enumerate(warehouse):
    for (j, char) in enumerate(row):
        if char == 'O':
            coordinates += 100*i + j

print(coordinates)
