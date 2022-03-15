from collections import deque
import operator
import re
import sys

def read_input():
	n = '(0|-?[1-9][0-9]*)'
	re1 = re.compile(f'^--- scanner {n} ---$')
	re2 = re.compile(f'^{n},{n},{n}$')
	scanners = []
	new_scanner = True
	for line_number, line in enumerate(sys.stdin, start=1):
		if new_scanner:
			m = re1.match(line)
			if not m:
				print(f'Input line {line_number}: Expected scanner header!')
				return None
			if int(m.group(1)) != len(scanners):
				print(f'Input line {line_number}: Unexpected scanner number!')
				return None
			scanners.append([])
			new_scanner = False
			continue
		m = re2.match(line)
		if not m:
			if not line.rstrip():
				new_scanner = True
				continue
			print(f'Input line {line_number}: Expected 3 comma-separated integers!')
			return None
		scanners[-1].append(tuple(map(int, m.groups())))
	return scanners

def multiply_matrices(m1, m2):
	mul = operator.mul
	m2 = list(zip(*m2))
	return tuple(tuple(sum(map(mul, row, col)) for col in m2) for row in m1)

def get_rotations():
	# cos(t), sin(t) for t in 0, 90, 180, and 270 degrees
	cos_sin = ((1, 0), (0, 1), (-1, 0), (0, -1))
	rotations = set()
	for zcos, zsin in cos_sin:
		z = ((zcos, -zsin, 0), (zsin, zcos, 0), (0, 0, 1))
		for ycos, ysin in cos_sin:
			y = ((ycos, 0, ysin), (0, 1, 0), (-ysin, 0, ycos))
			zy = multiply_matrices(z, y)
			for xcos, xsin in cos_sin:
				x = ((1, 0, 0), (0, xcos, -xsin), (0, xsin, xcos))
				rotations.add(multiply_matrices(zy, x))
	return rotations

def rotate_point(m, p):
	mul = operator.mul
	return tuple(sum(map(mul, row, p)) for row in m)

def preprocess_scanners(scanners):
	for i, beacons in enumerate(scanners):
		new_beacons = []
		for b1 in beacons:
			x1, y1, z1 = b1
			s = set()
			for b2 in beacons:
				if b1 is b2: continue
				x2, y2, z2 = b2
				s.add((x2 - x1, y2 - y1, z2 - z1))
			new_beacons.append((b1, s))
		scanners[i] = new_beacons

def find_overlap(rotations, scanners, s1, s2):
	beacons1 = scanners[s1]
	beacons2 = scanners[s2]
	for rot in rotations:
		for b2, b2_set in beacons2:
			rotated_set = set(rotate_point(rot, p) for p in b2_set)
			for b1, b1_set in beacons1:
				x_set = b1_set & rotated_set
				if len(x_set) >= 11:
					# b1 and b2 are the same beacon.
					# If p is the position of s2 relative to s1,
					# then since b2 is relative to s2, p + b2 = b1.
					# Thus p = b1 - b2
					x2, y2, z2 = rotate_point(rot, b2)
					x1, y1, z1 = b1
					p = (x1 - x2, y1 - y2, z1 - z2)
					print(f'Scanner {s2} is at {p} relative to scanner {s1}')
					return p, rot
	return None

def path_to_scanner0(i, overlap_map):
	tried = [False] * len(overlap_map)
	tried[i] = True
	q = deque()
	for j, overlap in overlap_map[i]:
		q.append((j, [overlap]))
	while q:
		j, path = q.popleft()
		if tried[j]:
			continue
		tried[j] = True
		if j == 0:
			return path
		for j, overlap in overlap_map[j]:
			new_path = path.copy()
			new_path.append(overlap)
			q.append((j, new_path))

	print(f'Cannot find a way to map scanner {i} to scanner 0!')
	return None

def follow_path(p1, path):
	for p2, rot2 in path:
		p1 = rotate_point(rot2, p1)
		x1, y1, z1 = p1
		x2, y2, z2 = p2
		p1 = (x1 + x2, y1 + y2, z1 + z2)
	return p1

def main():
	scanners = read_input()
	if not scanners: return

	rotations = get_rotations()
	preprocess_scanners(scanners)

	overlap_map = [[] for i in scanners]

	num_scanners = len(scanners)
	for i in range(num_scanners-1):
		for j in range(i+1, num_scanners):
			overlap = find_overlap(rotations, scanners, i, j)
			if overlap:
				overlap_map[j].append((i, overlap))
				overlap = find_overlap(rotations, scanners, j, i)
				overlap_map[i].append((j, overlap))

	beacon_positions = set(b for b, b_set in scanners[0])
	scanner_positions = [(0, 0, 0)]

	for i in range(1, num_scanners):
		path = path_to_scanner0(i, overlap_map)
		if not path:
			return
		p1 = follow_path(path[0][0], path[1:])
		print(f'Scanner {i} is at {p1} relative to scanner 0')
		scanner_positions.append(p1)
		for p1, b_set in scanners[i]:
			beacon_positions.add(follow_path(p1, path))
	print('Part 1:', len(beacon_positions))

	max_distance = 0
	for i in range(num_scanners-1):
		x1, y1, z1 = scanner_positions[i]
		for j in range(i+1, num_scanners):
			x2, y2, z2 = scanner_positions[j]
			d = abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)
			if d > max_distance:
				max_distance = d
	print('Part 2:', max_distance)

if __name__ == '__main__':
	main()
