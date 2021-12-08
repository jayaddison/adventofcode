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

unique_digit_wirings = {
    1: set("cf"),
    4: set("bcdf"),
    7: set("acf"),
    8: set("abcdefg"),
}

def candidate_digits(input):
    return set([
        digit for digit, count in digit_segment_counts.items() 
        if count == len(input)
    ])


sum = 0
content = open("08.txt").read()
for line in content.split("\n"):
    line = line.strip()
    if not line:
        continue
    signals, display = line.split("|", 1)
    signals, display = signals.strip(), display.strip()

    known_charsets = {}
    for item in signals.split(" "):
        possible_digits = candidate_digits(item)
        if len(possible_digits) == 1:
            digit = possible_digits.pop()
            known_charsets[digit] = set(item)

    for item in signals.split(" "):
        chars = set(item)
        if len(chars) == 6:
            if not known_charsets[7].issubset(chars):
                known_charsets[6] = chars
            elif known_charsets[4].issubset(chars):
                known_charsets[9] = chars
            else:
                known_charsets[0] = chars

    for item in signals.split(" "):
        chars = set(item)
        if len(chars) == 5:
            if known_charsets[7].issubset(chars):
                known_charsets[3] = chars
            elif chars.issubset(known_charsets[9]):
                known_charsets[5] = chars
            else:
                known_charsets[2] = chars

    result = ""
    charsets_to_digits = {"".join(sorted(chars)): digit for digit, chars in known_charsets.items()}
    for item in display.split(" "):
        key = "".join(sorted(set(item)))
        digit = charsets_to_digits[key]
        result += str(digit)
    sum += int(result)

print(sum)
