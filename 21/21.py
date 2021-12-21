from abc import ABC, abstractmethod


class Die(ABC):
    @abstractmethod
    def roll(self):
        pass


class DeterministicDie(Die):
    def __init__(self):
        self.roll_count = 0

    def roll(self):
        result = (self.roll_count % 100) + 1
        self.roll_count += 1
        return result


class Player:
    def __init__(self, name, pos, die=None):
        if die is None:
            die = DeterministicDie()
        self.name = name.strip()
        self.pos = pos
        self.die = die
        self.score = 0

    def __str__(self):
        return self.name

    def play(self):
        a, b, c, = (
            self.die.roll(),
            self.die.roll(),
            self.die.roll(),
        )
        advance = sum([a, b, c])
        self.pos = self.pos + advance
        while self.pos > 10:
            self.pos -= 10
        self.score += self.pos
        print(f"{self} rolls {a}+{b}+{c} and moves to space {self.pos} for a total score of {self.score}")

    @property
    def has_won(self):
        return self.score >= 1000


content = open("21.txt").read()

die = DeterministicDie()
players = []
for line in content.split("\n"):
    line = line.strip()
    if not line:
        continue
    preamble, pos = line.split(":")
    player_name, _ = preamble.split("starting position")
    players.append(Player(player_name, int(pos), die))

game_over = False
prev_player = None
while not game_over:
    for player in players:
        if prev_player and prev_player.has_won:
            game_over = True
            losing_score = player.score
            dice = set([player.die for player in players])
            total_roll_count = sum([die.roll_count for die in dice])
            print(f"Player: {prev_player} won")
            print(f"Result: {losing_score} ({player}) x {total_roll_count} = {losing_score * total_roll_count}")
            break
        player.play()
        prev_player = player
