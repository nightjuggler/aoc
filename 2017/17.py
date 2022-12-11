import argparse

def part1(steps, num_values, before_value):
	steps -= 1
	after = [0] * (num_values + 1)
	next_pos = 0
	for value in range(1, num_values + 1):
		pos = next_pos
		for _ in range(steps):
			pos = after[pos]
		after[value] = next_pos = after[pos]
		after[pos] = value
	return after[before_value]

def part2(steps, num_values):
	pos = 0
	after0 = 0
	for value in range(1, num_values + 1):
		pos = (pos + steps) % value
		if not pos:
			after0 = value
		pos += 1
	return after0

def main():
	parser = argparse.ArgumentParser(allow_abbrev=False)
	parser.add_argument('steps', nargs='?', type=int, default=328)
	args = parser.parse_args()

	print('Part 1:', part1(args.steps, 2017, 2017))
	print('Part 2:', part2(args.steps, 50_000_000))
main()
