from operator import itemgetter
import re
import sys

def read_input(f):
	n = '([1-9][0-9]*|0)'
	pattern = re.compile(f'^/dev/grid/node-x{n}-y{n} +{n}T +{n}T +{n}T +{n}%$')

	nodes = []
	for line_num, line in enumerate(f, start=1):
		if m := pattern.match(line):
			node = tuple(map(int, m.groups()))
			x, y, size, used, avail, percent_used = node
			assert size == used + avail
			assert int(100 * used / size) == percent_used
			nodes.append(node)
		elif nodes or line_num > 2:
			sys.exit(f"Input line {line_num} doesn't match pattern!")
	return nodes

# Simple, but slower
def part1(nodes):
	get_used = itemgetter(3)
	get_avail = itemgetter(4)

	return sum(sum(used <= get_avail(n2) and n1 is not n2 for n2 in nodes)
		for n1 in nodes if (used := get_used(n1)))

# More complicated, but faster
def part1(nodes):
	get_used = itemgetter(3)
	get_avail_used = itemgetter(4, 3)

	used_sorted = sorted(filter(None, map(get_used, nodes)), reverse=True)
	avail_sorted = sorted(map(get_avail_used, nodes), reverse=True)

	if not used_sorted: return 0

	num_viable = 0
	len_used = len(used_sorted)
	used_sorted = enumerate(used_sorted)
	i, used = next(used_sorted)

	for avail, avail_used in avail_sorted:
		if used > avail:
			for i, used in used_sorted:
				if used <= avail: break
			else:
				break
		num_viable += len_used - i - int(0 < avail_used <= used)

	return num_viable

def main():
	nodes = read_input(sys.stdin)

	print(part1(nodes))

if __name__ == '__main__':
	main()
