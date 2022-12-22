import formulas

room_mapping = {}
room_definitions = {}

content = open("21.txt").read()
for idx, line in enumerate(content.splitlines()):
    room_id = f"A{idx}"
    room_name, _, definition = line.partition(":")
    room_mapping[room_name] = room_id
    room_definitions[room_id] = definition.strip()


room_formulae = {}
for room_id, definition in room_definitions.items():
    if definition[0].isdigit():
        room_formulae[room_id] = definition
    else:
        formula = [room_mapping.get(value) or value for value in definition.split()]
        room_formulae[room_id] = "= " + " ".join(formula)


spreadsheet = formulas.ExcelModel().from_dict(room_formulae)
evaluated_spreadsheet = spreadsheet.calculate()
root_room_result = evaluated_spreadsheet[room_mapping["root"]]

print(root_room_result)
