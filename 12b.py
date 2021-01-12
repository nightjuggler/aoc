import sys
import re

def err(message, *args):
	sys.exit(message.format(*args))

def position(x, y):
	return '{} {}, {} {}'.format(
		'east' if x >= 0 else 'west', abs(x),
		'north' if y >= 0 else 'south', abs(y))

def main():
	line_number = 0
	line_pattern = re.compile('^[A-Z][1-9][0-9]*$')

	X = 0
	Y = 0
	WX = 10
	WY = 1

	def north(v): nonlocal WY; WY += v
	def south(v): nonlocal WY; WY -= v
	def east(v):  nonlocal WX; WX += v
	def west(v):  nonlocal WX; WX -= v

	rotation_matrix = (
		( 1,  0,  0,  1), # 0 degrees
		( 0,  1, -1,  0), # 90 degrees
		(-1,  0,  0, -1), # 180 degrees
		( 0, -1,  1,  0), # 270 degrees
	)

	def right(v):
		nonlocal WX, WY
		v, z = divmod(v % 360, 90)
		if z != 0:
			err('On line {}, the angle is not an integer multiple of 90!', line_number)

		a, b, c, d = rotation_matrix[v]
		x, y = WX, WY
		WX = a * x + b * y
		WY = c * x + d * y

	def left(v):
		right(-v)

	def forward(v):
		nonlocal X, Y, WX, WY
		X += v * WX
		Y += v * WY

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

	print('The ship is at', position(X, Y))
	print('The waypoint is at', position(WX, WY))
	print('The Manhattan distance is', abs(X) + abs(Y))

if __name__ == '__main__':
	main()
