leanings = {"0": set(), "1": set()}
for line in open("03.txt").readlines():
    line = line.strip()
    leanings["0"].add(line)
    leanings["1"].add(line)

def categorize(bit_string_subset, index, leaning):
    count = sum(bit_string[index] == "1" for bit_string in bit_string_subset)
    total = len(bit_string_subset)

    if count * 2 == total:
        return leaning
    fallback = "1" if leaning == "0" else "0"
    return leaning if count > total / 2 else fallback

def filter_strings_by_prefix(bit_strings, prefix):
    results = set()
    for bit_string in bit_strings:
        if bit_string.startswith(prefix):
            results.add(bit_string)
    return results

for leaning in leanings.keys():
    prefix = str()
    while len(leanings[leaning]) > 1:
        prefix += categorize(leanings[leaning], len(prefix), leaning)
        leanings[leaning] = filter_strings_by_prefix(leanings[leaning], prefix)

print(leanings)
print(int(leanings['0'].pop(), 2) * int(leanings['1'].pop(), 2))
