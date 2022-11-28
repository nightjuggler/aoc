import re
import sys

def read_input():
	pattern = re.compile('^([a-z]+) \\(([1-9][0-9]*)\\)(?: -> ([a-z]+(?:, [a-z]+)*))?$')
	weights = {}
	above = {}
	for line_num, line in enumerate(sys.stdin, start=1):
		m = pattern.match(line)
		if not m:
			sys.exit(f'Line {line_num} doesn\'t match expected pattern!')
		name, weight, names = m.groups()
		assert name not in weights
		weights[name] = int(weight)
		if names:
			above[name] = names.split(', ')
	return weights, above

def tower_weight(node, weights, above):
	node_weight = weights[node]
	children = above.get(node)
	if not children:
		return node_weight
	child_weights = {}
	for child in children:
		w = tower_weight(child, weights, above)
		child_weights.setdefault(w, []).append(child)
		node_weight += w
	if len(child_weights) != 1:
		assert len(child_weights) == 2
		for w, children in child_weights.items():
			if len(children) == 1:
				child, = children
				del child_weights[w]
				delta = child_weights.popitem()[0] - w
				print('Part 2:', weights[child] + delta)
				return node_weight + delta
	return node_weight

def main():
	weights, above = read_input()

	below = set(weights)
	below.difference_update(*above.values())
	print('Part 1:', ', '.join(below))

	tower_weight(below.pop(), weights, above)

main()
