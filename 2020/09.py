import sys

def main(args):
	size = int(args[0]) if args else 25
	window = []

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
			print(n)
			break
		window.pop(0)
		window.append(n)

if __name__ == '__main__':
	main(sys.argv[1:])
