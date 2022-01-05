import sys

def get_layers(size):
	line = sys.stdin.readline().rstrip()
	line_len = len(line)
	if not line or line_len % size:
		raise SystemExit(f'Expected one or more layers of exactly {size} digits!')
	if line.rstrip('012'):
		raise SystemExit('Expected only the digits 0, 1, and 2!')

	return [list(map(int, line[i:i+size])) for i in range(0, line_len, size)]

def zeros(digits):
	count = [0] * 3
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

	print('Part 2:')
	for j in range(0, size, width):
		print(''.join([' # '[image[j + i]] for i in range(width)]))

main()
