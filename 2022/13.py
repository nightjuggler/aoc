import json
import sys

def compare(list1, list2):
	for a, b in zip(list1, list2):
		if isinstance(a, int):
			if isinstance(b, int):
				if a < b: return -1
				if a > b: return 1
				continue
			a = [a]
		elif isinstance(b, int):
			b = [b]
		if result := compare(a, b):
			return result
	a = len(list1)
	b = len(list2)
	if a < b: return -1
	if a > b: return 1
	return 0

class Packet(list):
	def __lt__(self, other): return compare(self, other) < 0
	def __le__(self, other): return compare(self, other) <= 0
	def __eq__(self, other): return compare(self, other) == 0
	def __ne__(self, other): return compare(self, other) != 0
	def __gt__(self, other): return compare(self, other) > 0
	def __ge__(self, other): return compare(self, other) >= 0

def err(line_num, message):
	sys.exit(f'Line {line_num}: {message}!')

def is_valid(p):
	return isinstance(p, list) and all(isinstance(a, int) or is_valid(a) for a in p)

def read_input():
	packets = []
	line_num = 0
	for line_num, line in enumerate(sys.stdin, start=1):
		if line_num % 3:
			try:
				packet = json.loads(line)
			except json.decoder.JSONDecodeError:
				packet = None
			if not is_valid(packet):
				err(line_num, 'Invalid packet')
			packets.append(Packet(packet))
		elif line.strip():
			err(line_num, 'Expected a blank line')
	if len(packets) % 2:
		err(line_num + 1, 'Expected an even number of packets')
	return packets

def part1(p):
	p = iter(p)
	return sum(i for i, (a, b) in enumerate(zip(p, p), start=1) if a < b)

def part2(p):
	p.append(a := Packet([[2]]))
	p.append(b := Packet([[6]]))
	p.sort()
	i = p.index(a) + 1
	j = p.index(b) + 1
	return f'{i} * {j} = {i*j}'

def main():
	packets = read_input()
	print('Part 1:', part1(packets))
	print('Part 2:', part2(packets))
main()
