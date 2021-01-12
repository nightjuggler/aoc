import sys
import re

def binary_partition(s, c_lo):
	size = 1 << len(s)
	lo = 0
	for c in s:
		size //= 2
		if c != c_lo:
			lo += size
	return lo

def main():
	line_number = 0
	line_pattern = re.compile('^[BF]{7}[LR]{3}$')
	seats = []

	for line in sys.stdin:
		line_number += 1
		if not line_pattern.match(line):
			sys.exit('Line {} doesn\'t match pattern!'.format(line_number))
		row = binary_partition(line[:7], 'F')
		col = binary_partition(line[7:10], 'L')
		seat = row * 8 + col
		seats.append(seat)

	seats.sort()
	prev = seats.pop(0)
	for seat in seats:
		if seat != prev + 1:
			assert seat == prev + 2
			print(prev + 1)
		prev = seat

if __name__ == '__main__':
	main()
