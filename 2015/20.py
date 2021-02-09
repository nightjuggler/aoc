def solve(n, size):
	if n == 1:
		return 1, 1
	if size == 0:
		size = n + 2
	s = [0] * size
	for elf in range(1, size // 2):
		for i in range(elf, size, elf):
			s[i] += elf
		i = elf * 2
		if s[i] + i >= n:
			return i, s[i] + i
		i += 1
		if s[i] + i >= n:
			return i, s[i] + i
	print('Please try an array size >', size)
	return 0, 0

def solve_naive(n):
	x = 1
	while True:
		s = 0
		for d in range(1, int(x ** 0.5) + 1):
			f, r = divmod(x, d)
			if r == 0:
				s += d if d == f else d + f
		if s >= n:
			break
		x += 1
	return x, s

def main():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('presents', nargs='?', type=int, default=36000000)
	parser.add_argument('--naive', action='store_true')
	parser.add_argument('--size', type=int, default=0)
	args = parser.parse_args()

	n = args.presents
	if n <= 0:
		print('The number of presents must be > 0!')
		return
	n, r = divmod(n, 10)
	if r:
		n += 1

	size = args.size
	if size < 0:
		print('The array size must be >= 0!')
		return

	x, s = solve_naive(n) if args.naive else solve(n, size)

	print('House', x, 'receives', 10 * s, 'presents')

if __name__ == '__main__':
	main()
