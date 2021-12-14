from collections import defaultdict

content = open("14.txt").read()

rule_map = {}

chain, rules = content.split("\n\n")
for line in rules.split("\n"):
    line = line.strip()
    if not line:
        continue
    match, insertion = line.split(" -> ")
    rule_map[match] = insertion

counts = defaultdict(lambda: 0)

def populate_counts(chain):
    for n in range(len(chain) - 1):
        left, right = chain[n], chain[n+1]
        counts[f"{left}{right}"] += 1

def apply_rules():
    pair_counts = defaultdict(lambda: 0)
    for pair, count in counts.items():
        left, right = pair
        middle = rule_map[pair]
        pair_counts[f"{left}{middle}"] += count
        pair_counts[f"{middle}{right}"] += count
    return pair_counts


def collect_char_counts():
    char_counts = defaultdict(lambda: 0)
    char_counts[chain[-1]] = 1
    for pair, count in counts.items():
        left, right = pair
        middle = rule_map[pair]
        char_counts[left] += count
        char_counts[middle] += count
    return char_counts


populate_counts(chain)
for step in range(40):
    char_counts = collect_char_counts()
    counts = apply_rules()

most_frequent, least_frequent = None, None
for char in char_counts:
    if most_frequent is None or char_counts[char] > char_counts[most_frequent]:
        most_frequent = char
    if least_frequent is None or char_counts[char] < char_counts[least_frequent]:
        least_frequent = char

print(char_counts[most_frequent] - char_counts[least_frequent])
