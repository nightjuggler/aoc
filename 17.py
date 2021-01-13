import sys

def err(message, *args):
	sys.exit(message.format(*args))

class State(object):
	def __init__(self):
		self.active = set()

	def add(self, x, y, z):
		if self.active:
			if   x < self.min_x: self.min_x = x
			elif x > self.max_x: self.max_x = x
			if   y < self.min_y: self.min_y = y
			elif y > self.max_y: self.max_y = y
			if   z < self.min_z: self.min_z = z
			elif z > self.max_z: self.max_z = z
		else:
			self.min_x = self.max_x = x
			self.min_y = self.max_y = y
			self.min_z = self.max_z = z

		self.active.add((x, y, z))

	def print(self):
		active = self.active
		if not active:
			return

		zlo, zhi = self.min_z, self.max_z + 1
		ylo, yhi = self.min_y, self.max_y + 1
		xlo, xhi = self.min_x, self.max_x + 1

		for z in range(zlo, zhi):
			print('z={}'.format(z))
			for y in range(ylo, yhi):
				print(''.join(['#' if (x, y, z) in active else '.'
					for x in range(xlo, xhi)]))
			print()

	def play(self):
		active = self.active
		if not active:
			return self

		zlo, zhi = self.min_z - 1, self.max_z + 2
		ylo, yhi = self.min_y - 1, self.max_y + 2
		xlo, xhi = self.min_x - 1, self.max_x + 2

		new_state = State()

		for z in range(zlo, zhi):
			for y in range(ylo, yhi):
				for x in range(xlo, xhi):
					# Note that the current cell is included in this neighbor count
					n = sum([(i, j, k) in active
						for k in range(z - 1, z + 2)
						for j in range(y - 1, y + 2)
						for i in range(x - 1, x + 2)])
					if n == 3 or n == 4 and (x, y, z) in active:
						new_state.add(x, y, z)
		return new_state

def main():
	state = State()

	for y, line in enumerate(sys.stdin):
		for x, c in enumerate(line.rstrip()):
			if c == '#':
				state.add(x, y, 0)
			elif c != '.':
				err('Line {} contains characters other than "#" and "."!', y + 1)

	for cycle in range(6):
#		state.print()
		state = state.play()

#	state.print()
	print(len(state.active))

if __name__ == '__main__':
	main()
