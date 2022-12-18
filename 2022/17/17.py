rocks = [
    horizonta := [[True] * 4],
    plus_sign := [[False, True, False], [True, True, True], [False, True, False]],
    corner_pc := [[False, False, True], [False, False, True], [True, True, True]],
    verticala := [[True]] * 4,
    chunky_pc := [[True, True] * 2],
]

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.occupied = [[False] * width] * height
        self.action = None
        self.descending = None

    def handle_keypress(self, keypress):
        match keypress:
            case "<":
                self.action = LEFT
            case ">":
                self.action = RIGHT

    def perform_actions(self):
        self.action = None

    def update_simulation(self):
        pass

    def tick(self):
        self.perform_actions()
        self.update_simulation()


board = Board(width=7, height=4)
board.tick()
