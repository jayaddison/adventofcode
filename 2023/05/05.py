from collections import defaultdict

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
    mappings[prev] = mappings.get(prev, {})
    mappings[prev][current] = mappings[prev].get(current, defaultdict(list))
    mappings[prev][current][(source_start, source_start + range_length)] = destination_start


# Evaluate the result for each seed
min_result = None
for seed in seeds:
    prev = "seed"
    for current in path:
        for (range_from, range_to), destination_start in mappings[prev][current].items():
            if range_from <= seed <= range_to:
                offset = seed - range_from
                seed = destination_start + offset
                break
        prev = current
    min_result = min(seed, min_result or seed)
print(min_result)
