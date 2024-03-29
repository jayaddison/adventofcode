from functools import cmp_to_key

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor


class NestedIntegerListParser(NodeVisitor):

    grammar = Grammar(
        """
        nested_integer_list = integer_list

        integer_list = open_bracket items close_bracket

        items = item? (comma items)?

        item = integer_list
             / number

        open_bracket = "["
        close_bracket = "]"
        comma = ","
        number = ~"[0-9]+"
        """
    )

    def __init__(self, text):
        self.tree = self.grammar.parse(text)

    def visit_integer_list(self, node, visited_children):
        _, items, _ = visited_children
        return list(items)

    def visit_items(self, node, visited_children):
        head, tail = visited_children
        yield from head
        for subexpr in tail:
            for items in subexpr:
                yield from items

    def visit_item(self, node, visited_children):
        item, = visited_children
        return item

    def visit_number(self, node, visited_children):
        return int(node.text)

    def visit_comma(self, node, visited_children):
        yield from ()

    def generic_visit(self, node, visited_children):
        return visited_children

    def process(self):
        return self.visit(self.tree)


# Test parsing
for test_input, expected_output in [
    ("[[[[[9,8,3],1],2],3],4]", [[[[[9,8,3],1],2],3],4]),
    ("[7,[6,[5,[4,[3,2]]]]]", [7,[6,[5,[4,[3,2]]]]]),
    ("[[6,[5,[4,[3,2]]]],1]", [[6,[5,[4,[3,2]]]],1]),
    ("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]),
    ("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]),
    ("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]", [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]),
    ("[[[[14,13],[8,15]],[[12,5],[10,0]]],[[[11,[7,4]],7],1]]", [[[[14,13],[8,15]],[[12,5],[10,0]]],[[[11,[7,4]],7],1]]),
    ("[]", []),
]:
    test_nested_integer_list = NestedIntegerListParser(test_input).process()
    assert test_nested_integer_list == expected_output


def compare(left, right):
    match type(left).__name__, type(right).__name__:

        case 'int', 'int':
           if left < right:
               return True
           elif left > right:
               return False
           else:
               return None

        case 'list', 'list':
           left = iter(left)
           right = iter(right)
           while True:
               left_item = next(left, None)
               right_item = next(right, None)
               if left_item is None and right_item is None:
                   break
               if left_item is None:
                   return True
               if right_item is None:
                   return False
               comparison = compare(left_item, right_item)
               if comparison is None:
                   continue
               return comparison

        case 'int', _:
            return compare([left], right)

        case _, 'int':
            return compare(left, [right])


def sort_compare(left, right):
    comparison = compare(left, right)
    if comparison is True:
        return -1
    if comparison is False:
        return 1
    return 0


content = open("13.txt").read().splitlines()
lines = []
pairing, total = 1, 0
for line in content:
    if line:
        lines.append(NestedIntegerListParser(line).process())

dividers = [ [[2]], [[6]] ]
lines.extend(dividers)
lines = sorted(lines, key=cmp_to_key(sort_compare))
indices = [lines.index(divider) + 1 for divider in dividers]
print(indices)

assert compare(1, 2) == True  # left item is lower
assert compare(2, 1) == False
assert compare([1], [2]) == True  # lower integer first
assert compare([1, 2], [2]) == True  # left items exhausted; all lower than corresponding right items
assert compare([3, 2], [1]) == False
assert compare([1], [2, 3]) == True
assert compare([1, 2, 3, 4, 5], [1, 2, 5, 4, 5]) == True
