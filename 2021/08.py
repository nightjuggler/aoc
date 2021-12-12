import sys

def map_wires(signal_patterns):
	wires = {c: set('abcdefg') for c in 'abcdefg'}
	fives = set('abcdefg')
	sixes = set('abcdefg')

	def update_wires(x, keep, remove):
		for c in keep:
			wires[c].intersection_update(x)
		for c in remove:
			wires[c].difference_update(x)

	for x in signal_patterns:
		n = len(x)
		if   n == 2: update_wires(x, 'cf', 'abdeg') # digit 1
		elif n == 3: update_wires(x, 'acf', 'bdeg') # digit 7
		elif n == 4: update_wires(x, 'bcdf', 'aeg') # digit 4
		elif n == 5: fives.intersection_update(x)   # digits 2, 3, and 5
		elif n == 6: sixes.intersection_update(x)   # digits 0, 6, and 9

	update_wires(fives, 'adg', 'bcef')
	update_wires(sixes, 'abfg', 'cde')

#	for wire, possible in wires.items():
#		print(wire, '=>', ', '.join(sorted(possible)))

	assert all([len(possible) == 1 for possible in wires.values()])

	return {b.pop(): a for a, b in wires.items()}

def part2():
	digits = {
		'abcefg':  '0',
		'cf':      '1',
		'acdeg':   '2',
		'acdfg':   '3',
		'bcdf':    '4',
		'abdfg':   '5',
		'abdefg':  '6',
		'acf':     '7',
		'abcdefg': '8',
		'abcdfg':  '9',
	}
	output_sum = 0
	for line in sys.stdin:
		signal_patterns = []
		output_digits = []
		is_output = False
		for x in line.split():
			if x == '|':
				is_output = True
			elif is_output:
				output_digits.append(x)
			else:
				signal_patterns.append(x)
		wires = map_wires(signal_patterns)
		output = int(''.join([digits[''.join(sorted([wires[c] for c in x]))] for x in output_digits]))
		print(f'{" ".join(output_digits)}: {output}')
		output_sum += output

	print(output_sum)

def part1():
	easy_digits = 0
	for line in sys.stdin:
		is_output = False
		for x in line.split():
			if x == '|':
				is_output = True
			elif is_output and len(x) in (2, 3, 4, 7):
				easy_digits += 1
	print(easy_digits)

if __name__ == '__main__':
	if len(sys.argv) == 1:
		part1()
	elif len(sys.argv) != 2 or sys.argv[1] != '2':
		print('usage: wtf?')
	else:
		part2()
