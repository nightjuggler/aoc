import argparse
import operator
import sys

def solve(row, num_rows, verbose=False):
	row = [True, *(c == '.' for c in row), True]
	num_safe = sum(row) - 2

	if verbose:
		print(''.join(['^.'[c] for c in row[1:-1]]))

	for _ in range(num_rows - 1):
		row = [True, *map(operator.eq, row[:-2], row[2:]), True]
		num_safe += sum(row) - 2

		if verbose:
			print(''.join(['^.'[c] for c in row[1:-1]]))

	return num_safe

def main():
	parser = argparse.ArgumentParser(allow_abbrev=False)
	parser.add_argument('rows', nargs='?', type=int, default=40)
	parser.add_argument('-v', '--verbose', action='store_true')
	args = parser.parse_args()

	row = sys.stdin.readline().rstrip()
	if not row or row.strip('^.'):
		sys.exit('Invalid input!')

	print(solve(row, args.rows, args.verbose))

if __name__ == '__main__':
	main()
