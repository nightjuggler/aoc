import math
import re
import sys

err = sys.exit

def read_input(f):
	n = '((?:-?[1-9][0-9]*)|0)'
	xyz = f'<{n},{n},{n}>'
	line_pattern = re.compile(f'^p={xyz}, v={xyz}, a={xyz}$')

	particles = []
	for n, line in enumerate(f):
		m = line_pattern.match(line)
		if not m:
			err(f'Line {n+1} doesn\'t match pattern!')
		particles.append(tuple(map(int, m.groups())))
	return particles

def part_one(particles):
	min_a = None
	closest = None

	for n, p in enumerate(particles):
		a = sum(map(abs, p[6:9]))
		if not closest or a < min_a:
			min_a = a
			closest = [n]
		elif a == min_a:
			closest.append(n)

	if not closest:
		return 'There are no particles!'
	if len(closest) > 1:
		return f'There are {len(closest)} particles with the same minimum acceleration ({min_a})!'
	return f'Particle {closest[0]} has the minimum acceleration ({min_a})'

def position(particle, i, t):
	p, v, a = particle[i::3]
	return p + v*t + a*t*(t+1)/2

def collide_at_time(p1, p2, i, t):
	if not t.is_integer():
		return None
	t = int(t)
	if t < 0:
		return None
	assert position(p1, i, t) == position(p2, i, t)
	return t if (i == 2 or position(p1, 2, t) == position(p2, 2, t) and
		(i == 1 or position(p1, 1, t) == position(p2, 1, t))) else None

def collide(particle1, particle2, i=0):
	# p, v, a = initial position, velocity, and acceleration
	# position at time t = p + v*t + a*t*(t+1)/2 = p + (v + a/2)*t + (a/2)*t*t

	# If two particles collide, then the positions must be equal at some time t:
	# p1 + (v1 + a1/2)*t + (a1/2)*t*t == p2 + (v2 + a2/2)*t + (a2/2)*t*t
	# (p1-p2) + (v1-v2 + (a1-a2)/2)*t + (a1-a2)/2*t*t == 0

	p1, v1, a1 = particle1[i::3]
	p2, v2, a2 = particle2[i::3]
	dp = p1-p2
	dv = v1-v2
	da = a1-a2
	if da:
		# If a = da/2, b = dv + da/2, and c = dp
		# Then a*t*t + b*t + c = 0
		# and t = (-b +- sqrt(b*b - 4*a*c))/(2*a)
		# Thus t = (-b +- sqrt(b*b - 2*da*dp))/da
		b = dv + da/2
		r = b*b - 2*da*dp
		if r < 0: return None
		r = math.sqrt(r)
		if r:
			t1 = collide_at_time(particle1, particle2, i, (-b + r)/da)
			t2 = collide_at_time(particle1, particle2, i, (-b - r)/da)
			return t1 if t2 is None or t1 is not None and t1 < t2 else t2
		return collide_at_time(particle1, particle2, i, -b/da)
	elif dv:
		# dp + dv*t = 0
		return collide_at_time(particle1, particle2, i, -dp/dv)
	elif dp:
		return None

	return 1 if i == 2 else collide(particle1, particle2, i+1)

def part_two(particles):
	n = len(particles)
	collisions = []
	for i, particle in enumerate(particles):
		for j in range(i+1, n):
			t = collide(particle, particles[j])
			if t is not None:
				assert t > 0
				collisions.append((t, i, j))
	removed = set()
	to_be_removed = set()
	last_t = 0
	for t, i, j in sorted(collisions):
		if t != last_t:
			removed.update(to_be_removed)
			to_be_removed = set()
			last_t = t
		if i not in removed and j not in removed:
#			print(f'Particles {i} and {j} collide at time {t}')
			to_be_removed.add(i)
			to_be_removed.add(j)
	removed.update(to_be_removed)
	return n - len(removed)

def main():
	particles = read_input(sys.stdin)
	print('Part 1:', part_one(particles))
	print('Part 2:', part_two(particles))

if __name__ == '__main__':
	main()
