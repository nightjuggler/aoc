import re
import sys

def read_input():
	dot_pattern = re.compile('^(0|[1-9][0-9]*),(0|[1-9][0-9]*)$')
	fold_pattern = re.compile('^fold along ([xy])=([1-9][0-9]*)$')
	line_number = 0

	dots = set()
	for line in sys.stdin:
		line_number += 1
		m = dot_pattern.match(line)
		if not m:
			if not line.rstrip(): break
			print(f'Input line {line_number} doesn\'t match pattern!')
			return None, None
		x, y = m.groups()
		dots.add((int(x), int(y)))

	folds = []
	for line in sys.stdin:
		line_number += 1
		m = fold_pattern.match(line)
		if not m:
			print(f'Input line {line_number} doesn\'t match pattern!')
			return None, None
		x_or_y, value = m.groups()
		folds.append((x_or_y == 'y', int(value)))

	return dots, folds

def main():
	dots, folds = read_input()
	if not dots:
		return

	first = True
	for fold_up, fold_value in folds:
		new_dots = set()
		if fold_up:
			for x, y in dots:
				if y > fold_value:
					y = fold_value - (y - fold_value)
				new_dots.add((x, y))
		else:
			for x, y in dots:
				if x > fold_value:
					x = fold_value - (x - fold_value)
				new_dots.add((x, y))
		dots = new_dots
		if first:
			print(len(dots), 'dots after the first fold')
			first = False

	first = True
	min_x, max_x = None, None
	min_y, max_y = None, None
	for x, y in dots:
		if first:
			min_x = max_x = x
			min_y = max_y = y
			first = False
		else:
			if x < min_x: min_x = x
			elif x > max_x: max_x = x
			if y < min_y: min_y = y
			elif y > max_y: max_y = y

	for y in range(min_y, max_y + 1):
		print(''.join(['#' if (x, y) in dots else '.' for x in range(min_x, max_x + 1)]))

if __name__ == '__main__':
	main()
