content = open("03.txt").read()

def score(letter):
    if letter.isupper():
       return ord(letter) - ord('A') + 27
    else:
       return ord(letter) - ord('a') + 1

total_score = 0
lines = iter(content.splitlines())
while True:
    elf1, elf2, elf3 = next(lines, None), next(lines, None), next(lines, None)
    if elf1 is None:
        break

    common = (set(elf1) & set(elf2) & set(elf3)).pop()
    total_score += score(common)
print(total_score)

assert score('r') == 18
assert score('Z') == 52
