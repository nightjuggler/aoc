import argparse
import sys

def err(message, *args):
	sys.exit(message.format(*args) if args else message)

def print_rows(rows, header):
	y_stop = len(rows) - 1
	x_stop = len(rows[0]) - 1

	print(header + ':')
	for y in range(1, y_stop):
		print(''.join(['#' if rows[y][x] else '.' for x in range(1, x_stop)]))
	print()

def play(rows):
	num_rows = len(rows)
	num_cols = len(rows[0])

	y_stop = num_rows - 1
	x_stop = num_cols - 1

	num_ones = 0
	new_rows = [[0] * num_cols for y in range(num_rows)]

	for y in range(1, y_stop):
		for x in range(1, x_stop):
			n = sum([rows[j][i] for j in range(y-1, y+2) for i in range(x-1, x+2)])
			if n == 3 or n == 4 and rows[y][x]:
				new_rows[y][x] = 1
				num_ones += 1

	return num_ones, new_rows

def init(input_file):
	rows = []
	num_on = 0
	num_cols = 0

	for y, line in enumerate(input_file, start=1):
		line = line.rstrip()
		if num_cols == 0:
			num_cols = len(line) + 2
			rows.append([0] * num_cols)
		elif len(line) + 2 != num_cols:
			err('Line {}: Unexpected length!', y)

		row = [0] * num_cols
		for x, c in enumerate(line, start=1):
			if c == '#':
				row[x] = 1
				num_on += 1
			elif c != '.':
				err('Line {}, column {}: Unexpected character!', y, x)
		rows.append(row)

	if num_cols == 0:
		num_cols = 2
		rows.append([0] * num_cols)

	rows.append([0] * num_cols)
	print(len(rows) - 2, 'x', num_cols - 2)
	return num_on, rows

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('steps', nargs='?', type=int, default=100)
	parser.add_argument('-v', '--verbose', action='store_true')
	args = parser.parse_args()

	num_steps = args.steps
	verbose = args.verbose

	num_on, rows = init(sys.stdin)
	if verbose:
		print_rows(rows, 'Initial state')

	for step in range(1, num_steps + 1):
		num_on, rows = play(rows)
		if verbose:
			print_rows(rows, 'After {} step{}'.format(step, '' if step == 1 else 's'))

	print('{} lights are on after {} steps'.format(num_on, num_steps))

if __name__ == '__main__':
	main()
