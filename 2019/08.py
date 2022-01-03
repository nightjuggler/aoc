import sys

def get_layers(size):
	line = sys.stdin.readline()
	line_len = len(line) // size * size
	if line_len < size or line[line_len:].rstrip():
		raise SystemExit(f'Expected one or more layers of exactly {size} digits!')
	if not all([line[i] in '0123456789' for i in range(line_len)]):
		raise SystemExit('Expected only decimal digits!')

	return [list(map(int, line[i:i+size])) for i in range(0, line_len, size)]

def zeros(digits):
	count = [0] * 10
	for d in digits:
		count[d] += 1
	return count[0], count[1] * count[2]

def main():
	width, height = 25, 6
	size = width * height

	layers = get_layers(size)

	print('Part 1:', sorted(map(zeros, layers))[0][1])

	image = [2] * size
	for layer in layers:
		for i in range(size):
			if image[i] == 2 and layer[i] != 2:
				image[i] = layer[i]

	i2a = [' ', '#', ' ']

	print('Part 2:')
	for j in range(0, size, width):
		print(''.join([i2a[image[j + i]] for i in range(width)]))

main()
