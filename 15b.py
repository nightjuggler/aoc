import sys

def main(args):
	args = args[0] if args else '0,8,15,2,12,1,4'

	memory = {}
	turn = 0
	prev = None

	for n in map(int, args.split(',')):
		if prev is not None:
			memory[prev] = turn
		turn += 1
		prev = n
	while turn < 30000000:
		n = 0 if prev not in memory else turn - memory[prev]
		memory[prev] = turn
		turn += 1
		prev = n

	print(prev)

if __name__ == '__main__':
	main(sys.argv[1:])
