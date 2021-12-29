content = open("10.txt").read()

OPENINGS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

CLOSINGS = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}

scores = []
for line in content.split("\n"):
    stack = []
    for char in line:
        if stack and char in CLOSINGS:
            expected = stack[-1]
            if stack[-1] == char:   
                stack.pop()
            else:
                stack = []
                break
        if char in OPENINGS:
            stack.append(OPENINGS[char])
    score = 0
    while stack:
        score *= 5
        score += CLOSINGS[stack.pop()]
    if score:
        scores.append(score)

scores = sorted(scores)
middle = scores[int(len(scores) / 2)]

print(middle)
