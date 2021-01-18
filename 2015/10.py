def look_and_say(seq1):
	seq2 = []
	prev = seq1[0]
	reps = 0
	for n in seq1:
		if n == prev:
			reps += 1
		else:
			seq2.append(str(reps))
			seq2.append(prev)
			prev = n
			reps = 1
	seq2.append(str(reps))
	seq2.append(prev)
	return ''.join(seq2)

def main():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('seed', nargs='?', default='1321131112')
	parser.add_argument('-i', '--iterations', type=int, default=40)
	parser.add_argument('-v', '--verbose', action='store_true')
	args = parser.parse_args()

	seq = args.seed
	if not seq:
		print('Please specify an integer seed number!')
		return
	for c in seq:
		if c not in '1234567890':
			print('The seed must contain only decimal digits!')
			return

	for i in range(args.iterations):
		seq = look_and_say(seq)
		if args.verbose:
			print(seq)

	print(len(seq), 'digits')

if __name__ == '__main__':
	main()
