from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor


class NestedIntegerListParser(NodeVisitor):

    grammar = Grammar(
        """
        integer_list = open_bracket left comma right close_bracket

        left = number
             / integer_list

        right = number
              / integer_list

        open_bracket = "["
        close_bracket = "]"
        comma = ","
        number = ~"[0-9]+"
        """
    )

    def __init__(self, text):
        self.tree = self.grammar.parse(text)

    def visit_integer_list(self, node, visited_children):
        _, left, _, right, _ = visited_children
        return left + right

    def visit_number(self, node, visited_children):
        return int(node.text)

    def generic_visit(self, node, visited_children):
        return visited_children

    def process(self):
        return self.visit(self.tree)


# Test parsing
for test_input, expected_output in [
    ("[[[[[9,8],1],2],3],4]", [[[[[9,8],1],2],3],4]),
    ("[7,[6,[5,[4,[3,2]]]]]", [7,[6,[5,[4,[3,2]]]]]),
    ("[[6,[5,[4,[3,2]]]],1]", [[6,[5,[4,[3,2]]]],1]),
    ("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]),
    ("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]),
    ("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]", [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]),
    ("[[[[14,13],[8,15]],[[12,5],[10,0]]],[[[11,[7,4]],7],1]]", [[[[14,13],[8,15]],[[12,5],[10,0]]],[[[11,[7,4]],7],1]]),
]:
    test_nested_integer_list = NestedIntegerListParser(test_input).process()
    assert test_nested_integer_list == expected_output


def compare(left, right):
    match type(left).__name__, type(right).__name__:

        case 'int', 'int':
           return left < right

        case 'list', 'list':
           left = iter(left)
           right = iter(right)
           while True:
               left_item = next(left, None)
               right_item = next(right, None)
               if not right_item:
                   return True
               if not left_item:
                   return False
               if not compare(left_item, right_item):
                   return False

        case 'int', _:
            return compare([left], right)

        case _, 'int':
            return compare(left, [right])


assert compare(1, 2) == True  # left item is lower
assert compare(2, 1) == False
assert compare([1], [2]) == True  # lower integer first
assert compare([1, 2], [2]) == True  # left items exhausted; all lower than corresponding right items
assert compare([3, 2], [1]) == False
assert compare([1], [2, 3]) == False
