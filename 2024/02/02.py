import sys

rows = []
for line in sys.stdin.read().splitlines():
    levels = list(map(int, line.split()))
    rows.append(levels)

status = []
for row in rows:
    problem_encountered = False
    diffs, directions = set(), set()
    prev, direction = None, None
    for level in row:
        if prev:
            diff = abs(prev - level)
            direction = 1 if level > prev else -1
            if not 1 <= diff <= 3 or directions and direction not in directions:
                if not problem_encountered:
                    problem_encountered = True
                    continue
            diffs.add(diff)
            directions.add(direction)
        prev = level

    safe = len(directions) == 1 and all(1 <= diff <= 3 for diff in diffs)
    status.append(safe)

print(sum(status))
