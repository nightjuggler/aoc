import argparse
import hashlib

def solve(salt, stretch):
	new_md5 = hashlib.md5
	candidates = {c: [] for c in '0123456789abcdef'}
	keys = []
	got_keys = False
	done = False
	i = -1
	while not done:
		i += 1
		hash = new_md5(salt + str(i).encode('ascii')).hexdigest()
		if stretch:
			for _ in range(2016):
				hash = new_md5(hash.encode('ascii')).hexdigest()
		triple = got_keys
		prev = None
		count = 0
		for c in hash:
			if c == prev:
				count += 1
				if count == 3:
					if not triple:
						triple = True
						candidates[c].append(i)
				elif count == 5 and (indices := candidates[c]):
					if indices[-1] == i:
						keys.extend(j for j in indices[:-1] if i - j <= 1000)
						indices[:-1] = []
					else:
						keys.extend(j for j in indices if i - j <= 1000)
						indices.clear()
					if len(keys) >= 64:
						got_keys = True
						keys.sort()
						k = keys[63]
						num_candidates = 0
						for indices in candidates.values():
							indices[:] = [j for j in indices if i - 1000 <= j < k]
							num_candidates += len(indices)
						if not num_candidates:
							done = True
			else:
				prev = c
				count = 1
	print(keys[63])

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('salt', nargs='?', default='yjdafjpo')
	parser.add_argument('-2', '--part2', action='store_true')
	args = parser.parse_args()

	solve(args.salt.encode('ascii'), args.part2)

if __name__ == '__main__':
	main()
