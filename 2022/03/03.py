content = open("03.txt").read()

def score(letter):
    if letter.isupper():
       return ord(letter) - ord('A') + 27
    else:
       return ord(letter) - ord('a') + 1

total_score = 0
for line in content.splitlines():
    halfway = int(len(line) / 2)
    first, second = line[:halfway], line[halfway:]
    common = (set(first) & set(second)).pop()
    total_score += score(common)
print(total_score)

assert score('p') == 16
assert score('P') == 42
