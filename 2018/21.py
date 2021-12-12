# Run the "disassembler" from day 19 on the puzzle input:
# > python3 19b.py < data/21.input > 21.py
# Then manually "decompile" to more readable Python and
# add the code to solve the puzzle.

def main():
	reg0_values = set()
	reg1_values = set()
	last_added = None
	reg1 = 0
	while True:
		if reg1 in reg1_values:
			print('Part 2:', last_added)
			break
		reg1_values.add(reg1)
		reg5 = reg1 | 65536
		reg1 = 8586263
		while True:
			reg1 += reg5 & 255
			reg1 &= 16777215
			reg1 *= 65899
			reg1 &= 16777215
			if reg5 < 256:
				# The original program halts here if reg1 == reg0
				if reg1 not in reg0_values:
					if not reg0_values:
						print('Part 1:', reg1)
					reg0_values.add(reg1)
					last_added = reg1
				break
			reg5 //= 256

if __name__ == '__main__':
	main()
