import re
import sys

def lens_hash(s):
	v = 0
	for c in map(ord, s):
		v += c
		v *= 17
		v %= 256
	return v

def part2(steps):
	regex = re.compile('^([a-z]+)(?:-|=([1-9]))$')
	boxes = [[] for _ in range(256)]
	lenses = {}
	for step_num, step in enumerate(steps, start=1):
		m = regex.match(step)
		if not m:
			return f'Step {step_num} ({step}) doesn\'t match pattern!'
		lens, focal_len = m.groups()
		box = boxes[lens_hash(lens)]
		if focal_len:
			if lens not in box:
				box.append(lens)
			lenses[lens] = int(focal_len)
		elif lens in box:
			box.remove(lens)
	return sum(box_num * slot_num * lenses[lens]
		for box_num, box in enumerate(boxes, start=1)
		for slot_num, lens in enumerate(box, start=1))

def main():
	steps = sys.stdin.readline().rstrip().split(',')
	print('Part 1:', sum(map(lens_hash, steps)))
	print('Part 2:', part2(steps))
main()
