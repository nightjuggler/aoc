import sys

def part1(lines):
	x, y = 1, 1 # corresponds to 5 on the keypad
	code = []
	for line_num, line in enumerate(lines, start=1):
		for c in line:
			if   c == 'D': y = min(y + 1, 2)
			elif c == 'L': x = max(x - 1, 0)
			elif c == 'R': x = min(x + 1, 2)
			elif c == 'U': y = max(y - 1, 0)
			else:
				print('Unexpected character on input line', line_num)
				return
		code.append(y*3 + x + 1)
	print('Part 1: ', *code, sep='')

def part2(lines):
	keypad = (
		'       ',
		'   1   ',
		'  234  ',
		' 56789 ',
		'  ABC  ',
		'   D   ',
		'       ',
	)
	x, y = 1, 3
	code = []
	for line_num, line in enumerate(lines, start=1):
		for c in line:
			if c == 'D':
				if keypad[y+1][x] != ' ': y += 1
			elif c == 'L':
				if keypad[y][x-1] != ' ': x -= 1
			elif c == 'R':
				if keypad[y][x+1] != ' ': x += 1
			elif c == 'U':
				if keypad[y-1][x] != ' ': y -= 1
			else:
				print('Unexpected character on input line', line_num)
				return
		code.append(keypad[y][x])
	print('Part 2: ', *code, sep='')

def main():
	lines = [line.rstrip() for line in sys.stdin]
	part1(lines)
	part2(lines)

if __name__ == '__main__':
	main()
