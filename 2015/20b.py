def solve(n, size):
	if n == 1:
		print(1)
		return
	if size == 0:
		size = n + 2
		print('Setting the array size to', size)
	s = [0] * size
	for elf in range(1, size // 2):
		for i in range(elf, min(50 * elf + 1, size), elf):
			s[i] += elf
		i = elf * 2
		if s[i] + i >= n:
			print('House', i, 'receives', 11 * (s[i] + i), 'presents')
			return
		i += 1
		if s[i] + i >= n:
			print(i)
			return
	print('Please try an array size >', size)

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

	solve(n, size)

if __name__ == '__main__':
	main()
