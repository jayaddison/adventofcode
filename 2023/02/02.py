from collections import defaultdict

content = open("02.txt").read()

games = defaultdict(lambda: defaultdict(lambda: []))

# Record colour-counts from the observations within each game
for line in content.splitlines():
    game, _, description = line.partition(":")
    game_id = int(game.replace("Game ", ""))
    observations = description.strip().split(";")
    for observation in observations:
        measurements = observation.split(",")
        for measurement in measurements:
            count, colour = measurement.strip().split(" ")
            games[game_id][colour].append(int(count))

# Set acceptable thresholds
THRESHOLDS = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

# Filter acceptable games
total = 0
for game_id, counts in games.items():
    acceptable = all(max(counts[colour]) <= threshold for colour, threshold in THRESHOLDS.items())
    total += game_id if acceptable else 0
print(total)
