import sys
import re

def err(message, *args):
	sys.exit(message.format(*args))

def setmem(mem, addr, floating_bits, value):
	mem[addr] = value

	for bits in range(1, 1 << len(floating_bits)):
		mask = 0
		for i, x in enumerate(floating_bits):
			mask |= ((bits >> i) & 1) << x
		mem[addr | mask] = value

def main():
	mask_pattern = re.compile('mask = ([01X]{36})$')
	mem_pattern = re.compile('mem\\[(0|[1-9][0-9]*)\\] = (0|[1-9][0-9]*)$')
	line_number = 0
	set_mask = 0
	unset_mask = 0
	floating_bits = []
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
			setmem(mem, (addr | set_mask) & unset_mask, floating_bits, value)
			continue
		m = mask_pattern.match(line)
		if m:
			set_mask = 0
			unset_mask = 0
			floating_bits.clear()
			for i, x in enumerate(m.group(1)):
				if x == 'X':
					floating_bits.append(35 - i)
				else:
					unset_mask |= 1 << (35 - i)
					if x == '1':
						set_mask |= 1 << (35 - i)
			continue
		err('Invalid operation on line {}!', line_number)

	print(sum(mem.values()))

if __name__ == '__main__':
	main()
