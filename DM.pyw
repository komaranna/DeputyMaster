#################################################################
#				Deputy (Dungeon) Master
#					by A.Komar
#			for Dungeons and Dragons 3.5
#				v. 2017-12-04
#################################################################
#################################################################
# This version scrapes a folder for all text files, and
# opens 1 window for each text file/monster.
#
# For more info, see the User's Manual:
# https://github.com/komaranna/DeputyMaster/blob/master/manual.pdf
#################################################################

import random # random number generators
# import GUI module, name is different for 2.x and 3.x
try:
    # for python 2.x
	from Tkinter import *
except ImportError:
    # for python 3.x
	from tkinter import * 
# these two are needed for file reading:
import glob
import sys


# Scrapes "folder" for text files,
# returns list of strings "allfiles"
# containing filenames
def ReadAllMonsters(folder):
    if folder == "":
        allfiles = glob.glob('*.txt')
    else:
        allfiles = []
        filenames = glob.glob(folder + '/*.txt')
        for filename in filenames:
            temp = filename.split("\\")
            allfiles.append(temp[-1])
    
    return allfiles


# Reads monster stats from "filename",
# assuming each stat is a new line,
# preceded by the proper keyword
def ReadMonster(filename, sep, sepWeapon):
    with open(filename, "r") as f:
        index = -1
        weapons = []
        noOfWeapons = 0
		# looping through all lines:
        for line in f:
			# splitting each line into list of values
            values = line.split(sep)
            weapon_i = []
            
			# read stat based on keyword
            if values[0] == 'Name':
                name = values[1][0:-1]
            elif values[0] == 'AC':
                AC = int(values[1])
            elif values[0] == 'Init':
                initiative = int(values[1])
            elif values[0] == 'HP':
                HP = int(values[1])
            elif values[0] == 'Fort':
                fort = int(values[1])
            elif values[0] == 'Refl':
                refl = int(values[1])
            elif values[0] == 'Will':
                will = int(values[1])
            elif values[0] == 'Weapon':
				# keeping track of number of weapons
                noOfWeapons = noOfWeapons + 1
				# splitting each weapon's stats
                weaponValues = values[1].split(sepWeapon)
				# adding stats to the list "weapon_i"
                for data in weaponValues:
                    try:
                        weapon_i.append(int(data))
                    except:
                        weapon_i.append(data)
				# merging all weapon_i into 1 list, "weapons"
                weapons.append(weapon_i)
            
    return name,AC,HP,initiative,fort,refl,will,weapons,noOfWeapons


def Main(directory):
	# This is a GUI class
	# each monster will be a new instance of this
	class MonsterGUI:
		# Initializing GUI by assigning base stats,
		# defining and placing GUI objects
		def __init__(self,name,AC,HP,initiative,fort,refl,will,attacks,noAttacks):
			self.name = name #monster's name
			self.origAC = int(AC) #Armor Class
			self.origHP = int(HP) #Total number of health points
			self.currentHP = int(HP) #Current number of health points
			self.initiative = int(initiative) #Initiative modifier
			self.fort = int(fort) #Fortitude modifier
			self.refl = int(refl) #Reflex modifier
			self.will = int(will) #Will modifier
			self.noAttacks = noAttacks #Number of different attacks it can make
			self.damageHistory = [] #List, keeping track of last 10 damage to the monster
			self.statusEffects = {} #Dictionary of status effects
		
			
			#####################################################
			#	Visual structure of a window, defining frames
			#####################################################
			
			# Defining the main window
			self.root = Tk()
			self.root.wm_title(str(name))
			self.defaultbg = self.root.cget('bg')
			# Defining and placing the Dice Roller Frame
			self.FrameDiceRoller = LabelFrame(self.root)
			self.FrameDiceRoller.pack(side=TOP, padx=10, pady=10)
			# Defining and placing the Status Effects Frame
			self.FrameStatusEffects = LabelFrame(self.root)
			self.FrameStatusEffects.pack(side=LEFT, padx=10, pady=10)
			# Defining and placing the Main Stats Frame
			self.FrameMonster = LabelFrame(self.root)
			self.FrameMonster.pack(side=LEFT)
			# Defining and placing the subframes of the Main Stats Frame
			#  this is where AC,HP,saves are (Stats Frame):
			self.FrameStats = LabelFrame(self.FrameMonster)
			self.FrameStats.pack(side=TOP, padx=10, pady=10)
			#  this is where the Attacks are (Weapons Frame):
			self.FrameAttacks = LabelFrame(self.FrameMonster)
			self.FrameAttacks.pack(side=TOP, padx=10, pady=10)
			#   subframe of Weapons Frame, will contain Misc.Modifiers to attacks:
			self.FrameMiscAttacks = LabelFrame(self.FrameAttacks)
			self.FrameMiscAttacks.pack(side=TOP)
			# Defining and placing the Damage History Frame
			self.FrameDamageHistory = LabelFrame(self.root)
			self.FrameDamageHistory.pack(side=LEFT, padx=10, pady=10)
			#self.FrameRolls = LabelFrame(self.root)
			#self.FrameRolls.pack(side=LEFT)
		

			#####################################################
			#	Defining and placing interactive objects
			#####################################################
			
			########################
			# Dice Roller objects
			########################
			# Entry windows: number of dice, number of sides on dice, +modifier to roll
			self.entryNoOfDice = Entry(self.FrameDiceRoller, width=5)
			self.entryDiceType = Entry(self.FrameDiceRoller, width=5)
			self.entryDiceModifier = Entry(self.FrameDiceRoller, width=5)
			# Static labels
			self.labelDiceRoller1 = Label(self.FrameDiceRoller, text='How many dice:')
			self.labelDiceRoller2 = Label(self.FrameDiceRoller, text='Type (dX):')
			self.labelDiceRoller3 = Label(self.FrameDiceRoller, text='Modifier (+):')
			# Label where result is displayed
			self.labelDiceRollerResult = Label(self.FrameDiceRoller, text='', width=10)
			# Button: roll!
			self.buttonDiceRoller = Button(self.FrameDiceRoller, text="Roll", command=self.RollDice)
			# Placing the objects:
			self.labelDiceRoller1.pack(side=LEFT)
			self.entryNoOfDice.pack(side=LEFT)
			self.labelDiceRoller2.pack(side=LEFT)
			self.entryDiceType.pack(side=LEFT)
			self.labelDiceRoller3.pack(side=LEFT)
			self.entryDiceModifier.pack(side=LEFT)
			self.buttonDiceRoller.pack(side=LEFT)
			self.labelDiceRollerResult.pack(side=LEFT)
			
			########################
			# Status Effects objects
			########################
			# Buttons: apply effect, next turn
			self.buttonUpdateStatus = Button(self.FrameStatusEffects, text='Apply Status Effect:', command=self.ApplyStatusEffect)
			self.buttonTurnStatus = Button(self.FrameStatusEffects, text='TURN', command=self.TurnStatusEffect)
			# Entry windows: status effect name, number of turns it'll last
			self.entryStatusType = Entry(self.FrameStatusEffects, width=10)
			self.entryStatusLength = Entry(self.FrameStatusEffects, width=10)
			# Static labels
			self.labelStatusLength1 = Label(self.FrameStatusEffects, text=' for ')
			self.labelStatusLength2 = Label(self.FrameStatusEffects, text=' rounds')
			self.labelStatusAll = Label(self.FrameStatusEffects, text='Current Status Effects: \n')
			# Placing the objects:
			self.buttonUpdateStatus.pack(side=TOP)
			self.entryStatusType.pack(side=TOP)
			self.labelStatusLength1.pack(side=TOP)
			self.entryStatusLength.pack(side=TOP)
			self.labelStatusLength2.pack(side=TOP)
			self.labelStatusAll.pack(side=TOP)
			self.buttonTurnStatus.pack(side=BOTTOM)
			
			########################
			# Stats (AC,HP)
			########################
			# Static label
			self.labelAC = Label(self.FrameStats, text='AC: ' + str(self.origAC))
			# Dynamic label: will be modified to show current HP
			self.labelHP = Label(self.FrameStats, text='HP: ' + str(self.origHP) + ' / ' + str(self.origHP))
			# Entry window for damage
			self.entryHP = Entry(self.FrameStats, width=5)
			# Button: apply damage!
			self.buttonUpdateHP = Button(self.FrameStats, text="Apply damage:", command=self.UpdateHP)
			# Placing the objects:
			self.labelAC.grid(row=0,column=0)
			self.labelHP.grid(row=1,column=0)
			self.entryHP.grid(row=1,column=2)
			self.buttonUpdateHP.grid(row=1,column=1)
			
			########################
			# Saves (& initiative)
			########################
			# Dynamic labels: will show roll result
			self.labelInitiative = Label(self.FrameStats, text='Initiative: ' + str(self.initiative), width=20)
			self.labelFort = Label(self.FrameStats, text='Fortitude: ' + str(self.fort), width=20)
			self.labelRefl = Label(self.FrameStats, text='Reflex: ' + str(self.refl), width=20)
			self.labelWill = Label(self.FrameStats, text='Will: ' + str(self.will), width=20)
			# Buttons: roll save!
			self.buttonInitiative = Button(self.FrameStats, text="Roll Initiative", command=self.UpdateInitiative)
			self.buttonFort = Button(self.FrameStats, text="Roll Save", command=self.UpdateFort)
			self.buttonRefl = Button(self.FrameStats, text="Roll Save", command=self.UpdateRefl)
			self.buttonWill = Button(self.FrameStats, text="Roll Save", command=self.UpdateWill)
			# Placing the objects:
			self.labelInitiative.grid(row=2,column=0)
			self.buttonInitiative.grid(row=2,column=1)
			self.labelFort.grid(row=3,column=0)
			self.buttonFort.grid(row=3,column=1)
			self.labelRefl.grid(row=4,column=0)
			self.buttonRefl.grid(row=4,column=1)
			self.labelWill.grid(row=5,column=0)
			self.buttonWill.grid(row=5,column=1)

			########################
			# Attack objects
			# (not weapon-specific!)
			########################
			# Static labels
			self.labelAttackMiscModifier = Label(self.FrameMiscAttacks, text='Attack Bonus:')
			self.labelDamageMiscModifier = Label(self.FrameMiscAttacks, text='Damage Bonus:')
			# Entry windows: miscellaneous attack, damage modifier, to be applied to all attacks
			self.entryAttackMiscModifier = Entry(self.FrameMiscAttacks, width=5)
			self.entryDamageMiscModifier = Entry(self.FrameMiscAttacks, width=5)
			# Button: clear misc.modifier entries
			self.buttoneClearMiscModifiers = Button(self.FrameMiscAttacks, text="Clear", command=self.ClearModifiers)
			# Button: roll all weapons at once
			self.buttonUseAllWeapons = Button(self.FrameAttacks, text='Roll all weapons', command=self.UseAllWeapons)
			# Placing the objects:
			self.labelAttackMiscModifier.pack(side=LEFT)
			self.entryAttackMiscModifier.pack(side=LEFT)
			self.labelDamageMiscModifier.pack(side=LEFT)
			self.entryDamageMiscModifier.pack(side=LEFT)
			self.buttoneClearMiscModifiers.pack(side=LEFT)
			self.buttonUseAllWeapons.pack(side=BOTTOM)			
			
			########################
			# Weapon-specific objects:
			# creating new instance of
			# "Weapon" class for each
			########################
			# List to keep track of all instances
			self.weaponList = []
			# Creating all instances
			for i in range(0,self.noAttacks):
				self.weaponTemp = self.Weapon(attacks[i])
				self.weaponTemp.PlaceButtons(self)
				self.weaponList.append(self.weaponTemp)
			
			########################
			# Damage history objects
			########################
			# Dynamic label
			self.labelDamageHistory = Label(self.FrameDamageHistory, text='Damage History: \n')
			# Placing the objects:
			self.labelDamageHistory.pack(side=TOP)
			
			#self.rollsHistoryText = 'Recent Rolls: \n'
			#self.labelRollsHistory = Label(self.FrameRolls, text=self.rollsHistoryText)
			#self.labelRollsHistory.pack(side=TOP)
			
		# End of initialization
		############################################################################################

		
		
		#####################################################
		#	Functions for Dice Roller Frame
		#####################################################

		# Roll the dice
		def RollDice(self):
			try:
				# get modifier from entry window
				modifier = int(self.entryDiceModifier.get())
			# if fail to get it: apply 0 modifier:
			except:
				modifier = 0

			totalRoll = 0 #to keep track of result of dice roll
			try:
				# get number of dice and dice type from entry windows:
				diceType = int(self.entryDiceType.get())
				noOfDice = int(self.entryNoOfDice.get())

				# if input numbers make sense
				if (noOfDice >= 0) & (diceType > 0):
					# roll appropriate number of dice
					for i in range(0,noOfDice):
						dXroll = random.randint(1,diceType)
						totalRoll = totalRoll + dXroll
					# add modifier at end
					totalRoll = totalRoll + modifier
					# display result
					self.labelDiceRollerResult.config(text=str(totalRoll))
			# if can't get info from entry windows: do nothing
			except:
				return
		
		
		
		#####################################################
		#	Functions for Status Effects Frame
		#####################################################
		
		# Progress 1 turn
		def TurnStatusEffect(self):
			# list for status effects that reached their end
			keysToDelete = []
			# loop over all current status effects
			for keys in self.statusEffects:
				# decrease duration for all effects by 1
				self.statusEffects[keys] = self.statusEffects[keys]-1
				# if duration reached 0, flag that effect for removal
				if self.statusEffects[keys] == 0:
					keysToDelete.append(keys)
			
			# loop over effects that need to be deleted
			for el in keysToDelete:
				# delete effect
				del self.statusEffects[el]
					
			# update visual in window
			self.UpdateStatusEffectText()
		
		
		# Update shown list of status effects
		def UpdateStatusEffectText(self):
			# static part of text
			statusText = 'Current Status Effects: \n'
			# loop over status effects and add them to text
			for keys in self.statusEffects:
				statusText = statusText + keys + "\t" + str(self.statusEffects[keys]) + " rounds \n"
			
			# show new text
			self.labelStatusAll.config(text=statusText)
		

		# Add new status effect
		def ApplyStatusEffect(self):
			try:
				# get properties of status effect from entry windows
				typeTemp = self.entryStatusType.get()
				lengthTemp = int(self.entryStatusLength.get())
				self.entryStatusType.delete(0, END)
				self.entryStatusLength.delete(0, END)
				
				# add new status effect to list of effects
				self.statusEffects[typeTemp] = lengthTemp
				# update visual in window
				self.UpdateStatusEffectText()
			# if can't get info from entry windows: do nothing
			finally:
				return

		
		
		#####################################################
		#	Functions for Stats(AC,HP) & Saves Frame
		#		The template for the save functions is the same
		#		and thus they could be merged to one.
		#		I prefer to keep them separate
		#		in case you'll ever want to treat them differently
		#####################################################
		
		# Apply damage to HP
		def UpdateHP(self):
			try:
				# get amount of damage from entry window
				damage = int(self.entryHP.get())
				# if recorded damage history is short, add this
				if len(self.damageHistory) <= 9:
					self.damageHistory.append(damage)
				# else: delete first record in damage history, then shift and add this one to the end
				else:
					self.ShiftDamageHistory(damage)
				
				# update visual in Damage History frame
				damageHistoryText = 'Damage History:'
				for dam in self.damageHistory:
					damageHistoryText = damageHistoryText + '\n' + str(dam)
				self.labelDamageHistory.config(text=damageHistoryText)
				
				# apply damage to HP
				self.currentHP = self.currentHP - damage
				# only ever heal up to original HP:
				if self.currentHP > self.origHP:
					self.currentHP = self.origHP

				# color code if monster is dead:
				if self.currentHP <= 0:
					color = "red"
				else:
					color = "black"

				# update visual HP
				self.labelHP.config(text='HP: ' + str(self.currentHP) + ' / ' + str(self.origHP), foreground = color)
				
				# clear entry window
				self.entryHP.delete(0, END)
			# if couldn't get damage from entry window: do nothing
			except:
				return
					
		
		# Roll initiative
		def UpdateInitiative(self):
			# roll a d20
			d20roll = random.randint(1,20)
			#self.rollsHistoryText = self.rollsHistoryText + str(d20roll) + '\n'
			#self.labelRollsHistory.config(text=self.rollsHistoryText)

			# color code critical
			if d20roll == 1:
				color = "red"
			elif d20roll == 20:
				color = "green"
			else:
				color = "black"
			# update visual
			self.labelInitiative.config(text='Initiative: ' + str(self.initiative) + ' + ' + str(d20roll) + ' = ' + str(self.initiative+d20roll), foreground = color)

		
		# Roll Fortitude save
		def UpdateFort(self):
			# roll a d20
			d20roll = random.randint(1,20)
			#self.rollsHistoryText = self.rollsHistoryText + str(d20roll) + '\n'
			#self.labelRollsHistory.config(text=self.rollsHistoryText)

			# color code criticals
			if d20roll == 1:
				color = "red"
			elif d20roll == 20:
				color = "green"
			else:
				color = "black"
			# update visual
			self.labelFort.config(text='Fortitude: ' + str(self.fort) + ' + ' + str(d20roll) + ' = ' + str(self.fort+d20roll), foreground = color)


		# Roll Reflex save
		def UpdateRefl(self):
			# roll d20
			d20roll = random.randint(1,20)
			#self.rollsHistoryText = self.rollsHistoryText + str(d20roll) + '\n'
			#self.labelRollsHistory.config(text=self.rollsHistoryText)

			# color code criticals
			if d20roll == 1:
				color = "red"
			elif d20roll == 20:
				color = "green"
			else:
				color = "black"
			# update visual
			self.labelRefl.config(text='Reflex: ' + str(self.refl) + ' + ' + str(d20roll) + ' = ' + str(self.refl+d20roll), foreground = color)


		# Roll Will save
		def UpdateWill(self):
			# roll a d20
			d20roll = random.randint(1,20)
			#self.rollsHistoryText = self.rollsHistoryText + str(d20roll) + '\n'
			#self.labelRollsHistory.config(text=self.rollsHistoryText)

			# color code criticals
			if d20roll == 1:
				color = "red"
			elif d20roll == 20:
				color = "green"
			else:
				color = "black"
			# update visual
			self.labelWill.config(text='Will: ' + str(self.will) + ' + ' + str(d20roll) + ' = ' + str(self.will+d20roll), foreground = color)


		
		#####################################################
		#	Functions for Weapons Frame
		#####################################################	

		# Use all weapons at once
		def UseAllWeapons(self):
			# loop over all weapons, and invoke their "UseWeapon" method one by one
			for weapon in self.weaponList:
				weapon.UseWeapon(self)
		
		
		# Clear entries of attack and damage modifiers
		def ClearModifiers(self):
			self.entryDamageMiscModifier.delete(0, END)
			self.entryAttackMiscModifier.delete(0, END)

			

		#####################################################
		#	Functions for Damage History Frame
		#####################################################	
		
		# Erase oldest recorded damage, then append new damage to end of list
		def ShiftDamageHistory(self,newDamage):
			# first shift all recorded damage left
			for i in range(0,len(self.damageHistory)-1):
				self.damageHistory[i] = self.damageHistory[i+1]
				
			# then append new damage value to the end
			self.damageHistory[-1] = newDamage
			
		
		
		#####################################################
		#	"Weapon" class
		#		includes methods to place objects for each weapon
		#		and to use each weapon
		#####################################################
		
		class Weapon:
			# initialize: assign weapon properties
			def __init__(self,weapon):
				self.type = weapon[0] #weapon name
				self.attackModifier = int(weapon[1]) #attack modifier
				self.noOfDice = int(weapon[2]) #number of dice in damage roll
				self.diceType = int(weapon[3]) #number of sides of dice in damage roll
				self.damage = int(weapon[4]) #damage modifier
				self.critThreshold = int(weapon[5]) #lowest attack roll that is considered critical
				self.critFactor = int(weapon[6]) #multiplicative factor of a critical

			# Placing labels and buttons
			# 	"parent" is the instance of the MonsterGUI class in this case, that is where we want to place the objects
			def PlaceButtons(self,parent):
				# Define separate frame for this weapon, place it
				self.FrameWeapon = LabelFrame(parent.FrameAttacks)
				self.FrameWeapon.pack(side=BOTTOM)
				# Dynamic labels: attack roll, damage roll
				self.labelAttackRoll = Label(self.FrameWeapon, text=self.type + ': ' + str(self.attackModifier), width=20)
				self.labelAttackDamage = Label(self.FrameWeapon, text= 'Damage: ' + str(self.noOfDice) + 'd' + str(self.diceType) + '+' + str(self.damage), width=35)
				# Buttin: use weapon!
				self.buttonAttack = Button(self.FrameWeapon, text="Use", command=lambda: self.UseWeapon(parent))
				# Placing the objects:
				self.labelAttackRoll.pack(side=LEFT)
				self.labelAttackDamage.pack(side=LEFT)
				self.buttonAttack.pack(side=LEFT)

			# Using this weapon
			#	"parent" is the instance of the MonsterGUI class in this case, that is where we want to place the objects
			def UseWeapon(self,parent):
				# roll d20 for attack
				d20roll = random.randint(1,20)
				#parent.rollsHistoryText = parent.rollsHistoryText + str(d20roll) + '\n'
				#parent.labelRollsHistory.config(text=parent.rollsHistoryText)

				# get misc. attack and damage modifiers, if applicable
				try:
					attackMiscModifier = int(parent.entryAttackMiscModifier.get())
				except:
					attackMiscModifier = 0
				try:
					damageMiscModifier = int(parent.entryDamageMiscModifier.get())
				except:
					damageMiscModifier = 0

				totalRoll = 0 #keeping track of damage
				# rolling appropriate number of dice:
				for i in range(0,self.noOfDice):
					dXroll = random.randint(1,self.diceType)
					#parent.rollsHistoryText = parent.rollsHistoryText + str(d20roll) + '\n'
					#parent.labelRollsHistory.config(text=parent.rollsHistoryText)

					totalRoll = totalRoll + dXroll

				# adding misc. damage modifier
				totalRoll = totalRoll + self.damage + damageMiscModifier
				# updating text for damage
				if damageMiscModifier != 0:
					damageText = 'Damage: ' + str(self.noOfDice) + 'd' + str(self.diceType) + '+' + str(self.damage) + '+' + str(damageMiscModifier)
				else:
					damageText = 'Damage: ' + str(self.noOfDice) + 'd' + str(self.diceType) + '+' + str(self.damage)
				# updating visual (label) for damage
				if d20roll >= self.critThreshold:
					# it's a critical hit, apply multiplicative factor:
					critRoll = totalRoll*self.critFactor
					# color code based on which kind of critical
					if d20roll == 20:
						color = "green"
					else:
						color = "blue"
					# update visual
					self.labelAttackDamage.config(text=damageText + ' = ' + str(totalRoll) + ' Crit. damage: ' + str(critRoll))
				else: #not a critical hit
					# update visual
					self.labelAttackDamage.config(text=damageText + ' = ' + str(totalRoll))
					# color code if it's a critical fail:
					if d20roll == 1:
						color = "red"
					else:
						color = "black"

				# updating text for attack roll
				totalAttack = self.attackModifier+d20roll+attackMiscModifier
				attackText = self.type + ': ' + str(self.attackModifier) + ' + ' + str(d20roll)
				# updating visual (label) for attack roll:
				if attackMiscModifier != 0:
					self.labelAttackRoll.config(text=attackText + ' + ' + str(attackMiscModifier) + ' = ' + str(totalAttack), foreground = color)
				else:
					self.labelAttackRoll.config(text=attackText + ' = ' + str(totalAttack), foreground = color)


					
	# scrape folder "directory", return list of file names "allfiles"
	allfiles = ReadAllMonsters(directory)
	if directory == "":
		readText = ""
	else:
		readText = directory + "/"
	# create empty list of GUI's
	GUI = []
	# loop over list of filenames
	for i in range(0,len(allfiles)):
		# get stats for each monster
		name,AC,HP,initiative,fort,refl,will,weapons,noOfWeapons = ReadMonster(readText + allfiles[i], "\t", ",")

		# launch separate GUI for each monster
		GUI_temp = MonsterGUI(name,AC,HP,initiative,fort,refl,will,weapons,noOfWeapons)
		# collect all GUI's into a list
		GUI.append(GUI_temp)


	# close all GUI's
	for i in range(0,len(allfiles)):
		GUI[i].root.mainloop()

		
# if there is a command line argument, use that for directory to scrape	
try:		
	directory = sys.argv[1]
# else: scrape current directory
except:
	directory = ""
Main(directory)


