import argparse
import re
import sys

def int_if_num(x):
	return int(x) if x[0] in '0123456789' else x

def swap_positions(s, x, y):
	s[x], s[y] = s[y], s[x]

def swap_letters(s, x, y):
	xi = s.index(x)
	yi = s.index(y)
	s[xi] = y
	s[yi] = x

def rotate_by_number(s, lr, x):
	if lr == 'left': x = -x
	x %= len(s)
	sx = s[-x:]
	s[-x:] = []
	s[0:0] = sx

def rotate_by_letter(s, x):
	x = s.index(x)
	x += 1 + int(x >= 4)
	x %= len(s)
	sx = s[-x:]
	s[-x:] = []
	s[0:0] = sx

def reverse_positions(s, x, y):
	s[x:y+1] = s[x:y+1][::-1]

def move_positions(s, x, y):
	letter = s[x]
	del s[x]
	s.insert(y, letter)

def unscramble_rotate_by_letter(s, x):
	xi = s.index(x)

	n = len(s)
	possible = [i for i in range(n) if (i + i + 1 + int(i >= 4)) % n == xi]

	if not possible:
		s = ''.join(s)
		sys.exit(f'Cannot unscramble rotate by letter {x} ({s})!')
	if len(possible) > 1:
		before = ''.join(s)
		possible_after = []
		for i in possible:
			s_copy = s.copy()
			rotate_by_number(s_copy, 'right', i - xi)
			possible_after.append(''.join(s_copy))
		possible = '\n'.join([f'{before} -> {after}' for after in possible_after])
		sys.exit(f'More than one way to unscramble rotate by letter {x}!\n{possible}')

	rotate_by_number(s, 'right', possible[0] - xi)

def read_input():
	number = '([1-9][0-9]*|0)'
	letter = 'letter ([a-z])'
	patterns = list(map(re.compile, (
		f'^swap position {number} with position {number}$',
		f'^swap {letter} with {letter}$',
		f'^rotate (left|right) {number} steps?$',
		f'^rotate based on position of {letter}$',
		f'^reverse positions {number} through {number}$',
		f'^move position {number} to position {number}$',
	)))
	operations = (
		swap_positions,
		swap_letters,
		rotate_by_number,
		rotate_by_letter,
		reverse_positions,
		move_positions,
	)
	ops = []
	for line_num, line in enumerate(sys.stdin, start=1):
		for pattern, op in zip(patterns, operations):
			if m := pattern.match(line):
				ops.append((op, list(map(int_if_num, m.groups()))))
				break
		else:
			sys.exit(f"Input line {line_num} doesn't match pattern!")
	return ops

def scramble(ops, password):
	password = list(password)
	for op, args in ops:
		op(password, *args)
	return ''.join(password)

def unscramble(ops, password):
	password = list(password)
	for op, args in ops[::-1]:
		if op is rotate_by_number:
			args[0] = 'right' if args[0] == 'left' else 'left'
		elif op is rotate_by_letter:
			op = unscramble_rotate_by_letter
		elif op is move_positions:
			args[0], args[1] = args[1], args[0]
		op(password, *args)
	return ''.join(password)

def main():
	parser = argparse.ArgumentParser(allow_abbrev=False)
	parser.add_argument('password', nargs='?')
	parser.add_argument('-2', '--part2', action='store_true')
	args = parser.parse_args()

	ops = read_input()

	if args.part2:
		print(unscramble(ops, args.password or 'fbgdceah'))
	else:
		print(scramble(ops, args.password or 'abcdefgh'))

if __name__ == '__main__':
	main()
