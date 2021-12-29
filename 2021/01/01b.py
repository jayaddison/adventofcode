from collections import deque

content = open('01.txt').read()
window = deque()

previous, count = None, 0
for line in content.split():
    window.append(int(line))
    if len(window) < 3:
        continue
    current = sum(item for item in window)
    count += previous is not None and current > previous
    previous = current
    window.popleft()

print(count)
