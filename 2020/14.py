import sys
import re

def err(message, *args):
	sys.exit(message.format(*args))

def main():
	mask_pattern = re.compile('mask = ([01X]{36})$')
	mem_pattern = re.compile('mem\\[(0|[1-9][0-9]*)\\] = (0|[1-9][0-9]*)$')
	line_number = 0
	set_mask = 0
	unset_mask = 0
	max_int = (1 << 36) - 1
	mem = {}

	for line in sys.stdin:
		line_number += 1
		m = mem_pattern.match(line)
		if m:
			if line_number == 1:
				err('The first operation must specify a bitmask!')
			addr, value = m.groups()
			addr, value = int(addr), int(value)
			if addr > max_int:
				err('The address on line {} is too large!', line_number)
			if value > max_int:
				err('The value on line {} is too large!', line_number)
			mem[addr] = (value | set_mask) & unset_mask
			continue
		m = mask_pattern.match(line)
		if m:
			set_mask = 0
			unset_mask = 0
			for i, x in enumerate(m.group(1)):
				if x != '0':
					unset_mask |= 1 << (35 - i)
					if x == '1':
						set_mask |= 1 << (35 - i)
			continue
		err('Invalid operation on line {}!', line_number)

	print(sum(mem.values()))

if __name__ == '__main__':
	main()
