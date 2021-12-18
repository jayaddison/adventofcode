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
        print(f"b: {total}")
        while reducing:
            reducing = total.reduce(mode="explode")
            if reducing:
                print(f"e: {total}")
                continue
            reducing = total.reduce(mode="split") or reducing
            if reducing:
                print(f"s: {total}")
        return total

    def reduce(self, mode="explode"):
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

            if carry_number and not isinstance(current_node.right, Snailfish):
                current_node.right += carry_number
                carry_number = 0

            if depth == 4 and mode == "explode" and not modified:
                explode = None
                if isinstance(current_node.left, Snailfish):
                    explode = current_node.left
                elif isinstance(current_node.right, Snailfish):
                    explode = current_node.right
                modified = explode is not None

                if current_node.left == explode:
                    current_node.left = 0
                    if isinstance(explode.left, Snailfish):
                        explode = explode.left
                    if previous_number_node:
                        if not isinstance(previous_number_node.right, Snailfish):
                            previous_number_node.right += explode.left
                        elif not isinstance(previous_number_node.left, Snailfish):
                            previous_number_node.left += explode.left
                    if isinstance(current_node.right, Snailfish):
                        current_node.right.left += explode.right
                    else:
                        current_node.right += explode.right

                elif current_node.right == explode:
                    current_node.right = 0
                    if isinstance(explode.left, Snailfish):
                        explode = explode.left
                    previous_number_node.left += explode.left
                    carry_number = explode.right

            if mode == "split" and type(current_node.left) == int and current_node.left >= 10:
                current_node.left = Snailfish(
                    left=floor(current_node.left / 2),
                    right=ceil(current_node.left / 2),
                )
                return True

            if mode == "split" and type(current_node.right) == int and current_node.right >= 10:
                current_node.right = Snailfish(
                    left=floor(current_node.right / 2),
                    right=ceil(current_node.right / 2),
                )
                return True

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
    test_snailfish.reduce()

    assert str(test_snailfish) == expected_output

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

    print(f"in: {test_lhs} + {test_rhs}")
    print(f"ac: {test_sum}")
    print(f"ex: {expected_output}")
    print(str(test_sum) == expected_output)
    print()


if False:
	content = open("18.txt").read().strip()

	total = None
	for line in content.split("\n"):
	    parser = SnailfishParser(line)
	    value = parser.process()
	    total = value if total is None else total + value
	print(total)
