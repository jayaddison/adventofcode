import sys

rows = []
for line in sys.stdin.read().splitlines():
    levels = list(map(int, line.split()))
    rows.append(levels)

def row_variants(row):
    yield row
    for i in range(len(row)):
        yield [level for idx, level in enumerate(row) if idx != i]

status = []
for row in rows:
    for row_variant in row_variants(row):
        diffs, directions = set(), set()
        prev, direction = None, None
        for level in row_variant:
            if prev:
                diffs.add(abs(prev - level))
                directions.add(1 if level > prev else -1)
            prev = level

        safe = len(directions) == 1 and all(1 <= diff <= 3 for diff in diffs)
        if safe:
            break
    status.append(safe)

print(sum(status))
