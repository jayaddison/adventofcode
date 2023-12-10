content = open("04.txt").read()

cards, card_tallies = {}, {}
for line in content.splitlines():
    card, _, numbers = line.partition(": ")
    card_id = int(card.replace("Card ", ""))
    winning_numbers, _, found_numbers = numbers.partition(" | ")
    winning_numbers = set(filter(None, winning_numbers.split(" ")))
    found_numbers = set(filter(None, found_numbers.split(" ")))
    cards[card_id] = (winning_numbers, found_numbers)
    card_tallies[card_id] = 1

for card_id, card in cards.items():
    winning_numbers, found_numbers = card
    matched = len(winning_numbers & found_numbers)
    if matched:
        for winning_card_id in range(card_id + 1, card_id + matched + 1):
            card_tallies[winning_card_id] += card_tallies[card_id]

print(sum(card_tallies.values()))
