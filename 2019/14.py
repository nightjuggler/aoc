import re
import sys

def split_qty(qty):
	qty, name = qty.split(' ')
	return int(qty), name

def read_input():
	pattern = re.compile('^{x}(?:, {x})* => {x}$'.format(x='[1-9][0-9]* [A-Z]+'))
	rules = {}
	for line_num, line in enumerate(sys.stdin, start=1):
		if not pattern.match(line):
			sys.exit(f"Input line {line_num} doesn't match pattern!")
		inputs, output = line.rstrip().split(' => ')
		qty, name = split_qty(output)
		assert name not in rules
		rules[name] = (qty, tuple(map(split_qty, inputs.split(', '))))
	return rules

def main():
	rules = read_input()
	extra = {}

	def solve(want_qty, want_name):
		if (have_qty := extra.setdefault(want_name, 0)):
			if have_qty >= want_qty:
				extra[want_name] = have_qty - want_qty
				return 0
			want_qty -= have_qty
			extra[want_name] = 0

		qty, inputs = rules[want_name]
		mult, left = divmod(want_qty, qty)
		if left:
			mult += 1
			left = qty - left
		ore = 0
		for qty, name in inputs:
			qty *= mult
			if name == 'ORE':
				ore += qty
			else:
				ore += solve(qty, name)
		extra[want_name] += left
		return ore

	ore_per_fuel = solve(1, 'FUEL')
	print('Part 1:', ore_per_fuel)

	ore_left = 1_000_000_000_000
	total_fuel = 0
	while True:
		fuel = ore_left // ore_per_fuel
		if not fuel:
			while (ore := solve(1, 'FUEL')) <= ore_left:
				ore_left -= ore
				total_fuel += 1
			break
		ore_left -= solve(fuel, 'FUEL')
		total_fuel += fuel

	print('Part 2:', total_fuel)

if __name__ == '__main__':
	main()
