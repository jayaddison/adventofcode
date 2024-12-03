import sys

rows = []
for line in sys.stdin.read().splitlines():
    levels = list(map(int, line.split()))
    rows.append(levels)

status = []
for row in rows:
    diffs, directions = set(), set()
    prev, direction = None, None
    for level in row:
        if prev:
            diffs.add(abs(prev - level))
            directions.add(1 if level > prev else -1)
        prev = level
    
    safe = len(directions) == 1 and all(1 <= diff <= 3 for diff in diffs)
    status.append(safe)

print(sum(status))
