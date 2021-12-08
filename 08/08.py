digit_segment_counts = {
    0: 6,
    1: 2,
    2: 5,
    3: 5,
    4: 4,
    5: 5,
    6: 6,
    7: 3,
    8: 7,
    9: 6,
}

def candidate_digits(input):
    return set([
        digit for digit, count in digit_segment_counts.items() 
        if count == len(input)
    ])


known_digits = {}
unique_count = 0

content = open("08.txt").read()
for line in content.split("\n"):
    line = line.strip()
    if not line:
        continue
    signals, display = line.split("|", 1)
    signals, display = signals.strip(), display.strip()

    for item in display.split(" "):
        possible_digits = candidate_digits(item)
        if len(possible_digits) == 1:
            known_digits[item] = possible_digits.pop()
            unique_count += 1

print(unique_count)
