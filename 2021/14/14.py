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

def apply_rules(chain):
    yield chain[0]
    for n in range(len(chain) - 1):
        left, right = chain[n], chain[n+1]
        middle = rule_map[chain[n:n+2]]
        yield f"{middle}{right}"

for step in range(10):
    chain = "".join(apply_rules(chain))

counts = defaultdict(lambda: 0)
for char in chain:
    counts[char] += 1

most_frequent, least_frequent = None, None
for char in counts:
    if most_frequent is None or counts[char] > counts[most_frequent]:
        most_frequent = char
    if least_frequent is None or counts[char] < counts[least_frequent]:
        least_frequent = char

print(f"{counts[most_frequent] - counts[least_frequent]}")
