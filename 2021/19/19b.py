from itertools import permutations

content = open("19b.txt").read()

keystones = []
for line in content.split("\n"):
    line = line.strip()
    if not line:
        continue
    x, y, z = line.split(",")
    keystones.append((int(x), int(y), int(z)))


def manhattan_distance(keystone_a, keystone_b):
    x_dist = keystone_a[0] - keystone_b[0]
    y_dist = keystone_a[1] - keystone_b[1]
    z_dist = keystone_a[2] - keystone_b[2]
    return abs(x_dist) + abs(y_dist) + abs(z_dist)


max_dist = None
for keystone_a, keystone_b in permutations(keystones, 2):
    distance = manhattan_distance(keystone_a, keystone_b)
    print(f"{distance} {keystone_a} {keystone_b}")
    max_dist = distance if max_dist is None or distance > max_dist else max_dist
print(max_dist)
