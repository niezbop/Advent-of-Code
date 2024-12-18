import os
import sys

Vector2 = tuple[int, int]
State = list[list[str]]

args = sys.argv[1:]
source_path = args[0]

if not source_path:
    raise ValueError("No source file given")
if not os.path.isfile(source_path):
    raise ValueError(f"No file found at {source_path}")

with open(source_path, 'r') as file:
    rows = list(map(lambda line: list(line.strip()), file.readlines()))

empty_line = rows.index([])


def print_warehouse() -> None:
    for row in warehouse:
        print(''.join(row))


WIDER = {
    '#': ['#', '#'],
    'O': ['[', ']'],
    '.': ['.', '.'],
    '@': ['@', '.']
}
warehouse = []
for row in rows[:empty_line]:
    new_row = []
    for char in row:
        new_row += WIDER[char]
    warehouse.append(new_row)

print_warehouse()

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


def copy_state(state: State) -> State:
    new_state = []
    for row in state:
        new_state.append(row.copy())
    return new_state


def override_state(state: State, override: State) -> None:
    for (i, row) in enumerate(override):
        for (j, char) in enumerate(row):
            state[i][j] = char


def move_crate(
        direction: Vector2,
        state: State,
        left: Vector2 = None,
        right: Vector2 = None) -> State:
    if left is None and right is None:
        raise ValueError
    if left is None:
        left = (right[0], right[1] - 1)
    if right is None:
        right = (left[0], left[1] + 1)

    xl, yl = left
    xr, yr = right
    u, v = direction
    xlf, ylf = (xl+u, yl+v)
    xrf, yrf = (xr+u, yr+v)

    if state[xlf][ylf] == '#' or state[xrf][yrf] == '#':
        return None

    if direction == (0, -1):
        if state[xlf][ylf] == ']' and not move_crate(direction, state, right=(xlf, ylf)):
            return None
        state[xlf][ylf], state[xl][yl], state[xr][yr] = (
            '[', ']', '.')
        return state
    elif direction == (0, 1):
        if state[xrf][yrf] == '[' and not move_crate(direction, state, left=(xrf, yrf)):
            return None
        state[xl][yl], state[xr][yr], state[xrf][yrf] = (
            '.', '[', ']')
        return state
    else:
        match (state[xlf][ylf], state[xrf][yrf]):
            case ('[', ']'):
                if not move_crate(direction, state, left=(xlf, ylf), right=(xrf, yrf)):
                    return None
            case (']', '.'):
                if not move_crate(direction, state, right=(xlf, ylf)):
                    return None
            case ('.', '['):
                if not move_crate(direction, state, left=(xrf, yrf)):
                    return None
            case (']', '['):
                temp = copy_state(state)
                moved_left = move_crate(direction, temp, right=(xlf, ylf))
                moved_right = move_crate(direction, temp, left=(xrf, yrf))
                if moved_left and moved_right:
                    override_state(state, temp)
                else:
                    return None
            case _:
                pass

        state[xl][yl], state[xr][yr], state[xlf][ylf], state[xrf][yrf] = (
            state[xlf][ylf], state[xrf][yrf], state[xl][yl], state[xr][yr])
        return state


def move(position: Vector2, direction: Vector2) -> Vector2:
    x, y = position
    u, v = direction

    xf, yf = (x+u, y+v)
    if warehouse[xf][yf] == '#':
        return None

    if warehouse[xf][yf] == '[' and not move_crate(direction, warehouse, left=(xf, yf)):
        return None

    if warehouse[xf][yf] == ']' and not move_crate(direction, warehouse, right=(xf, yf)):
        return None

    warehouse[xf][yf], warehouse[x][y] = (warehouse[x][y], warehouse[xf][yf])
    return (xf, yf)


def find_robot() -> Vector2:
    for (i, row) in enumerate(warehouse):
        for (j, char) in enumerate(row):
            if char == '@':
                return (i, j)
    raise ValueError


robot = find_robot()
for direction in moves:
    new_position = move(robot, direction)
    if new_position:
        robot = new_position

print_warehouse()

coordinates = 0
for (i, row) in enumerate(warehouse):
    for (j, char) in enumerate(row):
        if char == '[':
            coordinates += 100 * i + j
        # reverse_j = len(row) - 1 - j
        # if char == '[' and j <= reverse_j:
        #     coordinates += 100*i + j
        # if char == ']' and j >= reverse_j:
        #     coordinates += 100*i + reverse_j

print(coordinates)
