import sys

rows = []
for line in sys.stdin.read().splitlines():
    levels = list(map(int, line.split()))
    rows.append(levels)

status = []
for row in rows:
    problem_encountered = False
    diffs, directions = set(), list()
    prev, direction = None, None
    for level in row:
        if prev:
            diff = abs(prev - level)
            direction = 1 if level > prev else -1
            if not 1 <= diff <= 3 or directions and direction not in directions:
                if not problem_encountered:
                    # edge case: direction change due to problem level
                    if len(directions) == 1:
                        directions = [direction]
                    problem_encountered = True
                    continue
            diffs.add(diff)
            directions.append(direction)
        prev = level

    safe = len(set(directions)) == 1 and all(1 <= diff <= 3 for diff in diffs)
    print(f'{safe}: {row} ({problem_encountered})')
    status.append(safe)

print(sum(status))
