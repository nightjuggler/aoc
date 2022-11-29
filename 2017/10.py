import argparse
import sys

def hash(lengths, num_elements, num_rounds):
	assert all(length <= num_elements for length in lengths)
	elements = list(range(num_elements))
	i = skip = 0
	for _ in range(num_rounds):
		for length in lengths:
			skip += 1
			j = i + length - 1
			next_pos = (j + skip) % num_elements
			while i < j:
				i2 = i % num_elements
				j2 = j % num_elements
				elements[i2], elements[j2] = elements[j2], elements[i2]
				i += 1
				j -= 1
			i = next_pos
	return elements

def reduce(elements):
	output = 0
	for n in elements:
		output ^= n
	return format(output, '02x')

def main():
	parser = argparse.ArgumentParser(allow_abbrev=False)
	parser.add_argument('-1', dest='part_one', action='store_true')
	parser.add_argument('-n', dest='num_elements', type=int, default=256)
	args = parser.parse_args()

	num_elements = args.num_elements
	if not 2 <= num_elements <= 256:
		sys.exit('The number of elements must be >= 2 and <= 256!')
	puzzle_input = sys.stdin.readline()

	if args.part_one:
		lengths = list(map(int, puzzle_input.split(',')))
		elements = hash(lengths, num_elements, 1)
		print('Part 1:', elements[0] * elements[1])
	else:
		lengths = list(map(ord, puzzle_input.strip()))
		lengths.extend([17, 31, 73, 47, 23])
		elements = hash(lengths, num_elements, 64)
		print('Part 2:', ''.join([reduce(elements[i:i+16]) for i in range(0, num_elements, 16)]))

main()
