content = open("04.txt").read()

def sections(assignment):
    first_section, last_section = assignment.split("-")
    return set(section for section in range(int(first_section), int(last_section) + 1))

fully_contained_count = 0
for line in content.splitlines():
    assignment_one, assignment_two = line.split(",")
    sections_one, sections_two = sections(assignment_one), sections(assignment_two)
    fully_contained_count += bool(sections_one & sections_two)

print(fully_contained_count)
