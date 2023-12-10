content = open("01.txt").read().splitlines()

NUMBERS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

total = 0
for line in content:
    numbers = []
    while line:
        if line[0].isdigit():
            numbers.append(line[0])
        else:
            for word, number in NUMBERS.items():
                if line.startswith(word):
                    numbers.append(number)
        line = line[1:]
    value = f"{numbers[0]}{numbers[-1]}"
    total += int(value)
print(total)
