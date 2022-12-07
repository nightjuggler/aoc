import re
import sys

def err(n, s): sys.exit(f'Line {n}: {s}!')

def read_input():
	path = ''
	path_dirs = {}
	path_files = {}
	dir_pattern = re.compile('^dir ([a-z]+)$')
	file_pattern = re.compile('^([1-9][0-9]*) ([a-z]+(?:\\.[a-z]+)?)$')
	in_ls = False

	line_num = 0
	for line_num, line in enumerate(sys.stdin, start=1):
		line = line.rstrip()
		if line.startswith('$ cd '):
			if in_ls:
				in_ls = False
			d = line[5:]
			if d == '/':
				path = ''
			elif d == '..':
				if not path:
					err(line_num, 'cd .. in root directory')
				path = path[:path.rindex('/')]
			else:
				dirs = path_dirs.get(path)
				if dirs is None:
					err(line_num, 'cd to unknown directory')
				if d not in dirs:
					err(line_num, 'cd to nonexistent directory')
				path += '/' + d
		elif line == '$ ls':
			if path in path_dirs:
				err(line_num, 'Already listed ' + (path or '/'))
			path_dirs[path] = dirs = set()
			path_files[path] = files = []
			in_ls = True
		elif in_ls:
			if m := dir_pattern.match(line):
				dirs.add(m.group(1))
			elif m := file_pattern.match(line):
				files.append(int(m.group(1)))
			else:
				err(line_num, 'Expected cd, dir <name>, or <size> <name>')
		else:
			err(line_num, 'Expected cd or ls')

	if not path_dirs:
		err(line_num + 1, 'Expected ls in root directory')
	return path_dirs, path_files

def main():
	dir_sizes = []
	path_dirs, path_files = read_input()

	def get_dir_size(path):
		size = sum(path_files[path]) + sum(get_dir_size(path + '/' + d) for d in path_dirs[path])
		dir_sizes.append(size)
		return size

	used = get_dir_size('')
	print('Part 1:', sum(size for size in dir_sizes if size <= 100_000))
	unused = 70_000_000 - used
	needed = 30_000_000 - unused
	dir_sizes.sort()
	for size in dir_sizes:
		if size >= needed:
			print('Part 2:', size)
			break
main()
