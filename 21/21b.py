from collections import defaultdict
from itertools import product


class Player:
    def __init__(self, name, pos):
        self.name = name.strip()
        self.pos = pos
        self.score = 0

    def __str__(self):
        return self.name

    def play(self, advance):
        self.pos = self.pos + advance
        while self.pos > 10:
            self.pos -= 10
        self.score += self.pos

    def play_path(self, path):
        for step in path:
            self.play(step)
            if self.has_won:
                return self

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
games_won = defaultdict(lambda: 0)


faces = [1, 2, 3]
outcome_counts = defaultdict(lambda: 0)
for a, b, c in product(faces, repeat=3):
    outcome = sum([a, b, c])
    outcome_counts[outcome] += 1
total_outcomes = sum(outcome_counts.values())
outcome_frequencies = {
    outcome: outcome_count / total_outcomes
    for outcome, outcome_count in outcome_counts.items()
}


def path_to_occurrences(path):
    outcome_frequency = 1.0
    for roll in path:
        roll_frequency = outcome_frequencies[roll]
        outcome_frequency *= roll_frequency
    possible_games = pow(3, len(path) * 3)
    return round(possible_games * outcome_frequency)


def explore_paths(players, path):
    for outcome in outcome_frequencies:
        evaluation_path = path + [outcome]
        winner = None
        for index, player in enumerate(players):
            simulated_player = Player(name=player.name, pos=player.pos)
            player_rolls = evaluation_path[index :: len(players)]
            winner = simulated_player.play_path(player_rolls)
            if winner:
                break
        if winner:
            games_won[player.name] += path_to_occurrences(evaluation_path)
        else:
            explore_paths(players, evaluation_path)


assert path_to_occurrences([3]) == 1
assert path_to_occurrences([6, 3]) == 7
assert path_to_occurrences([3, 6]) == 7

explore_paths(players, [])
print(games_won)
