from functools import cache
from math import floor
from statistics import median

content = open("07.txt").read()

x_positions = [int(n) for n in content.split(",")]
x_average = sum(x_positions) / len(x_positions)
x_target = floor(x_average)

def cost(n):
    return sum(range(n + 1))

fuel_consumption = sum([cost(abs(x_position - x_target)) for x_position in x_positions])
print(fuel_consumption)
