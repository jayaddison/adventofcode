from abc import ABC, abstractmethod
from copy import deepcopy
from itertools import product


class Die(ABC):
    @abstractmethod
    def roll(self):
        pass


class Player:
    def __init__(self, name, pos):
        self.name = name.strip()
        self.pos = pos
        self.score = 0

    def __str__(self):
        return self.name

    def play(self, a, b, c):
        advance = sum([a, b, c])
        self.pos = self.pos + advance
        while self.pos > 10:
            self.pos -= 10
        self.score += self.pos

    @property
    def has_won(self):
        return self.score >= 21


content = open("21.txt").read()

players = []
for line in content.split("\n"):
    line = line.strip()
    if not line:
        continue
    preamble, pos = line.split(":")
    player_name, _ = preamble.split("starting position")
    players.append(Player(player_name, int(pos)))
winning_paths = {player.name: [] for player in players}


def explore_paths(player, path):
    faces = [1, 2, 3]
    for a, b, c in product(faces, faces, faces):
        player_copy = deepcopy(player)
        player_copy.play(a, b, c)
        if player_copy.has_won:
            winning_path = path + [a, b, c]
            winning_paths[player.name].append(winning_path)
            print(f"{winning_path} is a winning path for {player}")
        else:
            explore_paths(player_copy, path + [a, b, c])

for player in players:
    explore_paths(player, [])
