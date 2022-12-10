content = open("09.txt").read()


head_position = (0, 0)
tail_position = (0, 0)

def move_head(x_step, y_step):
    global head_position
    x, y = head_position
    head_position = (x + x_step, y + y_step)

def update_tail():
    global head_position
    global tail_position
    head_x, head_y = head_position
    tail_x, tail_y = tail_position
    horizontal_distance = abs(head_x - tail_x)
    vertical_distance = abs(head_y - tail_y)
    if horizontal_distance > 1 or vertical_distance > 1:
        tail_x += (head_x - tail_x) / 2
        tail_y += (head_y - tail_y) / 2
        tail_position = tail_x, tail_y

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
        update_tail()
        
        for j in range(0, 10):
            for i in range(0, 10):
                sign = "."
                sign = "T" if tail_position == (i, j) else sign
                sign = "H" if head_position == (i, j) else sign
                print(sign , end="")
            print()
        print()