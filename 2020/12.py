import sys
import re

def err(message, *args):
	sys.exit(message.format(*args))

def main():
	line_number = 0
	line_pattern = re.compile('^[A-Z][1-9][0-9]*$')

	X = 0
	Y = 0
	H = 90

	def north(v): nonlocal Y; Y += v
	def south(v): nonlocal Y; Y -= v
	def east(v):  nonlocal X; X += v
	def west(v):  nonlocal X; X -= v
	def left(v):  nonlocal H; H = (H - v) % 360
	def right(v): nonlocal H; H = (H + v) % 360

	heading_lookup = (north, east, south, west)

	def forward(v):
		h, z = divmod(H, 90)
		if z != 0:
			err('At line {}, the heading is not an integer multiple of 90!', line_number)
		heading_lookup[h](v)

	action_lookup = {
		'N': north,
		'S': south,
		'E': east,
		'W': west,
		'L': left,
		'R': right,
		'F': forward,
	}

	for line in sys.stdin:
		line_number += 1
		line = line.strip()
		if not line_pattern.match(line):
			err('Line {} doesn\'t match pattern!', line_number)
		action = action_lookup.get(line[0])
		if not action:
			err('Line {} has an invalid action!', line_number)
		action(int(line[1:]))

	abs_x = abs(X)
	abs_y = abs(Y)
	print('{} {}, {} {}, Heading {}'.format(
		'East' if X >= 0 else 'West', abs_x,
		'North' if Y >= 0 else 'South', abs_y, H))
	print('Manhattan distance =', abs_x + abs_y)

if __name__ == '__main__':
	main()
