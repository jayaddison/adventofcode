from collections import defaultdict
import sys

result = 0
dependencies = defaultdict(set)
for line in sys.stdin.read().splitlines():
    if not line.strip():
        continue
    elif '|' in line:
        required_page, page = list(map(int, line.split('|')))
        dependencies[page].add(required_page)
    else:
        satisfiable = True
        resolved = set()
        update = list(map(int, line.split(',')))
        relevant = set(update)
        for page in update:
            if page in dependencies:
                 if any(
                     dependency in relevant
                     and dependency not in resolved
                     for dependency in dependencies[page]
                 ):
                     satisfiable = False
                     break
            resolved.add(page)
        if satisfiable:
            midpoint = update[int(len(update) / 2)]
            result += midpoint
print(result)
