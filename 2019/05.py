import sys

def to_digits(number):
	digits = []
	while number:
		number, digit = divmod(number, 10)
		digits.append(digit)
	return digits

def run(program, system_id):
	program = program.copy()
	proglen = len(program)
	i = 0

	def op_add(a, b): return a + b
	def op_mul(a, b): return a * b
	def op_lss(a, b): return int(a < b)
	def op_eql(a, b): return int(a == b)

	def op_input():
		nonlocal i
		assert dlen == 1
		a = program[i+1]
		program[a] = system_id
		i += 2

	def op_output():
		nonlocal i
		assert dlen <= 3
		a = program[i+1]
		if dlen < 3:
			a = program[a]
		print(a)
		i += 2

	def op3(fn):
		nonlocal i
		assert dlen <= 4
		a, b, c = program[i+1:i+4]
		if dlen < 3 or not digits[2]:
			a = program[a]
		if dlen < 4:
			b = program[b]
		program[c] = fn(a, b)
		i += 4

	def jump(if_true):
		nonlocal i
		assert dlen <= 4
		a, b = program[i+1:i+3]
		if dlen < 3 or not digits[2]:
			a = program[a]
		if dlen < 4:
			b = program[b]
		if bool(a) is if_true:
			i = b
		else:
			i += 3

	while i < proglen:
		digits = to_digits(program[i])
		dlen = len(digits)
		op = digits[0]
		if dlen > 1:
			op += digits[1] * 10
			if dlen > 2:
				assert digits[-1] == 1
				assert all([digit == 0 or digit == 1 for digit in digits[2:-1]])
		if   op == 1: op3(op_add)
		elif op == 2: op3(op_mul)
		elif op == 3: op_input()
		elif op == 4: op_output()
		elif op == 5: jump(True)
		elif op == 6: jump(False)
		elif op == 7: op3(op_lss)
		elif op == 8: op3(op_eql)
		elif op == 99:
			assert dlen == 2
			break
		else:
			print('Unknown opcode at position', i)
			break

def main():
	program = list(map(int, sys.stdin.readline().split(',')))
	print('---------- Part 1 ----------')
	run(program, 1)
	print('---------- Part 2 ----------')
	run(program, 5)

if __name__ == '__main__':
	main()
