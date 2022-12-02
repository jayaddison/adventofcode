content = open("02.txt").read()

SHAPES = {
    'A': 'rock',
    'B': 'paper',
    'C': 'scissors',
}

OUTCOMES = {
    'X': 0,
    'Y': 3,
    'Z': 6,
}

SHAPE_SCORES = {
    'rock': 1,
    'paper': 2,
    'scissors': 3,
}


def score(a, b):
    a, b = a, SHAPES[b]
    if a == 'rock' and b == 'scissors':
        outcome = 6
    elif a == 'paper' and b == 'rock':
        outcome = 6
    elif a == 'scissors' and b == 'paper':
        outcome = 6
    elif a == b:
        outcome = 3
    else:
        outcome = 0
    return SHAPE_SCORES[a] + outcome


def determine_choice(a, b):
    a, b = OUTCOMES[a], SHAPES[b]
    if a == 3:
        return b
    elif b == 'scissors':
        return 'rock' if a else 'paper'
    elif b == 'paper':
        return 'scissors' if a else 'rock'
    elif b == 'rock':
        return 'paper' if a else 'scissors'


total_score = 0
for line in content.splitlines():
    opponent_choice, required_outcome = line.split()
    responding_choice = determine_choice(required_outcome, opponent_choice)
    total_score += score(responding_choice, opponent_choice)
print(total_score)
