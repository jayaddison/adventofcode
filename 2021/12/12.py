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
    path_as_set = set(path)
    for destination in links[origin]:
        if destination.islower() and destination in path_as_set:
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
