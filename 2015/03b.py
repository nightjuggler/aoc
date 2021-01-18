import sys

def main():
	data = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.readline()

	xy = ([0, 0], [0, 0])
	houses = set([tuple(pos) for pos in xy])
	robo = False

	for c in data:
		pos = xy[robo]
		if   c == '^': pos[1] += 1
		elif c == 'v': pos[1] -= 1
		elif c == '<': pos[0] -= 1
		elif c == '>': pos[0] += 1
		elif c != '\n':
			sys.exit('Unexpected character!')
		houses.add(tuple(pos))
		robo = not robo

	print(len(houses))

if __name__ == '__main__':
	main()
