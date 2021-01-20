import sys

def recurse_verbose(sizes, i, amount, combo=[]):
	count = 0
	for j in range(i, len(sizes)):
		left = amount - sizes[j]
		if left < 0:
			break
		combo.append(sizes[j])
		if left == 0:
			print(', '.join([str(x) for x in combo]))
			count += 1
		else:
			count += recurse_verbose(sizes, j + 1, left, combo)
		combo.pop()
	return count

def recurse(sizes, i, amount):
	count = 0
	for j in range(i, len(sizes)):
		left = amount - sizes[j]
		if left < 0:
			break
		if left == 0:
			count += 1
		else:
			count += recurse(sizes, j + 1, left)
	return count

def main():
	total = 150
	func = recurse

	for arg in sys.argv[1:]:
		if arg == '-v':
			func = recurse_verbose
		elif arg.isdecimal():
			total = int(arg)
		else:
			sys.exit('Usage: {} [-v] [total]'.format(sys.argv[0]))

	sizes = [int(line) for line in sys.stdin]
	sizes.sort()

	print(func(sizes, 0, total))

if __name__ == '__main__':
	main()
