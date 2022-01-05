import sys

version_sum = 0

def op_sum(args):
	return sum(args)

def op_product(args):
	value = args[0]
	for x in args[1:]:
		value *= x
	return value

def op_min(args): return min(args)
def op_max(args): return max(args)

def op_greater_than(args):
	return 1 if args[0] > args[1] else 0

def op_less_than(args):
	return 1 if args[0] < args[1] else 0

def op_equal_to(args):
	return 1 if args[0] == args[1] else 0

ops = [
	op_sum,
	op_product,
	op_min,
	op_max,
	None,
	op_greater_than,
	op_less_than,
	op_equal_to,
]
op_names = [
	'sum',
	'product',
	'minimum',
	'maximum',
	None,
	'greater than',
	'less than',
	'equal to',
]

def parse_packet(b, i, depth):
	global version_sum
	packet_version = int(b[i:i+3], 2)
	version_sum += packet_version
	type_id = int(b[i+3:i+6], 2)
	i += 6
	if type_id == 4:
		number = []
		notdone = True
		while notdone:
			notdone = b[i] == '1'
			number.append(b[i+1:i+5])
			i += 5
		value = int(''.join(number), 2)
		print('\t'*depth, 'literal ', value, sep='')
		return value, i

	print('\t'*depth, 'operator: ', op_names[type_id], sep='')
	args = []
	if b[i] == '0':
		num_bits = int(b[i+1:i+16], 2)
		i += 16
		j = i + num_bits
		while i < j:
			value, i = parse_packet(b, i, depth+1)
			args.append(value)
	else:
		num_subpackets = int(b[i+1:i+12], 2)
		i += 12
		for n in range(num_subpackets):
			value, i = parse_packet(b, i, depth+1)
			args.append(value)

	return ops[type_id](args), i

def main():
	bitstr = ''.join([format(int(c, 16), '04b') for c in sys.stdin.readline().rstrip()])
	value, i = parse_packet(bitstr, 0, 0)
	print('Part 1: version sum =', version_sum)
	print('Part 2: expression value =', value)

if __name__ == '__main__':
	main()
