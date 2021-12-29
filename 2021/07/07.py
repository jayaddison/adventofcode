from statistics import median

content = open("07.txt").read()

x_positions = [int(n) for n in content.split(",")]
x_median = median(x_positions)
x_target = round(x_median)

fuel_consumption = sum([abs(x_position - x_target) for x_position in x_positions])
print(fuel_consumption)
