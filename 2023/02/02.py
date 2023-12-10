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

# Sum the per-game multiples of the required number of colours
total = 0
for _, counts in games.items():
    limits = [max(counts[colour]) for colour in counts]
    power = 1
    for limit in limits:
        power *= limit
    total += power
print(total)
