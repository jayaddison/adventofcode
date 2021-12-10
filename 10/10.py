content = open("10.txt").read()

OPENINGS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

CLOSINGS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

score = 0
for line in content.split("\n"):
    stack = []
    for char in line:
        if stack and char in CLOSINGS:
            expected = stack[-1]
            if stack[-1] == char:   
                stack.pop()
            else:
                score += CLOSINGS[char]
                break
        if char in OPENINGS:
            stack.append(OPENINGS[char])

print(score)
