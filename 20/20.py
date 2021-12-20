content = open("20.txt").read()

input_algorithm, input_image = content.split("\n\n")

algorithm = ['1' if char == '#' else 0 for char in input_algorithm]

image = []
for line in input_image.split("\n"):
    line = line.strip()
    if not line:
        continue
    row = ['1' if char == '#' else '0' for char in line]
    image.append(row)

def input_pixel_to_bitstring(x, y):
    bitstring = []
    for row in [y - 1, y, y + 1]:
        for col in [x - 1, x, x + 1]:
            bitstring.append(image[row][col])
    return str().join(bitstring)

def output_pixel(x, y):
    index_bitstring = input_pixel_to_bitstring(x, y)
    index = int(index_bitstring, 2)
    return algorithm[index]
    

print(len(algorithm))
print(output_pixel(2, 2))
