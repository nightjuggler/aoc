import argparse
from collections import deque
import hashlib

def solve(passcode, part2):
	md5 = hashlib.md5
	max_path_len = None

	q = deque()
	q.append((0, 0, ''))

	while q:
		x, y, path = q.popleft()
		if x == 3 == y:
			if part2:
				max_path_len = len(path)
				continue
			return path

		up, down, left, right = [x in 'bcdef' for x in
			md5(passcode + path.encode()).hexdigest()[:4]]

		if up    and y  : q.append((x, y-1, path+'U'))
		if down  and y<3: q.append((x, y+1, path+'D'))
		if left  and x  : q.append((x-1, y, path+'L'))
		if right and x<3: q.append((x+1, y, path+'R'))

	return max_path_len if part2 else None

def main():
	parser = argparse.ArgumentParser(allow_abbrev=False)
	parser.add_argument('passcode', nargs='?', default='qtetzkpl')
	parser.add_argument('-2', '--part2', action='store_true')
	args = parser.parse_args()

	print(solve(args.passcode.encode(), args.part2))

if __name__ == '__main__':
	main()
