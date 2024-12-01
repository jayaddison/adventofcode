import sys

lefts, rights = [], []
for line in sys.stdin.read().splitlines():
    left, right = map(int, line.split())
    lefts.append(left)
    rights.append(right)

total_difference = 0
lefts_sorted, rights_sorted = sorted(lefts), sorted(rights)
for left, right in zip(lefts_sorted, rights_sorted):
    difference = abs(left - right)
    total_difference += difference

print(total_difference)
