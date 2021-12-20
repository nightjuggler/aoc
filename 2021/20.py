import sys

class InputError(Exception):
	pass

def read_input():
	f = sys.stdin
	line = f.readline().rstrip()
	if len(line) != 512:
		raise InputError('Input line 1 must be 512 characters long!')
	if not all([c == '#' or c == '.' for c in line]):
		raise InputError('Input line 1: Unexpected character!')
	iea = [c == '#' for c in line]
	if f.readline() != '\n':
		raise InputError('Input line 2: Expected a blank line!')
	image = set()
	for y, line in enumerate(f):
		line = line.rstrip()
		if not all([c == '#' or c == '.' for c in line]):
			raise InputError(f'Input line {y+3}: Unexpected character!')
		for x, c in enumerate(line):
			if c == '#':
				image.add((x, y))
	return iea, image

def print_image(image):
	first = True
	min_x, max_x = None, None
	min_y, max_y = None, None
	for x, y in image:
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
		print(''.join(['#' if (x, y) in image else '.' for x in range(min_x, max_x + 1)]))

def apply(iea, image, border):
	first = True
	min_x, max_x = None, None
	min_y, max_y = None, None
	for x, y in image:
		if first:
			min_x = max_x = x
			min_y = max_y = y
			first = False
		else:
			if x < min_x: min_x = x
			elif x > max_x: max_x = x
			if y < min_y: min_y = y
			elif y > max_y: max_y = y

	new_image = set()
	for y in range(min_y - 1, max_y + 2):
		for x in range(min_x - 1, max_x + 2):
			n = []
			for ay in (y + 1, y, y - 1):
				if ay < min_y or ay > max_y:
					n.append(border)
					n.append(border)
					n.append(border)
					continue
				for ax in (x + 1, x, x - 1):
					if ax < min_x or ax > max_x:
						n.append(border)
					else:
						n.append((ax, ay) in image)

			if iea[sum([1 << bit for bit, on in enumerate(n) if on])]:
				new_image.add((x, y))
	return new_image

def main():
	try:
		iea, image = read_input()
	except InputError as e:
		print(e)
		return

	border = False
	for step in range(50):
		image = apply(iea, image, border)
		border = iea[-1 if border else 0]
		if step == 1:
#			print_image(image)
			print('Part 1:', len(image))

	print('Part 2:', len(image))

if __name__ == '__main__':
	main()
