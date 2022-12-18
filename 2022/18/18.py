from itertools import combinations

content = open("18.txt").read()


def vertex_to_cube(x, y, z, size=1):
    return [
        (x, y, z),
        (...),
        (x + 1, y + 1, z + 1),
    ]


def cube_to_surfaces(cube):
    pass


surfaces = set()
for line in content.splitlines():
    x, y, z = [int(c) for c in line.split(",")]
    cube = vertex_to_cube(x, y, z)
    cube_surfaces = cube_to_surfaces(cube)
    surfaces.add(cube_surfaces)

print(len(surfaces))
