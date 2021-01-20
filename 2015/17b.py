import sys

def solve(sizes, total, verbose=False):
	num_sizes = len(sizes)
	min_len = num_sizes + 1
	min_count = 0
	min_combos = []
	combo = []

	sizes.sort()

	def recurse(i, amount, combo_len):
		nonlocal min_len, min_count

		for j in range(i, num_sizes):
			left = amount - sizes[j]
			if left < 0:
				break
			if left == 0:
				if combo_len < min_len:
					min_len = combo_len
					min_count = 1
					min_combos.clear()
				else:
					assert combo_len == min_len
					min_count += 1
				combo.append(sizes[j])
				min_combos.append(combo.copy())
				combo.pop()
			elif combo_len < min_len:
				combo.append(sizes[j])
				recurse(j + 1, left, combo_len + 1)
				combo.pop()

	recurse(0, total, 1)
	if verbose:
		for combo in min_combos:
			print(', '.join([str(x) for x in combo]))

	print('Minimum number of containers =', None if min_count == 0 else min_len)
	print('Number of different combinations =', min_count)

def main():
	total = 150
	verbose = False

	for arg in sys.argv[1:]:
		if arg == '-v':
			verbose = True
		elif arg.isdecimal():
			total = int(arg)
		else:
			sys.exit('Usage: {} [-v] [total]'.format(sys.argv[0]))

	sizes = [int(line) for line in sys.stdin]
	solve(sizes, total, verbose)

if __name__ == '__main__':
	main()
