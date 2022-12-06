from collections import defaultdict

content = open("06.txt").read()

WINDOW_SIZE = 4

for line in content.splitlines():
    window = list(line[:WINDOW_SIZE])
    content = defaultdict(list)

    for char in window:
        content[char].append(char)

    for idx, fresh in enumerate(line[WINDOW_SIZE:], start=WINDOW_SIZE):
        window.append(fresh)
        content[fresh].append(fresh)

        stale = window.pop(0)
        assert stale in content
        if content[stale]:
            content[stale].pop()
        if not content[stale]:
            del content[stale]

        if len(content) == WINDOW_SIZE:
            print(f"Marker found at index {idx + 1}")
            break
