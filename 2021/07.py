import sys

def distance1(a, b):
	return abs(a - b)

def distance2(a, b):
	d = abs(a - b)
	return d * (d + 1) // 2

def sum_at_median(positions, distance):
	i, odd = divmod(len(positions), 2)

	median = positions[i]
	fuel = sum([distance(n, median) for n in positions])
	print(fuel, 'fuel @ median position', median)

	if odd or median == positions[i-1]:
		return

	median = positions[i-1]
	fuel = sum([distance(n, median) for n in positions])
	print(fuel, 'fuel @ median position', median)

def sum_at_average(positions, distance):
	float_average = sum(positions) / len(positions)
	print('The average is', float_average)

	average = int(float_average)
	fuel = sum([distance(n, average) for n in positions])
	print(fuel, 'fuel @ position', average)

	if average == float_average:
		return

	average += 1
	fuel = sum([distance(n, average) for n in positions])
	print(fuel, 'fuel @ position', average)

def main(distance):
	positions = [int(n) for n in sys.stdin.readline().split(',')]
	positions.sort()

	dashes = '-' * 40
	print(dashes)
	sum_at_median(positions, distance)
	print(dashes)
	sum_at_average(positions, distance)
	print(dashes)

	min_pos = positions[0]
	max_pos = positions[-1]

	min_fuel = sum([distance(n, max_pos) for n in positions])
	min_fuel_pos = max_pos

	for pos in range(min_pos, max_pos):
		fuel = sum([distance(n, pos) for n in positions])
		if fuel < min_fuel:
			min_fuel = fuel
			min_fuel_pos = pos

	print(min_fuel, 'fuel @ position', min_fuel_pos)
	print(dashes)

if __name__ == '__main__':
	if len(sys.argv) == 1:
		main(distance1)
	elif len(sys.argv) != 2 or sys.argv[1] != '2':
		print('usage: wtf?')
	else:
		main(distance2)
