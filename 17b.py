import sys

def err(message, *args):
	sys.exit(message.format(*args))

class State(object):
	def __init__(self):
		self.active = set()
		self.min_x = None
		self.max_x = None
		self.min_y = None
		self.max_y = None
		self.min_z = None
		self.max_z = None
		self.min_w = None
		self.max_w = None

	def add(self, x, y, z, w):
		if self.active:
			if   x < self.min_x: self.min_x = x
			elif x > self.max_x: self.max_x = x
			if   y < self.min_y: self.min_y = y
			elif y > self.max_y: self.max_y = y
			if   z < self.min_z: self.min_z = z
			elif z > self.max_z: self.max_z = z
			if   w < self.min_w: self.min_w = w
			elif w > self.max_w: self.max_w = w
		else:
			self.min_x = x
			self.max_x = x
			self.min_y = y
			self.max_y = y
			self.min_z = z
			self.max_z = z
			self.min_w = w
			self.max_w = w

		self.active.add((x, y, z, w))

	def print(self):
		wlo, whi = self.min_w, self.max_w + 1
		zlo, zhi = self.min_z, self.max_z + 1
		ylo, yhi = self.min_y, self.max_y + 1
		xlo, xhi = self.min_x, self.max_x + 1
		active = self.active
		for w in range(wlo, whi):
			for z in range(zlo, zhi):
				print('z={}, w={}'.format(z, w))
				for y in range(ylo, yhi):
					print(''.join(['#' if (x, y, z, w) in active else '.'
						for x in range(xlo, xhi)]))
				print()

	def play(self):
		new_state = State()

		wlo = self.min_w - 1
		whi = self.max_w + 2
		zlo = self.min_z - 1
		zhi = self.max_z + 2
		ylo = self.min_y - 1
		yhi = self.max_y + 2
		xlo = self.min_x - 1
		xhi = self.max_x + 2
		active = self.active

		for w in range(wlo, whi):
			for z in range(zlo, zhi):
				for y in range(ylo, yhi):
					for x in range(xlo, xhi):
						n = sum([(i, j, k, m) in active
							for m in range(w - 1, w + 2)
							for k in range(z - 1, z + 2)
							for j in range(y - 1, y + 2)
							for i in range(x - 1, x + 2)])
						if (x, y, z, w) in active:
							if n == 3 or n == 4:
								new_state.add(x, y, z, w)
						elif n == 3:
							new_state.add(x, y, z, w)
		return new_state

def main():
	state = State()

	for y, line in enumerate(sys.stdin):
		for x, c in enumerate(line.rstrip()):
			if c == '#':
				state.add(x, y, 0, 0)
			elif c != '.':
				err('Line {} contains characters other than "#" and "."!', y + 1)

	for cycle in range(6):
#		state.print()
		state = state.play()

#	state.print()
	print(len(state.active))

if __name__ == '__main__':
	main()
