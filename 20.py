import sys
import re

def err(message, *args):
	sys.exit(message.format(*args))

def main():
	pattern1 = re.compile('^Tile [1-9][0-9]{3}:$')
	pattern2 = re.compile('^[#.]{10}$')
	line_number = 0
	num_tiles = 0
	edges = {}

	for line in sys.stdin:
		line_number += 1
		if not pattern1.match(line):
			err('Line {} doesn\'t match pattern!', line_number)
		tile_id = int(line[5:9])
		num_tiles += 1
		tile_data = []
		for line in sys.stdin:
			line_number += 1
			if not pattern2.match(line):
				if line == '\n': break
				err('Line {} doesn\'t match pattern!', line_number)
			tile_data.append(line[:10])
		for edge in (
			tile_data[0], ''.join([row[9] for row in tile_data]),
			tile_data[9], ''.join([row[0] for row in tile_data]),
			):
			tiles = edges.get(edge)
			if tiles is None:
				tiles = edges.setdefault(edge[::-1], [])
			tiles.append(tile_id)

	size = int(num_tiles ** 0.5)
	if size * size != num_tiles:
		err('The number of tiles must be an integer squared!')

	num_edges = size * (size + 1) * 2
	if len(edges) != num_edges:
		err('Expected {} edges (got {}) for {} tiles!', num_edges, len(edges), num_tiles)

	outside_tiles = {}
	num_inside_edges = 0
	num_outside_edges = 0
	for edge, tiles in edges.items():
		if len(tiles) == 2:
			num_inside_edges += 1
		elif len(tiles) == 1:
			num_outside_edges += 1
			tile_id = tiles[0]
			outside_tiles[tile_id] = outside_tiles.get(tile_id, 0) + 1
		else:
			err('The edge "{}" is shared by more than 2 tiles!', edge)

	if num_outside_edges != size * 4:
		err('Expected {} outside edges (got {})!', size * 4, num_outside_edges)
	if num_inside_edges != num_edges - num_outside_edges:
		err('Expected {} inside edges (got {})!', num_edges - num_outside_edges, num_inside_edges)

	corner_tiles = []
	for tile_id, num_edges in outside_tiles.items():
		if num_edges == 2:
			corner_tiles.append(tile_id)
		elif num_edges != 1:
			err('Tile {} has more than 2 outside edges!', tile_id)

	if len(corner_tiles) != 4:
		err('Expected 4 corner tiles (got {})!', len(corner_tiles))

	a, b, c, d = corner_tiles
	print(a, '*', b, '*', c, '*', d, '=', a * b * c * d)

if __name__ == '__main__':
	main()
