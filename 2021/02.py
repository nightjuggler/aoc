import sys

def part1():
	position, depth = 0, 0
	for line in sys.stdin:
		cmd, x = line.split()
		x = int(x)
		if cmd == 'forward':
			position += x
		elif cmd == 'down':
			depth += x
		elif cmd == 'up':
			depth -= x
		else:
			print('input: wtf?')
	print(position * depth)

def part2():
	position, depth, aim = 0, 0, 0
	for line in sys.stdin:
		cmd, x = line.split()
		x = int(x)
		if cmd == 'forward':
			position += x
			depth += aim * x
		elif cmd == 'down':
			aim += x
		elif cmd == 'up':
			aim -= x
		else:
			print('input: wtf?')
	print(position * depth)

if __name__ == '__main__':
	if len(sys.argv) == 1:
		part1()
	elif len(sys.argv) != 2 or sys.argv[1] != '2':
		print('usage: wtf?')
	else:
		part2()
