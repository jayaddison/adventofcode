import formulas

room_mapping = {}
room_definitions = {}

content = open("21.txt").read()
for idx, line in enumerate(content.splitlines()):
    room_id = f"A{idx}"
    room_name, _, definition = line.partition(":")
    room_mapping[room_name] = room_id
    room_definitions[room_id] = definition.strip()


human_room, root_room = room_mapping["humn"], room_mapping["root"]
room_formulae = {}
for room_id, definition in room_definitions.items():
    if room_id == human_room:
        room_formulae[room_id] = 'NULL'
        continue
    if definition[0].isdigit():
        room_formulae[room_id] = definition
    elif room_id == root_room:
        formula = [room_mapping.get(value) or "=" for value in definition.split()]
        room_formulae[room_id] = "= " + " ".join(formula)
    else:
        formula = [room_mapping.get(value) or value for value in definition.split()]
        room_formulae[room_id] = "= " + " ".join(formula)

spreadsheet = formulas.ExcelModel().from_dict(room_formulae)
evaluated_spreadsheet = spreadsheet.calculate()
root_room_result = evaluated_spreadsheet[room_mapping["root"]]


inverted_formulae = room_formulae.copy()

def invert_definition(room_id, reference=None):
    definition = inverted_formulae[room_id]
    if not definition.startswith("="):
        return

    formula = definition.split()[1:]
    left_operand, operator, right_operand = formula
    left_value, right_value = (
        evaluated_spreadsheet[left_operand].value[0][0],
        evaluated_spreadsheet[right_operand].value[0][0],
    )
    left_value, right_value = (
        None if left_value == formulas.VALUE else left_value,
        None if right_value == formulas.VALUE else right_value,
    )

    if room_id == root_room:
        assert reference is None
        assert operator == "="
        inverted_formulae[room_id] = str(left_value or right_value)
    else:
        inverted_formula = None
        match left_value, operator:
            case None, "+":
                inverted_formula = f"{reference} - {right_operand}"
            case _, "+":
                inverted_formula = f"{right_operand} - {reference}"
            case None, "-":
                inverted_formula = f"{reference} + {right_operand}"
            case _, "-":
                inverted_formula = f"{right_operand} + {reference}"
            case None, "*":
                inverted_formula = f"{reference} / {right_operand}"
            case _, "*":
                inverted_formula = f"{right_operand} / {reference}"
            case None, "/":
                inverted_formula = f"{reference} * {right_operand}"
            case _, "/":
                inverted_formula = f"{right_operand} * {reference}"
        inverted_formulae[room_id] = f"={inverted_formula}"

    if left_value is None:
        invert_definition(left_operand, room_id)
    if right_value is None:
        invert_definition(right_operand, room_id)


invert_definition(root_room)

print(room_formulae)
print(inverted_formulae)
spreadsheet = formulas.ExcelModel().from_dict(inverted_formulae)
evaluated_spreadsheet = spreadsheet.calculate()

print(evaluated_spreadsheet)
