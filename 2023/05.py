import sys

def read_input(f):
	line = f.readline()
	seeds = list(map(int, line.removeprefix('seeds:').split()))
	assert f.readline() == '\n'

	names = 'seed', 'soil', 'fertilizer', 'water', 'light', 'temperature', 'humidity', 'location'
	maps = []

	for i, line in enumerate(f):
		assert line == f'{names[i]}-to-{names[i+1]} map:\n'
		ranges = []
		for line in f:
			if line == '\n': break
			dst_start, src_start, range_len = map(int, line.split())
			ranges.append((src_start, src_start + range_len - 1, dst_start - src_start))
		maps.append(sorted(ranges))

	assert len(maps) == len(names)-1
	return seeds, maps

def part1(seeds, maps):
	def location(src):
		for ranges in maps:
			for src_start, src_end, delta in ranges:
				if src < src_start:
					break
				if src <= src_end:
					src += delta
					break
		return src
	return min(map(location, seeds))

def part2(seeds, maps):
	seeds = iter(seeds)
	sources = [(start, start + range_len - 1) for start, range_len in zip(seeds, seeds)]
	for ranges in maps:
		new_sources = []
		for start, end in sources:
			for src_start, src_end, delta in ranges:
				if start < src_start:
					if end < src_start:
						new_sources.append((start, end))
						break
					new_sources.append((start, src_start - 1))
					start = src_start
				if start <= src_end:
					if end <= src_end:
						new_sources.append((start + delta, end + delta))
						break
					new_sources.append((start + delta, src_end + delta))
					start = src_end + 1
			else:
				new_sources.append((start, end))
		sources = new_sources
	return min(start for start, end in sources)

def main():
	data = read_input(sys.stdin)
	print('Part 1:', part1(*data))
	print('Part 2:', part2(*data))
main()
