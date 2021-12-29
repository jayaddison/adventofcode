from itertools import permutations
from math import ceil, floor

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor


class Snailfish:
    def __init__(self, left=None, right=None, value=None):
        self.left = left
        self.right = right
        self.value = value
        self.prev = None
        self.next = None

    def __add__(self, value):
        return Snailfish(left=self, right=value).reduce()

    def __len__(self):
        if self.is_number_node:
            return self.value
        return len(self.left) * 3 + len(self.right) * 2

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

    @property
    def is_number_node(self):
        return self.value is not None

    def link_nodes(self):
        prev_number_node = None
        for node, _ in self._walk_tree():
            if not node.is_number_node:
                continue
            if prev_number_node:
                prev_number_node.next = node
            node.prev = prev_number_node
            prev_number_node = node

    def explode(self):
        self.link_nodes()
        for current_node, depth in self._walk_tree():
            if depth == 4:
                nested_nodes = [
                    node
                    for node in [current_node.left, current_node.right]
                    if node and not node.is_number_node
                ]
                if not nested_nodes:
                    continue

                leftmost_nested = nested_nodes[0]
                assert leftmost_nested.left.is_number_node
                assert leftmost_nested.right.is_number_node

                left, right = leftmost_nested.left, leftmost_nested.right
                if left.prev is not None:
                    left.prev.value += left.value
                if right.next is not None:
                    right.next.value += right.value

                if current_node.left == leftmost_nested:
                    current_node.left = Snailfish(value=0)
                elif current_node.right == leftmost_nested:
                    current_node.right = Snailfish(value=0)
                return True

        return False

    def split(self):
        for current_node, _ in self._walk_tree():
            if current_node.is_number_node and current_node.value >= 10:
                current_node.left = Snailfish(value=floor(current_node.value / 2))
                current_node.right = Snailfish(value=ceil(current_node.value / 2))
                current_node.value = None
                return True
        return False

    def __str__(self):
        return str(self.value) if self.is_number_node else f"[{self.left},{self.right}]"


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
        return Snailfish(left=left[0], right=right[0])

    def visit_number(self, node, visited_children):
        return Snailfish(value=int(node.text))

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
    ("[[[[14,13],[8,15]],[[12,5],[10,0]]],[[[11,[7,4]],7],1]]", "[[[[14,13],[8,15]],[[12,5],[10,0]]],[[[18,0],11],1]]"),
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
    ("[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]", "[1,[[[9,3],9],[[9,0],[0,7]]]]", "[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]"),
    ("[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]", "[[[5,[7,4]],7],1]", "[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]"),
    ("[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]", "[[[[4,2],2],6],[8,7]]", "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"),
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

content = open("18.txt").read().strip()

max_magnitude = 0
lines = content.split("\n")
for line_a, line_b in permutations(lines, 2):
    result = SnailfishParser(line_a).process() + SnailfishParser(line_b).process()
    magnitude = len(result)
    max_magnitude = max(max_magnitude, magnitude)
print(max_magnitude)
