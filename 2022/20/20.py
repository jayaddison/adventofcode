content = open("20.txt").read()
numbers = content.splitlines()


class Node:
    def __init__(self, value, prev):
        if prev:
            prev.next = self
        self.prev = prev
        self.value = value


# Create a linked list
nodes = []
prev = None
for number in numbers:
    node = Node(int(number), prev)
    nodes.append(node)
    prev = node


# Make the linked list into a circular list
nodes[0].prev, nodes[-1].next = nodes[-1], nodes[0]

for node in nodes:
    moves = abs(node.value) % (len(nodes) * 2)
    if moves == 0:
        continue
    for _ in range(moves):
        if node.value > 0:
            a, b, c, d = node.prev, node, node.next, node.next.next
            a.next = c
            c.prev = a
            c.next = b
            b.prev = c
            b.next = d
            d.prev = b
        else:
            w, x, y, z = node.prev.prev, node.prev, node, node.next
            z.prev = x
            x.next = z
            x.prev = y
            y.next = x
            y.prev = w
            w.next = y

zero_node = None
for node in nodes:
    if node.value == 0:
        zero_node = node
        break
assert zero_node


def advance(node, iterations):
    global nodes
    steps = iterations % len(nodes)
    for _ in range(steps):
        node = node.next
    return node


coordinates = (
    advance(zero_node, 1000),
    advance(zero_node, 2000),
    advance(zero_node, 3000),
)


print(sum(coordinate.value for coordinate in coordinates))
