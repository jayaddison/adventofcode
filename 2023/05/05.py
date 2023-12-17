content = open("05.txt").read()

seeds = []
mappings = {}
current = None
path = ["soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]

# Construct datastructures for each path mapping
for line in content.splitlines():
    if current is None:
        _, _, seeds = line.partition(": ")
        seeds = [int(x) for x in seeds.split()]
        current = "seed"
        continue

    if not line.strip():
        continue

    if line.endswith(" map:"):
        prev, _, current = line[:-5].partition("-to-")
        continue

    destination_start, source_start, range_length = map(int, line.split())
    for x in range(range_length):
        mappings[prev] = mappings.get(prev, {})
        mappings[prev][current] = mappings[prev].get(current, {})
        mappings[prev][current][source_start + x] = destination_start + x


# Evaluate the result for each seed
min_result = None
for seed in seeds:
    prev = "seed"
    for current in path:
        seed = mappings[prev][current].get(seed, seed)
        prev = current
    min_result = min(seed, min_result or seed)
print(min_result)
