from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor


class Snailfish:

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __add__(self, value):
        total = Snailfish(left=self, right=value)
        total.reduce()
        return total

    def reduce(self):
        pass

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
        result = self.visit(self.tree)
        print(result)
        return Snailfish(left=1, right=1)


content = open("18.txt").read().strip()

total = None
for line in content.split("\n"):
    parser = SnailfishParser(line)
    value = parser.process()
    total = value if total is None else total + value
print(total)
