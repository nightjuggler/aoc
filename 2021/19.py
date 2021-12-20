from collections import deque
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
	m2 = list(zip(*m2))
	return tuple([tuple([sum([e1 * e2 for e1, e2 in zip(row, col)]) for col in m2]) for row in m1])

def get_rotations():
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
	return tuple([sum([me * pe for me, pe in zip(row, p)]) for row in m])

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
			rotated_set = set([rotate_point(rot, p) for p in b2_set])
			for b1, b1_set in beacons1:
				x_set = b1_set & rotated_set
				if len(x_set) >= 11:
					# b1 and b2 are the same beacon
					x2, y2, z2 = rotate_point(rot, b2)
					x1, y1, z1 = b1
					p = (x1 - x2, y1 - y2, z1 - z2)
					print(f'Scanner {s2} is at {p} relative to scanner {s1}')
					return p, rot
	return None

def main():
	scanners = read_input()
	if not scanners: return

	rotations = get_rotations()
	preprocess_scanners(scanners)

	overlap_map = [[] for i in scanners]

	num_scanners = len(scanners)
	for i in range(num_scanners-1):
		for j in range(i+1, num_scanners):
			overlap_ji = find_overlap(rotations, scanners, i, j)
			if overlap_ji:
				overlap_map[j].append((i, overlap_ji))
				overlap_ij = find_overlap(rotations, scanners, j, i)
				overlap_map[i].append((j, overlap_ij))

	beacon_positions = set([b for b, b_set in scanners[0]])
	scanner_positions = [(0, 0, 0)]

	for i in range(1, num_scanners):
		tried = [False] * num_scanners
		tried[i] = True
		success = False
		q = deque()
		for j, p_rot in overlap_map[i]:
			q.append((j, [p_rot]))
		while q:
			j, path = q.popleft()
			if tried[j]:
				continue
			tried[j] = True
			if j == 0:
				success = True
				break
			for j, p_rot in overlap_map[j]:
				new_path = path.copy()
				new_path.append(p_rot)
				q.append((j, new_path))
		if not success:
			print(f'Cannot find a way to map scanner {i} to scanner 0!')
			return
		p1, rot1 = path[0]
		for p2, rot2 in path[1:]:
			p1 = rotate_point(rot2, p1)
			x1, y1, z1 = p1
			x2, y2, z2 = p2
			p1 = (x1 + x2, y1 + y2, z1 + z2)
		print(f'Scanner {i} is at {p1} relative to scanner 0')
		scanner_positions.append(p1)
		for p1, b_set in scanners[i]:
			for p2, rot2 in path:
				p1 = rotate_point(rot2, p1)
				x1, y1, z1 = p1
				x2, y2, z2 = p2
				p1 = (x1 + x2, y1 + y2, z1 + z2)
			beacon_positions.add(p1)
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
