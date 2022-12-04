import argparse
import sys

def knot_hash(lengths):
	assert all(length <= 256 for length in lengths)
	marks = list(range(256))
	i = skip = 0
	for _ in range(64):
		for length in lengths:
			skip += 1
			j = (i + length - 1) % 256
			if i <= j:
				marks[i:j+1] = marks[j:i-1 if i else None:-1]
			else:
				m = marks[j::-1] + marks[:i-1:-1]
				marks[i:], marks[:j+1] = m[:256-i], m[256-i:]
			i = (j + skip) % 256
	result = []
	for i in range(0, 256, 16):
		output = 0
		for n in marks[i:i+16]:
			output ^= n
		result.extend(bool(output & 1<<(7-i)) for i in range(8))
	return result

def count_groups(hashes):
	next_group = 2
	merged_groups = {}
	def reduce(g):
		while g in merged_groups:
			g = merged_groups[g]
		return g
	prev_row = [0] * 128
	for row in hashes:
		assert len(row) == 128
		prev_col = 0
		for x, (col, above) in enumerate(zip(row, prev_row)):
			if not col:
				prev_col = 0
			elif prev_col:
				if above and (above := reduce(above)) != (prev_col := reduce(prev_col)):
					if above < prev_col:
						prev_col, above = above, prev_col
					merged_groups[above] = prev_col
				row[x] = prev_col
			elif above:
				row[x] = prev_col = above
			else:
				row[x] = prev_col = next_group
				next_group += 1
		prev_row = row
#	for row in hashes[:16]:
#		print(' '.join([format(reduce(col), '3') if col else '...' for col in row[:16]]))
	return next_group - 2 - len(merged_groups)

def main():
	parser = argparse.ArgumentParser(allow_abbrev=False)
	parser.add_argument('key', nargs='?', default='oundnydw')
	args = parser.parse_args()

	key = list(map(ord, args.key))
	key.append(ord('-'))

	hashes = []
	for row in range(128):
		lengths = key.copy()
		lengths.extend(map(ord, str(row)))
		lengths.extend([17, 31, 73, 47, 23])
		hashes.append(knot_hash(lengths))

	print('Part 1:', sum(map(sum, hashes)))
	print('Part 2:', count_groups(hashes))

main()
