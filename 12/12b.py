from collections import defaultdict

content = open("12.txt").read()

links = defaultdict(lambda: list())
for line in content.split("\n"):
    line = line.strip()
    if not line:
        continue
    (origin, destination) = line.split("-")
    links[origin].append(destination)
    links[destination].append(origin)

def explore(origin, path):
    routes = []
    lowercase_repeat_exists = False
    cave_visits = defaultdict(lambda: 0)
    for cave in path:
        cave_visits[cave] += 1
        if cave.islower() and cave_visits[cave] > 1:
            if lowercase_repeat_exists:
                return routes
            lowercase_repeat_exists = True

    for destination in links[origin]:
        if destination == "start":
            continue
        if destination.islower() and cave_visits[destination] > 1:
            continue
        destination_path = path + [destination]
        if destination == "end":
            routes.append(destination_path)
            continue
        routes += explore(destination, destination_path)
    return routes

path = ["start"]
assert "start" in links
routes = explore("start", path)
print(len(routes))
