def solve(n, size):
	if n < 4:
		print(1 if n == 0 else 2 if n <= 2 else 3)
		return
	if size == 0:
		size = (n // 2 if n >= 1000 else n) + 1
		print('Setting the array size to', size)
	s = [0] * size
	for elf in range(2, size // 2):
		for i in range(elf, size, elf):
			s[i] += elf
		i = elf * 2
		if s[i] + i >= n:
			print(i)
			return
	print('Please try an array size >', size)

def solve_naive(n):
	if n == 0:
		print(1)
		return
	x = 2
	while True:
		s = x
		for d in range(2, int(x ** 0.5) + 1):
			f, r = divmod(x, d)
			if r == 0:
				s += d if d == f else d + f
		if s >= n:
			break
		x += 1
	print(x)

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
	if r == 0:
		# Every house gets at least 10 presents from the first elf.
		n -= 1

	size = args.size
	if size < 0:
		print('The array size must be >= 0!')
		return

	if args.naive:
		solve_naive(n)
	else:
		solve(n, size)

if __name__ == '__main__':
	main()
