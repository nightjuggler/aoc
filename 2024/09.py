import sys

def part1(diskmap):
	pos = 0
	head = 0
	tail = len(diskmap) - 1
	if tail % 2: tail -= 1
	size = diskmap[tail]
	result = 0

	while head < tail:
		nextpos = pos + diskmap[head]
		result += head//2 * sum(range(pos, nextpos))
		pos = nextpos
		head += 1
		space = diskmap[head]
		while size <= space:
			nextpos = pos + size
			result += tail//2 * sum(range(pos, nextpos))
			pos = nextpos
			space -= size
			tail -= 2
			if head > tail: return result
			size = diskmap[tail]
		nextpos = pos + space
		result += tail//2 * sum(range(pos, nextpos))
		pos = nextpos
		size -= space
		head += 1
	if head == tail:
		result += tail//2 * sum(range(pos, pos + size))

	return result

def part2(diskmap):
	files = []
	space = [[] for size in range(10)]
	pos = 0
	is_file = True
	for size in diskmap:
		if is_file:
			files.append([pos, size])
		elif size:
			space[size].append(pos)
		pos += size
		is_file = not is_file

	for f in files[::-1]:
		fpos, fsize = f
		avail = [(space[size][0], size) for size in range(fsize, 10) if space[size]]
		if not avail: continue
		pos, size = min(avail)
		if fpos < pos: continue
		f[0] = pos
		del space[size][0]
		size -= fsize
		if not size: continue
		pos += fsize
		spaces = space[size]
		n = len(spaces)
		i = 0
		while i < n and pos > spaces[i]: i += 1
		spaces.insert(i, pos)

	return sum(i * sum(range(pos, pos + size)) for i, (pos, size) in enumerate(files))

def main():
	diskmap = list(map(int, sys.stdin.read().strip()))
	print('Part 1:', part1(diskmap))
	print('Part 2:', part2(diskmap))

main()
