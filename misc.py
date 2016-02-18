import random

def percentCheckBase(stat):
	roll = random.randint(1,100)
	if (roll == 1):
		return True;
	elif (roll == 100):
		return False
	else:
		return (roll <= stat)

def percentCheck(stat, difficulty = 'normal'):
	if difficulty == 'normal':
		return percentCheckBase(stat)
	elif difficulty == 'easy':
		return percentCheckBase(stat) or percentCheckBase(stat)
	elif difficulty == 'hard':
		return percentCheckBase(stat) and percentCheckBase(stat)
	else:
		#bad difficode, just do normal?  TODO: Log an error?
		return percentCheckBase(stat)
		
def percentCheckEasy(stat):
	return percentCheckBase(stat) or percentCheckBase(stat)

def percentCheckHard(stat):
	return percentCheckBase(stat) and percentCheckBase(stat)
	
def failPercentCheck(stat, difficulty = 'normal'):
	use_difficulty = 'normal'
	if difficulty == 'easy':
		use_difficulty = 'hard'
	elif difficulty == 'hard':
		use_difficulty = 'easy'
	return not percentCheck(stat, use_difficulty)
	
class Dice:
	def __init__(self, dice, sides, plus):
		self.dice = dice
		self.sides = sides
		self.plus = plus
	
	def roll(self):
		total = self.plus
		for ii in range(1, self.dice):
			total += random.randint(1, self.sides)
		return total
		
def nudgeTowardsAverage(current_value, target, steps = 4):
	if steps == 0: #This should probably cause an error message.
		return current_value
	diff = (current_value - target) / steps
	if diff == 0:
		return current_value
	if diff > 0:
		direction = -1
	if diff < 0:
		direction = 1
	diff = abs(diff)
	return current_value + (random.randint(0, diff) * direction)
	
	