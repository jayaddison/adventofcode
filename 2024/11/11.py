import sys

state = list(map(int, sys.stdin.read().split()))

def transform(n):
    strval = str(n)
    if strval == '0':
        yield 1
    elif len(strval) % 2 == 0:
        midpt = int(len(strval) / 2)
        left, right = strval[:midpt], strval[midpt:]
        yield int(left)
        if right:
            yield int(right)
    else:
        yield n * 2024

print(state)
for _ in range(25):
    state = [output for item in state for output in transform(item)]
print(len(state))
