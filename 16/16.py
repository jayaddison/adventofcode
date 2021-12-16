content = open("16.txt").read().strip()

TYPE_LITERAL = 4

LENGTH_TYPE_FIXED = 0
LENGTH_TYPE_COUNT = 1

HEX_MAP = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}

def hextobitstring(text):
    return "".join(HEX_MAP[char] for char in text)

def number(bitstring):
    return int(bitstring, base=2)

def process_literal(payload):
    bitstring = []
    index = 0
    done = False
    while not done:
        done = payload[index] == "0"
        bitstring.append(payload[index + 1:index + 5])
        index += 5
    while index % 5 and payload[index] == "0":
        index += 1
    return index, number("".join(bitstring))

def process_operator(payload):
    length_type_id = number(payload[0])
    if length_type_id == LENGTH_TYPE_FIXED:
        length = number(payload[1:16]) + 16
        index = 16
        while index < length:
            consumed = process_packet(payload[index:])
            print(f"consumed fixed packet from index {index} length {consumed}; {length} remaining")
            index += consumed

    elif length_type_id == LENGTH_TYPE_COUNT:
        count = number(payload[1:12])
        index = 12
        while count:
            consumed = process_packet(payload[index:])
            print(f"consumed count packet length {consumed}; {count} remaining")
            index += consumed
            count -= 1
    else:
        print(f"unexpected: did nothing")

    return index

version_sum = 0

def process_packet(payload):
    version = number(payload[0:3])
    type_id = number(payload[3:6])
    payload = payload[6:]

    global version_sum
    version_sum += version

    index = 6
    if type_id == TYPE_LITERAL:
        print(f"consuming literal")
        consumed, value = process_literal(payload)
        print(f"consumed literal length {consumed}: value is {value}")
    else:
        print(f"consuming operator")
        consumed = process_operator(payload)
        print(f"consumed operator length {consumed}")
    return index + consumed

bitstring = hextobitstring(content)
print(f"bitstring is {bitstring}")

process_packet(bitstring)

print(f"version sum is {version_sum}")
