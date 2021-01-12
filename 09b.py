import sys

def main(args):
	size = int(args[0]) if args else 25
	window = []
	numbers = []
	target = None

	for i, line in enumerate(sys.stdin):
		n = int(line.strip())
		if i < size:
			window.append(n)
			continue
		for j, x in enumerate(window):
			y = n - x
			if y == x:
				continue
			if y in window[j+1:]:
				break
		else:
			target = n
			break
		numbers.append(window.pop(0))
		window.append(n)

	if target is None:
		sys.exit('Wtf?')

	numbers.extend(window)
	numlen = len(numbers)
	for i, n in enumerate(numbers):
		j = i + 1
		while j < numlen and n < target:
			n += numbers[j]
			j += 1
		if n == target and j - i > 1:
			numbers = numbers[i:j]
			print(' + '.join(map(str, numbers)), '=', target)
			minnum = min(numbers)
			maxnum = max(numbers)
			print(minnum, '+', maxnum, '=', minnum + maxnum)
			break

if __name__ == '__main__':
	main(sys.argv[1:])
