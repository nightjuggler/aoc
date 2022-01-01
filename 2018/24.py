import re
import sys

class Army(object):
	def __init__(self, name):
		self.name = name
		self.groups = set()

class Group(object):
	def __init__(self, army, properties):
		units, hitpoints, reactions, damage, attack, initiative = properties

		self.army = army
		self.units = int(units)
		self.hitpoints = int(hitpoints)
		self.weaknesses = set()
		self.immunities = set()
		self.damage = int(damage)
		self.attack = attack
		self.initiative = int(initiative)

		if reactions:
			for reaction in reactions.split('; '):
				weak_or_immune, _, attacks = reaction.split(' ', 2)
				(self.weaknesses if weak_or_immune == 'weak'
					else self.immunities).update(attacks.split(', '))

		self.initial_units = self.units
		self.initial_damage = self.damage

		army.groups.add(self)
		self.number = len(army.groups)

def target_selection_key(group):
	return group.units * group.damage, group.initiative

def attack_key(group):
	return group.initiative

def read_input():
	number = '([1-9][0-9]*)'
	weakto = '(?:immune|weak) to [a-z]+(?:, [a-z]+)*'
	re1 = re.compile('^([A-Z][a-z]+(?: [A-Z][a-z]+)*):$')
	re2 = re.compile(f'^{number} units each with {number} hit points'
		f'(?: \\(({weakto}(?:; {weakto})?)\\))? with an attack that does '
		f'{number} ([a-z]+) damage at initiative {number}$')
	start = True
	armies = []
	for line_number, line in enumerate(sys.stdin, start=1):
		if start:
			m = re1.match(line)
			if not m:
				print(f'Syntax error on input line {line_number}!')
				return None
			armies.append(Army(m.group(1)))
			start=False
			continue
		m = re2.match(line)
		if not m:
			if not line.rstrip():
				start=True
				continue
			print(f'Syntax error on input line {line_number}!')
			return None
		Group(armies[-1], m.groups())
	return armies

def fight(army1, army2):
	all_groups = set()
	all_groups.update(army1.groups, army2.groups)

	army1.available = army1.groups.copy()
	army2.available = army2.groups.copy()
	attacking = set()

	for g1 in sorted(all_groups, key=target_selection_key, reverse=True):
		available = g1.army.enemy.available
		if not available:
			continue
		available_info = [(
			0 if g1.attack in g2.immunities else
			2 if g1.attack in g2.weaknesses else 1,
			g2.units * g2.damage,
			g2.initiative,
			g2) for g2 in available]
		available_info.sort(reverse=True)
		target = available_info[0]
		if not target[0]:
			continue
		g1.target = g2 = target[3]
		g1.target_damage = target[0] * g1.damage
		attacking.add(g1)
		available.remove(g2)
#		print(f'{g1.army.name} group {g1.number} targets {g2.army.name} group {g2.number}'
#			f' for {g1.target_damage * g1.units} damage')
	if not attacking:
		return False

	for g1 in sorted(attacking, key=attack_key, reverse=True):
		if not g1.units:
			continue
		g2 = g1.target
		killed = min(g2.units, g1.target_damage * g1.units // g2.hitpoints)
		g2.units -= killed
#		print(f'{g1.army.name} group {g1.number} attacks {g2.army.name} group {g2.number},'
#			f' killing {killed} units')
		if not g2.units:
			g2.army.groups.remove(g2)
	return True

def war(army1, army2, prefix):
	while army1.groups and army2.groups:
		if not fight(army1, army2):
			print(f'{prefix}: Stalemate, no winner!')
			assert all([g1.attack in g2.immunities
				for g1 in army1.groups
				for g2 in army2.groups])
			assert all([g2.attack in g1.immunities
				for g2 in army2.groups
				for g1 in army1.groups])
			return None, None

	winner = army1 if army1.groups else army2
	units = sum([g.units for g in winner.groups])
	print(f'{prefix}: {winner.name} wins with {units} units remaining')
	return winner, units

def get_max_boost(*armies):
	table, units, hitpoints, power = [], [], [], []
	for army in armies:
		table.append([army.name])
		units.append(sum([g.units for g in army.groups]))
		power.append(sum([g.units * g.damage for g in army.groups]))
		hitpoints.append(sum([g.units * g.hitpoints for g in army.groups]))

	for row, *values in zip(table, units, power, hitpoints):
		row.extend([format(value, ',') for value in values])

	table.insert(0, ['', 'Units', 'Power', 'Hitpoints'])

	specs = ['>{}'.format(max(map(len, column))) for column in zip(*table)]

	for row in table:
		print(' | '.join(map(format, row, specs)))

	return (hitpoints[1] - power[0]) // units[0] + 1

def main():
	armies = read_input()
	if not armies or len(armies) != 2:
		print(f'There must be exactly two armies!')
		return

	army1, army2 = armies
	army2.enemy, army1.enemy = army1, army2

	army1.initial_groups = army1.groups.copy()
	army2.initial_groups = army2.groups.copy()

	if army1.name != 'Immune System':
		army1, army2 = army2, army1

	min_boost = 1
	max_boost = get_max_boost(army1, army2)

	war(army1, army2, 'Part 1')

	answer = None
	while min_boost <= max_boost:
		boost = (min_boost + max_boost) // 2

		army1.groups = army1.initial_groups.copy()
		army2.groups = army2.initial_groups.copy()
		for g in army1.groups:
			g.units = g.initial_units
			g.damage = g.initial_damage + boost
		for g in army2.groups:
			g.units = g.initial_units

		winner, units = war(army1, army2, f'boost = {boost}')
		if winner is army1:
			max_boost = boost - 1
			answer = boost, units
		else:
			min_boost = boost + 1
	if answer:
		boost, units = answer
		print(f'Part 2: With boost = {boost}, {army1.name} wins with {units} units remaining')

if __name__ == '__main__':
	main()
