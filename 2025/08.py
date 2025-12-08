import argparse
from math import dist, prod

def main():
	args = argparse.ArgumentParser(allow_abbrev=False)
	args.add_argument('-x', '--example', action='store_true')
	args = args.parse_args()

	num_conns, suffix = (10, 'example') if args.example else (1000, 'input')
	with open(f'data/08.{suffix}') as f:
		boxes = [tuple(map(int, line.split(','))) for line in f]
	num_boxes = len(boxes)
	distances = sorted((dist(boxes[i], boxes[j]), i, j)
		for i in range(num_boxes-1)
		for j in range(i+1, num_boxes))

	circuits = {}
	for i, (d, p, q) in enumerate(distances, start=1):
		if p in circuits:
			c = circuits[p]
			if q in circuits:
				cq = circuits[q]
				c |= cq
				for q in cq: circuits[q] = c
			else:
				c.add(q)
				circuits[q] = c
		elif q in circuits:
			c = circuits[q]
			c.add(p)
			circuits[p] = c
		else:
			circuits[p] = circuits[q] = c = {p, q}
		if i == num_conns:
			print('Part 1:', prod(sorted(map(len, set(map(frozenset, circuits.values()))),
				reverse=True)[:3]))
		if len(c) == num_boxes:
			print('Part 2:', boxes[p][0] * boxes[q][0])
			break
main()
