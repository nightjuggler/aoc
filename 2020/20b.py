import sys
import re

def err(message, *args):
	sys.exit(message.format(*args))

class Tile(object):
	def set_borders(self):
		data = self.data
		k = len(data) - 1
		self.border_top = data[0]
		self.border_bottom = data[k]
		self.border_left = ''.join([row[0] for row in data])
		self.border_right = ''.join([row[k] for row in data])

	def connect_side(self, side, new_edge):
		old_edge = getattr(self, side)
		if old_edge:
			old_tile, old_side = old_edge
			new_tile, new_side = new_edge
			err('Cannot connect {} side of tile {} to {} side of tile {}: '
				'Already connected to {} side of tile {}!', side, self.id,
				new_side, new_tile.id,
				old_side, old_tile.id)
		setattr(self, side, new_edge)
		self.num_shared_edges += 1

	def update_sides(self, *args):
		for side, edge in args:
			if edge:
				other_tile, other_side = edge
				setattr(other_tile, other_side, (self, side))
			setattr(self, side, edge)

	def __init__(self, tile_id, tile_data):
		self.id = tile_id
		self.data = tile_data
		self.set_borders()
		self.top = None
		self.left = None
		self.right = None
		self.bottom = None
		self.num_shared_edges = 0

	def flip_horz(self):
		self.data = [row[::-1] for row in self.data]
		self.set_borders()
		self.update_sides(('right', self.left), ('left', self.right))

	def flip_vert(self):
		self.data = self.data[::-1]
		self.set_borders()
		self.update_sides(('top', self.bottom), ('bottom', self.top))

	def rot_180(self):
		self.data = [row[::-1] for row in self.data[::-1]]
		self.set_borders()
		self.update_sides(('top', self.bottom), ('right', self.left),
			('bottom', self.top), ('left', self.right))

	def rot_left(self):
		data = self.data
		self.data = [''.join([row[i] for row in data]) for i in range(len(data) - 1, -1, -1)]
		self.set_borders()
		self.update_sides(('top', self.right), ('right', self.bottom),
			('bottom', self.left), ('left', self.top))

	def rot_right(self):
		data = self.data[::-1]
		self.data = [''.join([row[i] for row in data]) for i in range(len(data))]
		self.set_borders()
		self.update_sides(('top', self.left), ('right', self.top),
			('bottom', self.right), ('left', self.bottom))

	def make_left(self, side, border):
		if side == 'top':
			self.rot_left()
		elif side == 'bottom':
			self.rot_right()
		elif side == 'right':
			self.rot_180()
		if self.border_left != border:
			self.flip_vert()

	def make_top(self, side, border):
		if side == 'right':
			self.rot_left()
		elif side == 'left':
			self.rot_right()
		elif side == 'bottom':
			self.rot_180()
		if self.border_top != border:
			self.flip_horz()

def arrange_tiles(tiles):
	corner_tiles = []
	for tile in tiles:
		n = tile.num_shared_edges
		if n == 2:
			corner_tiles.append(tile)
		elif n < 2 or n > 4:
			err('Tile {} has {} shared edges!', tile.id, n)

	if len(corner_tiles) != 4:
		err('Expected 4 corner tiles (got {})!', len(corner_tiles))

	product = 1
	for tile in corner_tiles:
		product *= int(tile.id)

	print(' * '.join([tile.id for tile in corner_tiles]), '=', product)

	tile = tile1 = corner_tiles[0]
	if tile.top:
		if tile.right:
			tile.rot_right()
		else:
			tile.rot_180()
	elif tile.left:
		tile.rot_left()

	tiles.clear()
	tiles.append(row := [])

	while True:
		row.append(tile)
		edge = tile.right
		if edge:
			border = tile.border_right
			tile, side = edge
			tile.make_left(side, border)
			continue

		edge = tile1.bottom
		if edge:
			border = tile1.border_bottom
			tile1, side = edge
			tile1.make_top(side, border)
			tile = tile1
			tiles.append(row := [])
			continue
		break

def check_arrangement(tiles, size):
	if len(tiles) != size or not all([len(row) == size for row in tiles]):
		err('The tiles are not arranged in a {0}x{0} square!', size)

	max_index = size - 1
	for y in range(size):
		for x in range(size):
			tile = tiles[y][x]
			if x == 0:
				assert tile.left is None
			else:
				tile2 = tiles[y][x - 1]
				assert tile.left == (tile2, 'right')
				assert tile.border_left == tile2.border_right
			if x == max_index:
				assert tile.right is None
			else:
				tile2 = tiles[y][x + 1]
				assert tile.right == (tile2, 'left')
				assert tile.border_right == tile2.border_left
			if y == 0:
				assert tile.top is None
			else:
				tile2 = tiles[y - 1][x]
				assert tile.top == (tile2, 'bottom')
				assert tile.border_top == tile2.border_bottom
			if y == max_index:
				assert tile.bottom is None
			else:
				tile2 = tiles[y + 1][x]
				assert tile.bottom == (tile2, 'top')
				assert tile.border_bottom == tile2.border_top

#	for row in tiles:
#		print(' '.join([tile.id for tile in row]))

def make_image1(tiles):
	image = []
	for row in tiles:
		a = [data[1:-1] for data in row[0].data[1:-1]]
		for tile in row[1:]:
			for i, data in enumerate(tile.data[1:-1]):
				a[i] += data[1:-1]
		image.extend(a)
	return image

def make_image2(tiles):
	k = len(tiles[0][0].data) - 1
	return [''.join([tile.data[i][1:k] for tile in row]) for row in tiles for i in range(1, k)]

def process_found(found, monster, roughness):
	n = len(found)
	print('Found {} sea monster{} @ {}{}'.format(n, '' if n == 1 else 's',
		'' if n == 1 else ', '.join(['({}, {})'.format(y, x) for y, x in found[:-1]]) +
			('' if n == 2 else ',') + ' and ', '({}, {})'.format(*found[-1])))

	s = set()
	for n, (y, x) in enumerate(found, start=1):
		m = set([(y + j, x + i) for j, row in enumerate(monster) for i in row])
		overlap = s & m
		if overlap:
			print('Monster {} overlaps previous monsters in {} places'.format(n, len(overlap)))
		s |= m

	print('Roughness is', roughness - len(s))

def match_monster(image, x, y, monster):
	for j, row in enumerate(monster):
		for i in row:
			if image[y + j][x + i] != '#':
				return False
	return True

def rot_right(image):
	image = image[::-1]
	return [''.join([row[i] for row in image]) for i in range(len(image))]

def find_monster(image, monster):
	monster = [[i for i, c in enumerate(row) if c == '#'] for row in monster]

	y_stop = len(image) - len(monster) + 1
	x_stop = len(image) - max([max(row) for row in monster if row])

	roughness = 0
	for row in image:
		for c in row:
			if c == '#':
				roughness += 1

	images = set()
	image = tuple(image)
	while True:
		found = []
		for y in range(y_stop):
			for x in range(x_stop):
				if match_monster(image, x, y, monster):
					found.append((y, x))
		if found:
			process_found(found, monster, roughness)
		images.add(image)
		image = tuple(rot_right(image))
		if image in images:
			image = image[::-1]
			if image in images:
				break
			print('Flipped vertically')
		else:
			print('Rotated right')

def connect_tiles(tiles):
	borders = {}
	num_inside_edges = 0

	for tile in tiles:
		for side in ('top', 'right', 'bottom', 'left'):
			border = getattr(tile, 'border_' + side)
			edge = (tile, side)
			edges = borders.get(border)
			if edges is None:
				edges = borders.get(border[::-1])
				if edges is None:
					borders[border] = [edge]
					continue
			if len(edges) != 1:
				err('The {} border of tile {} occurs more than twice!',
					side, tile.id)
			other_tile, other_side = other_edge = edges[0]
			if other_tile is tile:
				err('The {} border of tile {} is the same as its {} border!',
					side, tile.id, other_side)
			tile.connect_side(side, other_edge)
			other_tile.connect_side(other_side, edge)
			edges.append(edge)
			num_inside_edges += 1

	return len(borders), num_inside_edges

def read_tiles(input):
	pattern1 = re.compile('^Tile [1-9][0-9]{3}:$')
	pattern2 = re.compile('^[#.]+$')
	line_number = 0
	tiles = []

	for line in input:
		line_number += 1
		if not pattern1.match(line):
			err('Line {} doesn\'t match pattern!', line_number)
		tile_id = line[5:9]
		tile_data = []
		for line in input:
			line_number += 1
			line = line.rstrip()
			if not pattern2.match(line):
				if not line: break
				err('Line {} doesn\'t match pattern!', line_number)
			tile_data.append(line)

		if len(tile_data) != 10 or not all([len(row) == 10 for row in tile_data]):
			err('Tile {} is not 10x10!', tile_id)

		tiles.append(Tile(tile_id, tile_data))

	return tiles

def main():
	tiles = read_tiles(sys.stdin)

	num_tiles = len(tiles)
	size = int(num_tiles ** 0.5)
	if size * size != num_tiles:
		err('The number of tiles must be an integer squared!')

	num_edges, num_inside_edges = connect_tiles(tiles)

	expected_edges = size * (size + 1) * 2
	if num_edges != expected_edges:
		err('Expected {} edges (got {}) for {} tiles!', expected_edges, num_edges, num_tiles)

	expected_edges -= size * 4
	if num_inside_edges != expected_edges:
		err('Expected {} inside edges (got {}) for {} tiles!', expected_edges, num_inside_edges, num_tiles)

	if size > 1:
		arrange_tiles(tiles)

	check_arrangement(tiles, size)

	image = make_image1(tiles)
#	assert image == make_image2(tiles)

	find_monster(image, (
		'                  # ',
		'#    ##    ##    ###',
		' #  #  #  #  #  #   ',
		))

if __name__ == '__main__':
	main()
