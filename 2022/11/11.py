from collections import Counter

content = open("11.txt").read().splitlines()


class Department:
    def __init__(self, items, operation, test, destination_true, destination_false):
        self.items = items
        self.operation = operation
        self.test = test
        match test.split():
            case "divisible", "by", value:
                self.test_operation = "divide"
                self.test_operand = int(value)
        self.destinations = {True: destination_true, False: destination_false}

    def __str__(self):
        return f"items: {self.items}"

    @property
    def holding_items(self):
        return bool(self.items)

    def inspect_item(self):
        global prime_multiple
        item = self.items.pop(0)

        # apply operation to worry level
        parse_value = lambda x: item if x == "old" else int(x)
        match self.operation.split():
            case "*", value:
                item *= parse_value(value)
            case "+", value:
                item += parse_value(value)

        # test result of operation
        result = None
        if self.test_operation == "divide":
            result = item % self.test_operand == 0

        # append (throw) item to department at relevant destination
        departments[self.destinations[result]].items.append(item % prime_multiple)


def parse_segment(segment):
    department_id, items, operation, test, destination_true, destination_false = segment[:6]
    department_id = int(department_id[11:-1])
    items = [int(item) for item in items[18:].split(", ")]
    operation = operation[23:]
    test = test[8:]
    destination_true = int(destination_true[33:])
    destination_false = int(destination_false[34:])
    return department_id, Department(items, operation, test, destination_true, destination_false)


departments = {}
while segment := content[:7]:
    department_id, department = parse_segment(segment)
    departments[department_id] = department
    content = content[7:]

prime_multiple = 1
for department in departments.values():
    if department.test_operation == "divide":
        prime_multiple *= department.test_operand


department_activity = Counter()
for cycle in range(10000):
    for department_id, department in departments.items():
        while department.holding_items:
            department.inspect_item()
            department_activity[department_id] += 1

    for department in departments.values():
        print(department)
    print()

top_business_departments = department_activity.most_common(2)
top_department, second_department = top_business_departments
print(top_department[1] * second_department[1])

test_segment = (
    "Department 0:\n"
    "  Starting items: 79, 98\n"
    "  Operation: new = old * 19\n"
    "  Test: divisible by 23\n"
    "    If true: throw to department 2\n"
    "    If false: throw to department 3"
).splitlines()

parsed_segment = parse_segment(test_segment)
department_id, department = parsed_segment
assert (department_id, department.items, department.operation, department.test, department.destinations) == (
    0,
    [79, 98],
    "* 19",
    "divisible by 23",
    {True: 2, False: 3}
), parsed_segment
