import sys

def part1(stones, pmin, pmax):
	#
	# x = x0 + vx*t  =>  t = (x - x0) / vx
	# y = y0 + vy*t  =>  t = (y - y0) / vy
	#
	# y = y0 + vy*(x-x0)/vx
	# y = y0 + x*(vy/vx) - x0*(vy/vx)
	# y = x*(vy/vx) + y0 - x0*(vy/vx)
	#
	# x*(vy1/vx1) + y1 - x1*(vy1/vx1) = x*(vy2/vx2) + y2 - x2*(vy2/vx2)
	# x*(vy1/vx1 - vy2/vx2) = y2 - y1 + x1*(vy1/vx1) - x2*(vy2/vx2)
	#
	result = 0
	num_stones = len(stones)
	for i in range(num_stones):
		x1, y1, z1, vx1, vy1, vz1 = stones[i]
		for j in range(i+1, num_stones):
			x2, y2, z2, vx2, vy2, vz2 = stones[j]
			vyx1 = vy1/vx1
			vyx2 = vy2/vx2
			if vyx1 == vyx2: continue
			x = (y2 - y1 + x1*vyx1 - x2*vyx2) / (vyx1 - vyx2)
			y = y1 + (x-x1)*vyx1
			t1 = (x - x1) / vx1
			t2 = (x - x2) / vx2
			if (t1 > 0 and t2 > 0
				and pmin <= x <= pmax
				and pmin <= y <= pmax):
				result += 1
	return result

# ==== Part 2 Derivation ====
#
# If the rock's initial position is x,y,z, and the rock's velocity is vx,vy,vz,
# then for two arbitrary hailstones with initial positions x1,y1,z1 and x2,y2,z2
# and velocities vx1,vy1,vz1 and vx2,vy2,vz2, there will be times t1 and t2 when
# the rock collides with hailstones 1 and 2 respectively.
#
# x + vx*t1 = x1 + vx1*t1
# x = x1 + (vx1-vx)*t1
# y = y1 + (vy1-vy)*t1
# t1 = (y-y1)/(vy1-vy)
#
# y + vy*t2 = y2 + vy2*t2
# y = y2 + (vy2-vy)*t2
# x = x2 + (vx2-vx)*t2
# t2 = (x-x2)/(vx2-vx)
#
# Let dx1 = vx1-vx and dy1 = vy1-vy
# and dx2 = vx2-vx and dy2 = vy2-vy
#
# Then:
# x = x1 + dx1*t1 = x1 + dx1*(y-y1)/dy1
# y = y2 + dy2*t2 = y2 + dy2*(x-x2)/dx2
#
# Substitute y in the expression for x:
# x = x1 + dx1*(y2 + dy2*(x-x2)/dx2 - y1)/dy1
# x = x1 + dx1*((y2-y1) + dy2*(x-x2)/dx2)/dy1
#
# Multiply both sides by dy1:
# x*dy1 = x1*dy1 + dx1*(y2-y1) + dx1*dy2*(x-x2)/dx2
# Multiply both sides by dx2:
# x*dy1*dx2 = x1*dy1*dx2 + dx1*dx2*(y2-y1) + dx1*dy2*x - dx1*dy2*x2
#
# Solve for x:
# x*(dy1*dx2 - dx1*dy2) = x1*dy1*dx2 + dx1*dx2*(y2-y1) - dx1*dy2*x2
# x = (x1*dy1*dx2 - x2*dx1*dy2 + dx1*dx2*(y2-y1))/(dy1*dx2 - dx1*dy2)
#
# Now we can compute t1, t2, and y:
# t1 = (x-x1)/dx1
# t2 = (x-x2)/dx2
# y = y2 + dy2*t2
#
# And finally we can compute vz and z:
# z + vz*t1 = z1 + vz1*t1
# z + vz*t2 = z2 + vz2*t2
# z1 + vz1*t1 - vz*t1 = z2 + vz2*t2 - vz*t2
# vz*(t2-t1) = z2-z1 + vz2*t2 - vz1*t1
# vz = (z2-z1 + vz2*t2 - vz1*t1)/(t2-t1)
# z = z1 + vz1*t1 - vz*t1
#
def get_xyz(vx, vy, stone1, stone2):
	x1,y1,z1, vx1,vy1,vz1 = stone1
	x2,y2,z2, vx2,vy2,vz2 = stone2
	dx1 = vx1-vx
	dy1 = vy1-vy
	dx2 = vx2-vx
	dy2 = vy2-vy
	dxy = dy1*dx2 - dx1*dy2
	if not dxy: return 0
	if not dx2: return 0
	x = (x1*dy1*dx2 - x2*dx1*dy2 + dx1*dx2*(y2-y1))/dxy
	t2 = (x-x2)/dx2
	y = y2 + dy2*t2
	if dx1:
		t1 = (x-x1)/dx1
	elif dy1:
		t1 = (y-y1)/dy1
	else:
		return 0
	if t1 == t2:
		return None
	vz = (z2-z1 + vz2*t2 - vz1*t1)/(t2-t1)
	z = z1 + vz1*t1 - vz*t1
	result = vz, x, y, z
	int_result = int(vz), int(x), int(y), int(z)
	if result != int_result:
		return None
	return int_result

def part2(stones):
	stone1 = stones.pop()
	min_v, max_v = -1000, 1000
	for vx in range(min_v, max_v+1):
		for vy in range(min_v, max_v+1):
			result = None
			for stone2 in stones:
				result = get_xyz(vx, vy, stone1, stone2)
				if result or result is None: break
			if not result: continue
			#
			# Once we get an all-integer result, check that it works for all hailstones
			#
			vz, x, y, z = result
			for x2,y2,z2, vx2,vy2,vz2 in stones:
				t = (x-x2)/(vx2-vx) if vx != vx2 else (y-y2)/(vy2-vy)
				if (x+vx*t, y+vy*t, z+vz*t) != (x2+vx2*t, y2+vy2*t, z2+vz2*t): break
			else:
				return f'{x+y+z} (position={x},{y},{z}) (velocity={vx},{vy},{vz})'

def main(args):
	if len(args) > 1:
		filename = 'data/24.example'
		min_pos = 7
		max_pos = 27
	else:
		filename = 'data/24.input'
		min_pos = 200000000000000
		max_pos = 400000000000000

	stones = []
	with open(filename) as f:
		for line in f:
			position, velocity = line.split('@')
			stones.append((*map(int, position.split(',')), *map(int, velocity.split(','))))

	print('Part 1:', part1(stones, min_pos, max_pos))
	print('Part 2:', part2(stones))

main(sys.argv)
