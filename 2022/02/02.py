content = open("02.txt").read()

SHAPES = {
    'A': 'rock',
    'B': 'paper',
    'C': 'scissors',
    'X': 'rock',
    'Y': 'paper',
    'Z': 'scissors',
}

SHAPE_SCORES = {
    'rock': 1,
    'paper': 2,
    'scissors': 3,
}


def score(a, b):
    shape = SHAPES[a]
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
    return SHAPE_SCORES[shape] + outcome


total_score = 0
for line in content.splitlines():
    opponent_choice, responding_choice = line.split()
    total_score += score(responding_choice, opponent_choice)
print(total_score)
