from math import ceil, floor

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor


class Snailfish:

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __add__(self, value):
        total = Snailfish(left=self, right=value)
        reducing = True
        while reducing := total.reduce():
            pass
        return total

    def reduce(self):
        stack = [(self, 1)]
        current_node = None
        previous_node = None

        modified = False
        previous_number_node = None
        carry_number = 0

        while stack:
            current_node, depth = stack.pop()

            if not isinstance(current_node.left, Snailfish):
                previous_number_node = current_node

            if carry_number and not isinstance(current_node.left, Snailfish):
                current_node.left += carry_number
                carry_number = 0

            if depth == 4 and not modified:
                explode = None
                if isinstance(current_node.left, Snailfish):
                    explode = current_node.left
                elif isinstance(current_node.right, Snailfish):
                    explode = current_node.right
                modified = explode is not None

                if current_node.left == explode:
                    current_node.left = 0
                    current_node.right = explode.left

                elif current_node.right == explode:
                    current_node.right = 0
                    previous_number_node.left += explode.left
                    carry_number = explode.right

            if isinstance(current_node.right, Snailfish):
                stack.append((current_node.right, depth + 1))
            if isinstance(current_node.left, Snailfish):
                stack.append((current_node.left, depth + 1))

            previous_node = current_node

        if carry_number and not isinstance(self.right, Snailfish):
            self.right += carry_number
            carry_number = 0

        return modified

    def __str__(self):
        return f"[{self.left},{self.right}]"


class SnailfishParser(NodeVisitor):

    grammar = Grammar(
        """
        snailfish = open_bracket left comma right close_bracket
    
        left = number
             / snailfish
    
        right = number
              / snailfish
    
        open_bracket = "["
        close_bracket = "]"
        comma = ","
        number = ~"[0-9]+"
        """
    )

    def __init__(self, text):
        self.tree = self.grammar.parse(text)

    def visit_snailfish(self, node, visited_children):
        _, left, _, right, _ = visited_children
        return Snailfish(left[0], right[0])

    def visit_number(self, node, visited_children):
        return int(node.text)

    def generic_visit(self, node, visited_children):
        return visited_children

    def process(self):
        return self.visit(self.tree)


# Test cases
for test_input, expected_output in [
    ("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"),
    ("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"),
    ("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"),
    ("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"),
    ("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"),
]:
    test_snailfish = SnailfishParser(test_input).process()
    test_snailfish.reduce()

    print(f"in: {test_input}")
    print(f"ac: {test_snailfish}")
    print(f"ex: {expected_output}")
    print()

    assert str(test_snailfish) == expected_output

content = open("18.txt").read().strip()

total = None
for line in content.split("\n"):
    parser = SnailfishParser(line)
    value = parser.process()
    total = value if total is None else total + value
print(total)
