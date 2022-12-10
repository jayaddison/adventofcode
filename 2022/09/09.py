content = open("09.txt").read()


positions = {n: (0, 0) for n in range(10)}

tail_visited = set()
tail_visited.add(positions[9])

def move_head(x_step, y_step):
    global positions
    x, y = positions[0]
    positions[0] = (x + x_step, y + y_step)

def update_pair(head, tail):
    global positions
    head_x, head_y = positions[head]
    tail_x, tail_y = positions[tail]
    horizontal_distance = abs(head_x - tail_x)
    vertical_distance = abs(head_y - tail_y)
    if horizontal_distance > 1 or vertical_distance > 1:
        dist_x = (head_x - tail_x)
        dist_y = (head_y - tail_y)
        if dist_x:
            tail_x += dist_x / abs(dist_x)
        if dist_y:
            tail_y += dist_y / abs(dist_y)
        tail_position = tail_x, tail_y
        if tail == 9:
            tail_visited.add(tail_position)
        positions[tail] = tail_position

for line in content.splitlines():
    match line.split():
        case "L", count:
            x_step, y_step = -1, 0
        case "R", count:
            x_step, y_step = 1, 0
        case "U", count:
            x_step, y_step = 0, 1
        case "D", count:
            x_step, y_step = 0, -1

    for _ in range(int(count)):
        move_head(x_step, y_step)
        for n in range(1, 10):
            update_pair(n - 1, n)

print(len(tail_visited))
