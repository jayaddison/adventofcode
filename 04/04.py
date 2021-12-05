f = open("04.txt").read()
lines = f.split("\n")

draw_line, board_lines = lines[0], lines[1:-1]
assert len(board_lines) % 6 == 0

class Board:

    def __init__(self, board_lines):
        self.bingo = False
        self.grid = []
        self.remaining = set()
        self.coordinates = {}
        self.x_hits = [0] * 5
        self.y_hits = [0] * 5
        for y, line in enumerate(board_lines):
            row = [int(n) for n in line.split(" ") if n]
            self.grid.append(row)
            self.remaining.update(set(row))
        for y, row in enumerate(self.grid):
            for x, value in enumerate(row):
                self.coordinates[value] = (x, y)

    def draw(self, value):
        if value not in self.remaining:
            return
        (x, y) = self.coordinates[value]
        self.x_hits[x] += 1
        self.y_hits[y] += 1
        self.bingo = self.bingo or self.x_hits[x] == 5 or self.y_hits[y] == 5
        self.remaining.remove(value)

    def has_won(self):
        return self.bingo

    def product(self):
        return sum(self.remaining)

draw_numbers = [int(x) for x in draw_line.split(",")]
boards = []
while board_lines:
    boards.append(Board(board_lines[1:6]))
    board_lines = board_lines[6:]

for number in draw_numbers:
    for board_idx, board in enumerate(boards):
        board.draw(number)
        if board.has_won():
            print(f"Board {board_idx} wins with score: {number * board.product()}")
            break
    if board.has_won():
        break
