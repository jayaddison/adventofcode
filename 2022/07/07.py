from collections import defaultdict

content = open("07.txt").read()


def parse_command(cwd, cmd):
    """Parse an individual command from the console logs"""
    match cmd.split():
        case "ls":
           cmd = "ls"
           cwd = cwd
        case "cd", "..":
           cmd = "cd"
           cwd = "/" + "/".join(cwd.split("/")[1:-2])
        case "cd", "/":
           cmd = "cd"
           cwd = "/"
        case "cd", _ as directory:
           cmd = "cd"
           cwd += directory + "/"
    return cwd, cmd


def component_paths(path):
    """Given a directory, return that path and all parent directory paths"""
    depth = path.count("/")
    segments = path.split("/")
    for idx in range(depth, 0, -1):
        yield "/".join(segments[:idx]) + "/"


directory_sizes = defaultdict(int)

def parse_ls(cwd, line):
    if line.startswith("dir"):
        return
    size, filename = line.split()
    for path in component_paths(cwd):
        directory_sizes[path] += int(size)


cwd, cmd = None, None
for line in content.splitlines():
    if line.startswith("$"):
        _, cmd = line.split(" ", 1)
        cwd, cmd = parse_command(cwd, cmd)
    elif cmd == "ls":
        parse_ls(cwd, line)

SIZE_LIMIT = 100_000

total_size = 0
for directory, size in directory_sizes.items():
    total_size += size if size <= SIZE_LIMIT else 0
print(total_size)

assert list(component_paths("/abc/def/")) == ["/abc/def/", "/abc/", "/"]
