from collections import defaultdict
import sys

UP, RIGHT, DOWN, LEFT = [(-1, 0), (0, 1), (1, 0), (0, -1)]

height, width, obstacles, loop_obstacles = 0, 0, {}, {}
guard_position, guard_direction, guard_path = None, None, defaultdict(set)

def print_map():
    for idy in range(height + 1):
        for idx in range(width + 1):
            if (idy, idx) in loop_obstacles:
                print('!', end='')
            elif (idy, idx) in obstacles:
                print('#', end='')
            elif (idy, idx) in guard_path:
                print('X', end='')
            elif (idy, idx) == guard_position:
                print('@', end='')
            else:
                print('.', end='')
        print('')
    print('')

def rotate(input_direction):
    if input_direction == UP: return RIGHT
    elif input_direction == RIGHT: return DOWN
    elif input_direction == DOWN: return LEFT
    elif input_direction == LEFT: return UP

for idy, row in enumerate(sys.stdin.read().splitlines()):
    height = max(height, idy)
    for idx, char in enumerate(row):
        width = max(width, idx)
        if char == '.':
            pass
        elif char == '#':
            obstacles[(idy, idx)] = True
        elif guard_direction := {"^": UP, ">": RIGHT, "v": DOWN, "<": LEFT}.get(char):
            guard_position = (idy, idx)

print(guard_position)
print(guard_direction)

def would_loop(hypothetical_position, hypothetical_direction):
    hypothetical_y, hypothetical_x = hypothetical_position
    move_y, move_x = hypothetical_direction

    while 0 <= hypothetical_y <= height and 0 <= hypothetical_x <= width:
        hypothetical_y += move_y
        hypothetical_x += move_x
        hypothetical_position = (hypothetical_y, hypothetical_x)

        if hypothetical_direction in guard_path.get(hypothetical_position, []):
            return True

    return False

guard_y, guard_x = guard_position
while 0 <= guard_y <= height and 0 <= guard_x <= width:
    guard_path[guard_position].add(guard_direction)
    move_y, move_x = guard_direction
    if (guard_y + move_y, guard_x + move_x) in obstacles:
        guard_direction = rotate(guard_direction)
        continue

    guard_y += move_y
    guard_x += move_x
    guard_position = (guard_y, guard_x)

    # hypothetical: would the guard revisit a previous location + direction if they rotated and continued from here?
    if would_loop(guard_position, rotate(guard_direction)):
        loop_obstacle_position = (guard_y + move_y, guard_x + move_x)
        loop_obstacles[loop_obstacle_position] = True

    print_map()

print(len(guard_path))
print(len(loop_obstacles))
