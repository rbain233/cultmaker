import os
#import pickle
import cPickle as pickle
from Interface import * #Do it like this to avoid aggravation?
from person import Person
from cult import Cult, Doctrine, doctrine_list
from datetime import date, timedelta
from merch import *

"""Game object
	Purpose includes loading and saving game, 
	running the main event loop,
	setup,
	starting new game,
	and quitting. 
"""

class Game:
	def __init__(self):
		#This is called on program startup.
		self.filepath = "C:/lab/cultmaker/savedgames"
		self.cult = False
		#self.enemies = False //pointed to by cult?
		#self.government = False
		self.interface = Interface()
		pass
		
	def new_game(self):
		print "starting new game"
		#Do all the stuff involved with starting a cult here.
		print '"In a cult, there is someone at the top who knows the whole thing is a scam.'
		print 'In a religion, that person is dead. - Anonymous"'
		print
		print "You have had a revelation."
		print "Maybe it was contact with the Space Brothers."
		print "Maybe it was a message from Jesus."
		print "Perhaps it was a spontaneous upwelling from the Collective Subconscious."
		print "Maybe it was that there's a lot of gullible people out there with money."
		print "Whatever it was, you have decided to start your own cult!"
		print "So, tell us a bit about yourself."
		leader = Person()
		leader.name = ''
		while len(leader.name) == 0:
			print "What is your name?"
			leader.name = raw_input()

		b_year = self.interface.numberPrompt("What year were you born in?", 1900, date.today().year - 15)
		b_month = self.interface.numberPrompt("What month were you born in?", 1, 12)
		leader.birthday = date(b_year, b_month, 1)
		
		leader.rank = Person.RANK_LEADER
		leader.skills['recruit'] = 25  #You're better at it than average.
		leader.skills['doctrine'] = 25  #You wrote it.

		cult = Cult()
		cult.membership = [leader]
		cult.fame = 0
		cult.popularity = 0
		cult.wealth = 1000
		cult.doctrine = 10
		cult.weirdness = 0
		cult.leader = leader

		doctrine_choices = []
		for d in doctrine_list:
			doctrine_choices.append((d, d.name))
		doctrine_choices.append((False, "Nothing but my own delusions"))
		
		d_choice = self.interface.numbermenu("What sort of cult are you starting, %s?" % leader.name, doctrine_choices, 0)
		
		if (d_choice):
			cult.doctrines.append(d_choice)
		
		print "What is the name of your cult?"
		cult.name = ''
		while len(cult.name) == 0:
			cult.name = raw_input()

		f_choice = self.interface.numbermenu("Do you actually believe this stuff?", ((10, "No. It's just a scam."), (40, "I... think so?"), (70, "Yes. This is THE TRUTH!")))
		leader.fanaticism = f_choice
		if f_choice == 10:
			print "How cynical of you."
		elif f_choice == 40:
			print "How openminded of you."
		else: 
			print "How certain of you."
		
		leader.joined_date = date.today().replace(day=1)
		cult.founding_date = date.today().replace(day=1) #get things started.
		cult.current_date = date.today().replace(day=1)
		
		self.cult = cult
		
		self.main_loop()
		pass
	
	def load_game(self):
		print "loading game"
		os.chdir(self.filepath)
		#get list of files
		saved_game_list = os.listdir(self.filepath)
		menu_list = []
		for game_name in saved_game_list:
			menu_list.append((game_name, game_name))
		if len(saved_game_list) > 0:
			filename = self.interface.numbermenu("Which file?", menu_list, 1)
			print "File chosen: " + filename
			if filename != 0:
				print "load file"
				f = open( filename, "rb" )
				self.cult = pickle.load( f )
				self.main_loop()
			else:
				pass
		else:
			pass	
		
	def save_game(self):
		print "saving game"
		os.chdir(self.filepath)
		print "File name:"
		filename = raw_input()
		f = open( filename + ".p", "wb" )
		pickle.dump( self.cult,  f)
		f.close()
		pass
	
	def quit_game(self):
		#note: quits CURRENT game, goes back to title screen.
		print "quitting cult"
		pass
	
	def exit_game(self):
		#Note: totally done, shut everything down and go back to the command line.
		print "exiting game"
		pass
		
	def title_screen_loop(self):
		print "CULT LEADER"
		print ""
		action = False
		while action != 3:
			action = self.interface.numbermenu("Shall we begin?", ((1, "New Cult"),(2, "Load Cult"),(3, "Quit")), 0)
			if action == 1:
				self.new_game()
			if action == 2:
				self.load_game()
			#And if it's #3, we're done.
		self.exit_game()
		print "Be Seeing You."
		pass
		
		
	def assignLeaderMenu(self):
		#get options for Leader's actions.
		#Unlike the minion options, this one doesn't loop, since there's only one Leader.
		#It only loops to deal with full 'options'.
		sub_action = ""
		if self.cult.leader.department:
			print "You are currently doing: " + self.cult.leader.department.name + "."
		else:
			print "You are currently doing nothing."
		while sub_action != 'done':
			sub_action_list = self.cult.getJobs("leader")
			sub_action = self.interface.numbermenu("What will you do?", sub_action_list, 0)
			#Use sub action to assign the leader to a labor pool.
			if sub_action == 'full':
				print "That already has the maximum people. Reassign someone if you want to join."
				continue
			#Otherwise, add the leader to that labor-pool
			if self.cult.leader.department:
				self.cult.leader.department.removePerson(self.cult.leader)
			self.cult.assignLabor(sub_action, [self.cult.leader])
			print "You are now working on " + self.cult.leader.department.getName()
			return
	
	def assignCultistsMenu(self):
		"""This one will be a bit more complex - each labor pool can have a variable number of cultists assigned to it, and some require cultists of specific rank or higher."""
		sub_action = ""
		while sub_action != 'done':
			print "%d unassigned cultists ready." % len(self.cult.getUnassignedLabor())
			max_rank = "recruit"
			if self.cult.getInnerCircle():
				max_rank = "inner"
			elif self.cult.getOuterCircle():
				max_rank = "outer"
			sub_action_list = self.cult.getJobs(max_rank)
			if sub_action_list:
				sub_action = self.interface.numbermenu("Which job are you allocating cultists to?", sub_action_list, 0)
				if sub_action == 'done':
					break
				else: #it's a labor pool.
					#TODO: Remove the leader (if present) from this procedure's effects?
					dept = self.cult.departments[sub_action]
					unassigned_labor = self.cult.getUnassignedLabor(dept.minimum_rank)
					leader_here = self.cult.leader.department == sub_action
					if dept.max_people != 'unlimited':
						max_str = "(Max %d)"
						max_num = min(dept.max_people, len(dept.people) + len(unassigned_labor))
					else:
						max_str = ""
						max_num = len(dept.people) + len(unassigned_labor)
					if leader_here:
						is_leader = " (one of whom is you)"
					else:
						is_leader = ""
					print "%s has %d people already assigned to it%s. There are %d qualified cultists remaining to assign. %s" % (dept.name, len(dept.people), is_leader, len(unassigned_labor), max_str)
					assignment = self.interface.numberPrompt("How many cultists should work on this?", 0, max_num)
					if assignment > len(dept.people): #add more
						diff = assignment - len(dept.people)
						t = unassigned_labor[0:diff]
						for cultist in t:
							dept.addPerson(cultist)
						print "%d added." % diff
					elif assignment < len(dept.people): #Remove some.
						diff = len(dept.people) - assignment
						t = dept.people[0:diff]
						for cultist in t:
							dept.removePerson(cultist)
							if cultist.rank == 'leader':
								print "(Leader has been removed from this team. Re-assign the leader from the main menu.)"
						print "%d removed." % diff
					#else they're equal, and all is well.
				
			else:
				sub_action = 'done'
				break;

		pass
	
	def buyStuffMenu(self):
		action = ""
		while action != 'done':
			action_list = []
			for merch in merch_list:
				if merch.meetsPrereq(self.cult):
					if not self.cult.supplies.has_key(merch):
						qty = ""
					else:
						qty = "(%d in stock)" % self.cult.supplies[merch]
					
					action_list.append((merch, "%s - $%d each %s" % (merch.name, merch.unit_cost, qty)))
			action_list.append(("done", "Done"))
			action = self.interface.numbermenu("What do you want to buy?", action_list, 0)
			if action != 'done':
				#How much do they cost each, and how much money does the cult have?
				can_buy = self.cult.funds / action.unit_cost #rounds down automatically.
				#How many?
				if can_buy > 0:
					qty = self.interface.numberPrompt("How many units?", 0, can_buy)
					if qty > 0:
						self.cult.funds -= qty * action.unit_cost
						if not self.cult.supplies.has_key(action.internal_name):
							self.cult.supplies[action.internal_name] = qty
						else:
							self.cult.supplies[action.internal_name] += qty 
						#Note: I don't think this will need to track the items...
						print "%d %s purchased. %s has $%d remaining." % (qty, action.name, self.cult.name, self.cult.funds)
				else:
					print "We don't have enough funds to afford it."
		
	def main_loop(self):
		#events happen here.
		#when a game is running
		#give list of available commands.
		print "main loop (under construction)"
		#TODO: Move all the menu stuff into Interface?  Or at least other functions.
		while (True):
			print self.cult.current_date.strftime("%B %Y")
			print "cult membership: %d." % len(self.cult.membership)
		
			action_list = []
			action_list = self.cult.getActionList()
			#figure out what can be done, here.
			action_list.append(("save", "Save game")) #can always do these...
			action_list.append(("quit", "Quit to main menu"))
			action = False
			while action not in ("done", "quit"):
				action = self.interface.numbermenu("What will you do?", action_list, 0)
				if action == "save":
					self.save_game()
				if action == "assign_leader":
					self.assignLeaderMenu()
				if action == "assign_cultists":
					self.assignCultistsMenu()
				if action == "buy_stuff":
					self.buyStuffMenu()
		
			if action != "quit":
				#do all actions.
				print "Advance month."
				one_month = timedelta(days=32)
				next_month = self.cult.current_date + one_month
				next_month.replace(day=1)
				self.cult.current_date = next_month
				print "Monthly random events" #TODO
				print "Enemies' actions" #TODO
				print "Finance report - income, upkeep, spending"
				print self.cult.finances()
				print "Loyalty checks & other internal stuff" 
				print self.cult.membershipMonthlyChecks()
				print "Do all labor"
				print self.cult.doJobs()
				
			else:
				print "quitting"
				break #out of this loop, back to title screen.

game = Game()
game.title_screen_loop()