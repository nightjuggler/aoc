def rowcol(arg):
	arg = int(arg)
	if arg <= 0:
		raise ValueError
	return arg

def main():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('row', type=rowcol)
	parser.add_argument('column', type=rowcol)
	args = parser.parse_args()

	r = args.row
	c = args.column

	r1 = 1 + r * (r - 1) // 2
	rc = r1 + c * (c - 1) // 2 + r * (c - 1)

	code = 20151125
	for i in range(1, rc):
		code = code * 252533 % 33554393

	print('Row {}, column {} has code #{} = {}'.format(r, c, rc, code))

if __name__ == '__main__':
	main()
