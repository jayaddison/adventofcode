from collections import defaultdict
import sys

result = 0
result_part_two = 0
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
        reordered, pending = [], set()
        relevant = set(update)
        for page in update:
            for deferred in list(pending):
                if all(dependency in relevant and dependency in resolved for dependency in dependencies[deferred]):
                    resolved.add(deferred)
                    reordered.append(deferred)
                    pending.remove(deferred)
            if any(dependency in relevant and dependency not in resolved for dependency in dependencies[page]):
                satisfiable = False
                pending.add(page)
            else:
                reordered.append(page)
            if page not in pending:
                resolved.add(page)
        if satisfiable:
            midpoint = update[int(len(update) / 2)]
            result += midpoint
        else:
            while len(pending):
                next_resolved = next(item for item in pending if all(dependency not in relevant or dependency in resolved for dependency in dependencies[item]))
                resolved.add(next_resolved)
                reordered.append(next_resolved)
                pending.remove(next_resolved)
            midpoint = reordered[int(len(reordered) / 2)]
            result_part_two += midpoint
print(result)
print(result_part_two)
