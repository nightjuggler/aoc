import sys

err = sys.exit

def main():
	lines = [{x: c for x, c in enumerate(line.rstrip()) if c != ' '} for line in sys.stdin]
	num_lines = len(lines)

	def get_path(x, y):
		return lines[y].get(x) if 0 <= y < num_lines else None

	y = 0
	line = lines[y]
	if len(line) != 1:
		err('Expected exactly one path element on the first line!')
	x = list(line)[0]
	c = line[x]
	if c != '|':
		err("Expected '|' on the first line!")
	dx = 0
	dy = 1
	letters = []
	steps = 1

	while True:
		x += dx
		y += dy
		c = get_path(x, y)
		if not c: break
		steps += 1
		if c == '|' or c == '-': continue
		if c == '+':
			last_xy = x-dx,y-dy
			next_xy = {(a,b) for a,b in ((x+1,y), (x,y+1), (x-1,y), (x,y-1)) if get_path(a,b)}
			next_xy.remove(last_xy)
			if len(next_xy) != 1:
				err(f'{last_xy} -> ({x},{y}) -> {next_xy}')
			nx, ny = next_xy.pop()
			if nx == x + dx:
				err(f'{last_xy} -> ({x},{y}) -> ({nx},{ny})')
			dx = nx - x
			dy = ny - y
		else:
			letters.append(c)

	print('Part 1:', ''.join(letters))
	print('Part 2:', steps)

if __name__ == '__main__':
	main()
