import sys

def possible(sides):
	return sum([a + b > c and a + c > b and b + c > a for a, b, c in sides])

def main():
	sides1 = [tuple(map(int, line.split())) for line in sys.stdin]

	print('Part 1:', possible(sides1))

	sides2 = []
	for i in range(0, len(sides1), 3):
		sides2.extend(list(zip(*sides1[i:i+3])))

	print('Part 2:', possible(sides2))

if __name__ == '__main__':
	main()
