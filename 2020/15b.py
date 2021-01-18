import sys

def main():
	args = sys.argv
	args = (args[1] if len(args) > 1 else '0,8,15,2,12,1,4').split(',')

	argc = len(args)
	memory = {int(args[turn-1]): turn for turn in range(1, argc)}
	prev = int(args[argc-1])

	for turn in range(argc, 30000000):
		n = turn - memory.get(prev, turn)
		memory[prev] = turn
		prev = n

	print(prev)

if __name__ == '__main__':
	main()
