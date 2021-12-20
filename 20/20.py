content = open("20.txt").read()

input_algorithm, input_image_text = content.split("\n\n")
input_algorithm = [True if char == "#" else False for char in input_algorithm]

input_image = []
for line in input_image_text.split("\n"):
    line = line.strip()
    if not line:
        continue
    row = [char == "#" for char in line]
    input_image.append(row)


def pixel_neighbour_bitstring(source, x, y):
    bitstring = []
    for row in [y - 1, y, y + 1]:
        for col in [x - 1, x, x + 1]:
            try:
                bit = "1" if source[row][col] else "0"
            except:
                bit = "0"
            bitstring.append(bit)
    return str().join(bitstring)


def transform_pixel(source, x, y, algorithm):
    index_bitstring = pixel_neighbour_bitstring(source, x, y)
    index = int(index_bitstring, 2)
    return algorithm[index]


def render(source):
    width = len(source[0])
    height = len(source)
    for y in range(height):
        for x in range(width):
            print("#" if source[y][x] else ".", end="")
        print()
    print(count_light_pixels(source))
    print()


def empty_canvas(source):
    width = len(source[0])
    height = len(source)

    result = []
    for _ in range(height):
        result.append([False] * width)
    return result


def has_light_border(source):
    for y in (0, len(source) - 1):
        for value in source[y]:
            if value:
                return True
    for x in (0, len(source[0]) - 1):
        for y in range(len(source)):
            if source[y][x]:
                return True
    return False


def expand(source):
    width = len(source[0])
    height = len(source)

    result = []
    result.append([False] * (width + 2))
    for y in range(height):
        result.append([False] + source[y] + [False])
    result.append([False] * (width + 2))
    return result


def apply_algorithm(source, algorithm):
    destination = empty_canvas(source)
    width = len(destination[0])
    height = len(destination)
    for x in range(width):
        for y in range(height):
            destination[y][x] |= transform_pixel(source, x, y, algorithm)
    return destination


def apply_algorithm_repeatedly(source, algorithm, steps=1):
    for _ in range(steps):
        if has_light_border(source):
            source = expand(source)
        source = apply_algorithm(source, algorithm)
        render(source)
    return source


def count_light_pixels(source):
    return sum(sum(row) for row in source)


apply_algorithm_repeatedly(input_image, input_algorithm, steps=2)
