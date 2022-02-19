import sys

# Usage: python3 12-to-py.py < data/12.input | python3

# >>> TIMEFMT="%*E seconds"
# >>> time (python3 12-to-py.py < data/12.input | python3)
# Part 1: 318007
# Part 2: 9227661
# 0.049 seconds

# Note: See zshmisc(1) for the zsh time command and zshparam(1) for TIMEFMT

class Stmt(object): pass

def rollup_loop(self, jump_target):
	arg = self.arg
	prev1 = self.prev
	if not (prev1.op == 'dec' and prev1.arg == arg):
		return False

	prev2 = prev1.prev
	if not (prev2 is jump_target and prev2.op == 'inc' and prev2.arg != arg):
		return False

	prev3 = prev2.prev
	if prev3 and prev3.op == 'cpy' and prev3.arg == arg:
		arg = prev3.arg2
		prev3.op = None

	if prev2.arg2 == '1':
		prev2.arg2 = arg
	else:
		prev2.arg2 += ' * ' + arg
	prev2.code = f'{prev2.arg} += {prev2.arg2}'

	prev1.op = None # Skip decrement of loop arg
	prev2.next = self
	self.prev = prev2

	next = self.next
	if next and next.op == 'cpy' and next.arg == self.arg:
		self.op = None
	else:
		self.op = 'cpy'
		self.arg2 = '0'
		self.code = f'{self.arg} = 0'
	return True

def decompile_jump(code):
	next_block = 1
	loop_starts = set()

	def indent(i, j):
		nonlocal next_block
		for stmt in code[i:j]:
			stmt.depth += 1
			stmt.block = next_block
		next_block += 1

	def decompile_if(i, self):
		offset = self.arg2
		assert offset > 1
		if offset == 2 and (next := self.next).op == 'jnz' and next.arg == '1':
			offset = next.arg2
			assert offset > 1
			offset += 1
			next.op = None
			next = next.next
			self.next = next
			next.prev = self
			self.code = f'if {self.arg}:'
		else:
			self.code = f'if not {self.arg}:'

		indent(i+1, i+offset)

	def decompile_loop(i, self):
		j = i + self.arg2
		assert 0 <= j < i
		assert j not in loop_starts
		loop_starts.add(j)
		next = code[j]
		assert next.block == self.block

		if rollup_loop(self, next):
			return

		self.code = f'if not {self.arg}: break'

		# Insert "while True:" before jump target
		stmt = Stmt()
		stmt.op = 'loop'
		stmt.depth = self.depth
		stmt.block = self.block
		stmt.code = 'while True:'
		stmt.next = next
		stmt.prev = prev = next.prev

		assert prev # TO-DO: Set head if prev is None
		next.prev = stmt
		prev.next = stmt
		indent(j, i+1)

	for i, stmt in enumerate(code):
		if stmt.op == 'jnz':
			if stmt.arg2 > 0:
				decompile_if(i, stmt)
			else:
				decompile_loop(i, stmt)

def read_input():
	code = []
	for i, line in enumerate(sys.stdin):
		stmt = Stmt()
		stmt.depth = 0
		stmt.block = 0
		code.append(stmt)

		op, *args = line.split()
		stmt.op = op

		if op == 'cpy':
			y, x = args
			stmt.arg = x
			stmt.arg2 = y
			stmt.code = f'{x} = {y}'
		elif op == 'dec':
			x, = args
			stmt.arg = x
			stmt.code = f'{x} -= 1'
		elif op == 'inc':
			x, = args
			stmt.arg = x
			stmt.arg2 = '1'
			stmt.code = f'{x} += 1'
		elif op == 'jnz':
			x, y = args
			stmt.arg = x
			stmt.arg2 = int(y)
		else:
			sys.exit(f'Unknown instruction on line {i+1}!')
	return code

def main():
	code = read_input()
	head = None
	tail = None
	for stmt in code:
		stmt.prev = tail
		stmt.next = None
		if head:
			tail.next = stmt
		else:
			head = stmt
		tail = stmt

	decompile_jump(code)

	print('def solve(c):')
	stmt = head
	while stmt:
		if stmt.op:
			print('\t' * (stmt.depth + 1), stmt.code, sep='')
		stmt = stmt.next
	print('\treturn a')
	print("print('Part 1:', solve(0))")
	print("print('Part 2:', solve(1))")

if __name__ == '__main__':
	main()
