import sys

def main():
	data = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.readline()

	x = 0
	y = 0
	houses = set()
	houses.add((x, y))

	for c in data:
		if   c == '^': y += 1
		elif c == 'v': y -= 1
		elif c == '<': x -= 1
		elif c == '>': x += 1
		elif c != '\n':
			sys.exit('Unexpected character!')
		houses.add((x, y))

	print(len(houses))

if __name__ == '__main__':
	main()
