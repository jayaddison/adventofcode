from math import ceil, floor

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor


class Snailfish:

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __add__(self, value):
        return Snailfish(left=self, right=value).reduce()

    def __len__(self):
        left_value = self.left if type(self.left) == int else len(self.left)
        right_value = self.right if type(self.right) == int else len(self.right)
        return left_value * 3 + right_value * 2

    def reduce(self):
        while True:
            if self.explode():
                continue
            if self.split():
                continue
            break
        return self

    def _walk_tree(self):
        stack = [(self, 1)]
        while stack:
            current_node, depth = stack.pop()
            yield current_node, depth
            if isinstance(current_node.right, Snailfish):
                stack.append((current_node.right, depth + 1))
            if isinstance(current_node.left, Snailfish):
                stack.append((current_node.left, depth + 1))

    def explode(self):
        modified = False
        previous_number_node = None
        carry_number = 0

        for current_node, depth in self._walk_tree():

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
                    if type(current_node.right) == int:
                        current_node.right += explode.right
                    else:
                        current_node.right.left += explode.right

                    if previous_number_node:
                        if not isinstance(previous_number_node.right, Snailfish):
                            previous_number_node.right += explode.left
                        elif not isinstance(previous_number_node.left, Snailfish):
                            previous_number_node.left += explode.left

                elif current_node.right == explode:
                    current_node.left += explode.left
                    current_node.right = 0
                    carry_number = explode.right

        if carry_number and not isinstance(self.right, Snailfish):
            self.right += carry_number
            carry_number = 0

        return modified

    def split(self):

        for current_node, _ in self._walk_tree():

            if type(current_node.left) == int and current_node.left >= 10:
                current_node.left = Snailfish(
                    left=floor(current_node.left / 2),
                    right=ceil(current_node.left / 2),
                )
                return True

            if type(current_node.right) == int and current_node.right >= 10:
                current_node.right = Snailfish(
                    left=floor(current_node.right / 2),
                    right=ceil(current_node.right / 2),
                )
                return True

        return False

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


# Test parsing
for test_input, expected_output in [
    ("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"),
    ("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"),
    ("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"),
    ("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"),
    ("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"),
    ("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]", "[[[[0,7],4],[7,[[8,4],9]]],[1,1]]"),
]:
    test_snailfish = SnailfishParser(test_input).process()
    test_snailfish.explode()

    if (str(test_snailfish) != expected_output):
        print(f"parse in: {test_input}")
        print(f"parse ex: {expected_output}")
        print(f"parse ac: {test_snailfish}")
        print()

# Test sums

for test_lhs, test_rhs, expected_output in [
    ("[[[[1,1],[2,2]],[3,3]],[4,4]]", "[5,5]", "[[[[3,0],[5,3]],[4,4]],[5,5]]"),
    ("[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]", "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]", "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]"),
    ("[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]", "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]", "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]"),
    ("[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]", "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]", "[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]"),
    ("[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]", "[7,[5,[[3,8],[1,4]]]]", "[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]"),
    ("[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]", "[[2,[2,2]],[8,[8,1]]]", "[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]"),
    ("[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]", "[2,9]", "[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]"),
]:
    test_sum = SnailfishParser(test_lhs).process() + SnailfishParser(test_rhs).process()

    if (str(test_sum) != expected_output):
        print(f"sum in: {test_lhs + test_rhs}")
        print(f"sum ex: {expected_output}")
        print(f"sum ac: {test_sum}")
        print()

# Test magnitudes

for test_input, expected_output in [
    ("[[1,2],[[3,4],5]]", 143),
    ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
    ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
    ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
    ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
    ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488),
]:
    test_magnitude = len(SnailfishParser(test_input).process())

    if (test_magnitude != expected_output):
        print(f"mag in: {test_input}")
        print(f"mag ex: {expected_output}")
        print(f"mag ac: {test_magnitude}")
        print()
