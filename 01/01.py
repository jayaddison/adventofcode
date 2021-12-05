content = open('01.txt').read()
previous, count = None, 0
for line in content.split():
    current = int(line)
    count += previous is not None and current > previous
    previous = current
print(count)
