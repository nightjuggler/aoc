def solve(n, size):
	if n == 1:
		return 1, 1
	if size == 0:
		size = n + 2
	s = [0] * size
	for elf in range(1, size // 2):
		for i in range(elf, min(50 * elf + 1, size), elf):
			s[i] += elf
		i = elf * 2
		if s[i] + i >= n:
			return i, s[i] + i
		i += 1
		if s[i] + i >= n:
			return i, s[i] + i
	print('Please try an array size >', size)
	return 0, 0

def main():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('presents', nargs='?', type=int, default=36000000)
	parser.add_argument('--size', type=int, default=0)
	args = parser.parse_args()

	n = args.presents
	if n <= 0:
		print('The number of presents must be > 0!')
		return
	n, r = divmod(n, 11)
	if r:
		n += 1

	size = args.size
	if size < 0:
		print('The array size must be >= 0!')
		return

	x, s = solve(n, size)

	print('House', x, 'receives', 11 * s, 'presents')

if __name__ == '__main__':
	main()
