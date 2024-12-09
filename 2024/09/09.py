import sys

disk_map = list(sys.stdin.read().strip())
files = list(enumerate(map(int, disk_map[::2])))
spaces = list(map(int, disk_map[1::2]))
filesystem = []

def filesystem_representation(filesystem):
    return str().join('.' if block is None else str(block) for block in filesystem)

def filesystem_checksum(filesystem):
    return sum(idx * block for idx, block in enumerate(filesystem) if block is not None)

while files or spaces:
    if files:
        (file_id, file_size), files = files[0], files[1:]
        filesystem += [file_id] * file_size
    if spaces:
        space, spaces = spaces[0], spaces[1:]
        filesystem += [None] * space

print(filesystem_representation(filesystem))

while any(block is None for block in filesystem):
    block = filesystem.pop()
    empty = filesystem.index(None)
    filesystem = filesystem[:empty] + [block] + filesystem[empty + 1:]

print(filesystem_representation(filesystem))
print(filesystem_checksum(filesystem))
