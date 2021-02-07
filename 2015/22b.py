class Spell(object):
	def __init__(self, name, cost, effect, *, duration=0):
		self.name = name
		self.cost = cost
		self.effect = effect
		self.duration = duration
		self.timer = 0

	def cast(self, game):
		game.player_mana -= self.cost
		game.mana_used += self.cost
		if self.duration:
			self.timer = self.duration
		else:
			self.effect(game)

	def apply_effect(self, game):
		self.effect(game, self.timer)
		self.timer -= 1

def magic_missile_effect(game):
	game.boss_hp -= 4

def drain_effect(game):
	game.boss_hp -= 2
	game.player_hp += 2

def shield_effect(game, timer):
	game.player_armor = 0 if timer == 1 else 7

def poison_effect(game, timer):
	game.boss_hp -= 3

def recharge_effect(game, timer):
	game.player_mana += 101

class Game(object):
	def __init__(self, player_hp, player_mana, boss_hp, boss_damage, verbose=False):
		self.player_hp = player_hp
		self.player_mana = player_mana
		self.player_armor = 0
		self.boss_hp = boss_hp
		self.boss_damage = boss_damage
		self.verbose = verbose
		self.turn = 0
		self.mana_used = 0
		self.min_mana = None
		self.min_mana_spells = []
		self.spells_cast = []
		self.spells = (
			Spell('MagicMissile', 53, magic_missile_effect),
			Spell('Drain', 73, drain_effect),
			Spell('Shield', 113, shield_effect, duration=6),
			Spell('Poison', 173, poison_effect, duration=6),
			Spell('Recharge', 229, recharge_effect, duration=5),
		)

	def get_state(self):
		return [self.player_hp, self.player_mana, self.player_armor, self.boss_hp, self.mana_used,
			[(spell, spell.timer) for spell in self.spells if spell.duration]]

	def set_state(self, state):
		self.player_hp, self.player_mana, self.player_armor, self.boss_hp, self.mana_used, timers = state
		for spell, timer in timers:
			setattr(spell, 'timer', timer)

	def check_win(self):
		if self.boss_hp <= 0:
			self.log('Player wins')
			if self.min_mana is None:
				self.min_mana = self.mana_used
			elif self.mana_used > self.min_mana:
				return True
			elif self.mana_used < self.min_mana:
				self.min_mana = self.mana_used
				self.min_mana_spells.clear()
			self.min_mana_spells.append(self.spells_cast.copy())
			return True
		return False

	def log(self, *args):
		if not self.verbose: return
		print('{}Turn {} (player={}/{}/{}, boss={}):'.format('\t' * self.turn, self.turn + 1,
			self.player_hp, self.player_armor, self.player_mana, self.boss_hp), *args)

	def play(self):
#		state1 = self.get_state()
		self.player_hp -= 1
		if self.player_hp <= 0:
			self.log('Player loses')
#			self.set_state(state1)
			return
		for spell in self.spells:
			if spell.timer:
				self.log('Applying', spell.name)
				spell.apply_effect(self)
		if self.check_win():
#			self.set_state(state1)
			return

		mana = self.player_mana
		spells_cast = self.spells_cast
		state2 = self.get_state()

		for spell in self.spells:
			if spell.cost <= mana and spell.timer == 0:
				self.log('Casting', spell.name)
				spell.cast(self)
				spells_cast.append(spell.name)
				if self.check_win():
#					self.set_state(state1)
					spells_cast.pop()
					return
				if self.min_mana and self.mana_used > self.min_mana:
					self.log('Too expensive')
#					self.set_state(state1)
					spells_cast.pop()
					return

				for spell in self.spells:
					if spell.timer:
						self.log('Applying', spell.name)
						spell.apply_effect(self)
				if self.check_win():
#					self.set_state(state1)
					spells_cast.pop()
					return

				damage = max(self.boss_damage - self.player_armor, 1)
				self.log('Boss does', damage, 'damage')
				self.player_hp -= damage
				if self.player_hp > 0:
					self.turn += 1
					self.play()
					self.turn -= 1
				else:
					self.log('Player loses')
				self.set_state(state2)
				spells_cast.pop()

#		self.set_state(state1)

def main():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--boss-hp', type=int, default=55)
	parser.add_argument('--boss-damage', type=int, default=8)
	parser.add_argument('--mana', type=int, default=500)
	parser.add_argument('--player-hp', type=int, default=50)
	parser.add_argument('--verbose', '-v', action='store_true')
	args = parser.parse_args()
	game = Game(args.player_hp, args.mana, args.boss_hp, args.boss_damage, args.verbose)
	game.play()
	print(game.min_mana)
	for spells in game.min_mana_spells:
		print(', '.join(spells))

if __name__ == '__main__':
	main()
