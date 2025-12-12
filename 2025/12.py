import sys

def parse_shape(shape):
	index, *shape = shape.split()
	return int(index[:-1]), [[tile == '#' for tile in row] for row in shape]

def parse_region(region):
	size, qtys = region.split(':')
	width, height = size.split('x')
	return int(width), int(height), [int(qty) for qty in qtys.split()]

def main():
	*shapes, regions = sys.stdin.read().split('\n\n')
	shapes = [parse_shape(shape) for shape in shapes]
	regions = [parse_region(region) for region in regions.strip().split('\n')]

	assert all(shape[0] == i for i, shape in enumerate(shapes))
	shapes = [shape for i, shape in shapes]
	assert all(len(shape) == 3 and all(len(row) == 3 for row in shape) for shape in shapes)
	sizes = [sum(sum(row) for row in shape) for shape in shapes]

	fits = todo = 0
	for width, height, qtys in regions:
		if width*height < sum(qty*size for qty, size in zip(qtys, sizes)):
			# The shapes won't fit into the region even with clever tiling
			continue
		if sum(qtys) <= (width//3)*(height//3):
			# The shapes trivially fit into the region without any clever tiling
			fits += 1
		else:
			todo += 1 # Haha, maybe some day

	print(f'Part 1: {fits} (To-do: {todo})')
main()
