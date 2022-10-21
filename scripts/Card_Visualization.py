from textwrap import wrap
import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk
from scripts import constants
globals().update(constants.__dict__)


class Card_Visualization:
    ### take a card and display it as it would be in the game (close to the actual game)
    def __init__(self, card, master):
        self.card = card
        self.master = master

        self.get_stats() #reinitialize the stats

    def get_stats(self):
        #arbitrary values for visualizing the stat changes
        #corresponds to the labels in STATS
        #
        self.maxhealth = 100
        self.healthregen = 1
        self.defence = 1
        self.damagemitigation = 1
        self.xpmultiplier = 1
        self.pickupdistance = 1
        self.additionalprojectile = 1
        self.projectilepiercing = 1
        self.projectilelifetime = 1
        self.projectilespeed = 1
        self.projectilesize = 1
        self.areasize = 1
        self.knockback = 1
        self.movespeed = 1
        self.attackcooldown = 1
        self.attackdelay = 1
        self.damage = 1
        self.criticalchance = .05
        self.criticalmultiplier = 1
        self.dashspeed = 1
        self.dashduration = 1
        self.dashdelay = 3
        self.dashcooldown = 1
        self.dashcharge = 3
        self.dashchargepercooldown = 1
        self.goldmultiplier = 1
        self.soulcoinmultiplier = 1
        self.defencepiercing = 1
        self.corruption = 1

        self.stats = {
            "MaxHealth": self.maxhealth,
            "HealthRegen": self.healthregen,
            "Defence": self.defence,
            "DamageMitigation": self.damagemitigation,
            "XPMultiplier": self.xpmultiplier,
            "PickupDistance": self.pickupdistance,
            "AdditionalProjectile": self.additionalprojectile,
            "ProjectilePiercing": self.projectilepiercing,
            "ProjectileLifetime": self.projectilelifetime,
            "ProjectileSpeed": self.projectilespeed,
            "ProjectileSize": self.projectilesize,
            "AreaSize": self.areasize,
            "Knockback": self.knockback,
            "MoveSpeed": self.movespeed,
            "AttackCooldown": self.attackcooldown,
            "AttackDelay": self.attackdelay,
            "Damage": self.damage,
            "CriticalChance": self.criticalchance,
            "CriticalMultiplier": self.criticalmultiplier,
            "DashSpeed": self.dashspeed,
            "DashDuration": self.dashduration,
            "DashDelay": self.dashdelay,
            "DashCooldown": self.dashcooldown,
            "DashCharge": self.dashcharge,
            "DashChargePerCooldown": self.dashchargepercooldown,
            "GoldMultiplier": self.goldmultiplier,
            "SoulCoinMultiplier": self.soulcoinmultiplier,
            "DefencePiercing": self.defencepiercing,
            "Corruption": self.corruption
        }
        self.statConstants = {
            "MaxHealth": self.maxhealth,
            "HealthRegen": self.healthregen,
            "Defence": self.defence,
            "DamageMitigation": self.damagemitigation,
            "XPMultiplier": self.xpmultiplier,
            "PickupDistance": self.pickupdistance,
            "AdditionalProjectile": self.additionalprojectile,
            "ProjectilePiercing": self.projectilepiercing,
            "ProjectileLifetime": self.projectilelifetime,
            "ProjectileSpeed": self.projectilespeed,
            "ProjectileSize": self.projectilesize,
            "AreaSize": self.areasize,
            "Knockback": self.knockback,
            "MoveSpeed": self.movespeed,
            "AttackCooldown": self.attackcooldown,
            "AttackDelay": self.attackdelay,
            "Damage": self.damage,
            "CriticalChance": self.criticalchance,
            "CriticalMultiplier": self.criticalmultiplier,
            "DashSpeed": self.dashspeed,
            "DashDuration": self.dashduration,
            "DashDelay": self.dashdelay,
            "DashCooldown": self.dashcooldown,
            "DashCharge": self.dashcharge,
            "DashChargePerCooldown": self.dashchargepercooldown,
            "GoldMultiplier": self.goldmultiplier,
            "SoulCoinMultiplier": self.soulcoinmultiplier,
            "DefencePiercing": self.defencepiercing,
            "Corruption": self.corruption
        }
        self.statMultipliers = {
            "MaxHealth": 1,
            "HealthRegen": 1,
            "Defence": 1,
            "DamageMitigation": 1,
            "XPMultiplier": 1,
            "PickupDistance": 1,
            "AdditionalProjectile": 1,
            "ProjectilePiercing": 1,
            "ProjectileLifetime": 1,
            "ProjectileSpeed": 1,
            "ProjectileSize": 1,
            "AreaSize": 1,
            "Knockback": 1,
            "MoveSpeed": 1,
            "AttackCooldown": 1,
            "AttackDelay": 1,
            "Damage": 1,
            "CriticalChance": 1,
            "CriticalMultiplier": 1,
            "DashSpeed": 1,
            "DashDuration": 1,
            "DashDelay": 1,
            "DashCooldown": 1,
            "DashCharge": 1,
            "DashChargePerCooldown": 1,
            "GoldMultiplier": 1,
            "SoulCoinMultiplier": 1,
            "DefencePiercing": 1,
            "Corruption": 1
        }
        self.statPrintNames = {
            "MaxHealth": "Max Health",
            "HealthRegen": "Health Regen",
            "Defence": "Defence",
            "DamageMitigation": "Damage Mitigation",
            "XPMultiplier": "XP Multiplier",
            "PickupDistance": "Pickup Distance",
            "AdditionalProjectile": "Additional Projectile",
            "ProjectilePiercing": "Projectile Piercing",
            "ProjectileLifetime": "Projectile Lifetime",
            "ProjectileSpeed": "Projectile Speed",
            "ProjectileSize": "Projectile Size",
            "AreaSize": "Area Size",
            "Knockback": "Knockback",
            "MoveSpeed": "Move Speed",
            "AttackCooldown": "Attack Cooldown",
            "AttackDelay": "Attack Delay",
            "Damage": "Damage",
            "CriticalChance": "Critical Chance",
            "CriticalMultiplier": "Critical Multiplier",
            "DashSpeed": "Dash Speed",
            "DashDuration": "Dash Duration",
            "DashDelay": "Dash Delay",
            "DashCooldown": "Dash Cooldown",
            "DashCharge": "Dash Charge",
            "DashChargePerCooldown": "Dash Charge Per Cooldown",
            "GoldMultiplier": "Gold Multiplier",
            "SoulCoinMultiplier": "Soul Coin Multiplier",
            "DefencePiercing": "Defence Piercing",
            "Corruption": "Corruption"
        }
               
    def get_modifier_text(self):
        modifiers = [] #list of list of strings
        self.max_stats = [[], [], []] 
        for i in range(self.card.maxlevel+2): #you can overlevel by 2
            modifiers.append([])
            for j in range(len(self.card.modifiers)): #for each modifier
                value = self.card.modifiers[j]["ModifierValue"]
                stat = self.card.modifiers[j]["Stat"]
                type = self.card.modifiers[j]["ModifierType"]
                if type == "Additional": # update stats, append new value
                    self.stats[stat] += value
                    # modifiers[i].append(self.stats[stat] * self.statMultipliers[stat])
                    modifiers[i].append(str(self.stats[stat] - value) + " -> " + str(self.stats[stat]) + " " +  self.statPrintNames[stat] + " (+" + str(value) + ")")
                    if i > self.card.maxlevel-2:
                        output = (str(self.statConstants[stat]) + " -> " + str(self.stats[stat]) + " " +  self.statPrintNames[stat] + " (+" + str(value * (i+1)) + ")")
                        self.max_stats[i-(self.card.maxlevel-1)].append(output)  #literally just addition

                elif type == "Multiplier": #update statMultipliers
                    level = i+1
                    temp = 1 
                    new_val = value - 1
                    #remove previous multiplier boosts
                    for k in range(level):
                        temp += new_val

                    if level > 1 and temp-new_val != 0:
                        self.statMultipliers[stat] /=  (temp - new_val) #remove previous multiplier
                    elif temp-new_val == 0:
                        self.statMultipliers[stat] = 0
                    
                    curr = self.statMultipliers[stat] * (temp - new_val) * self.stats[stat] #true current value, before new multiplier stack
                    
                    self.statMultipliers[stat] *= temp #add new multiplier, one multiplier higher than current level
                    #construct the string "current -> new stat (*value%)"
                    # modifiers[i].append(self.stats[stat] * self.statMultipliers[stat])
                    modifiers[i].append(str(curr) + " -> " + str(self.stats[stat] * self.statMultipliers[stat]) + " " + self.statPrintNames[stat] + " (*" + str(value) + ")")
                    if i > self.card.maxlevel-2:
                        output = (str(self.stats[stat]) + " -> " + str(self.stats[stat] * temp) + " " + self.statPrintNames[stat] + " (*" + str(temp) + ")")
                        self.max_stats[i-(self.card.maxlevel-1)].append(output) #additive multipliers

                elif type == "Compound": #update statMultipliers
                    self.statMultipliers[stat] *= value
                    #construct the string "current -> new stat (*value%)"
                    modifiers[i].append(str(self.stats[stat]*self.statMultipliers[stat]/value) + " -> " + str(self.stats[stat] * self.statMultipliers[stat]) + " " +  self.statPrintNames[stat] + " (*" + str(value) + ")")
                    if i > self.card.maxlevel-2:
                        output = (str(self.stats[stat]) + " -> " + str(self.stats[stat] * self.statMultipliers[stat]) + " " +  self.statPrintNames[stat] + " (*" + str(value ** (i+1)) + ")")
                        self.max_stats[i-(self.card.maxlevel-1)].append(output) #compound is exponential
                    # modifiers[i].append(self.statMultipliers[stat]*self.stats[stat])

        return modifiers

    def set_card(self, card):
        self.card = card

    def draw(self, max_stats_ready):
        ##return a tkinter canvas with the card drawn on it, ready to be displayed in the main window
        #create canvas
        canvas = tkinter.Canvas(self.master, width=250, height=450, bg="black")

        #draw the card image on the top left of the canvas
        image = Image.open("assets/" + self.card.path)
        image = image.resize((125, 125))
        image = ImageTk.PhotoImage(image)
        canvas.create_image(60, 15, image=image, anchor="nw")
        #show the image
        canvas.image = image
        #give the canvas a border whose color is the corresponding rarity color
        canvas.create_rectangle(5, 5, 248, 448, outline=RARITY_COLORS[self.card.rarity], width=7)

        #draw the card name under the image
        canvas.create_text(25, 140, text=self.card.name, anchor="nw", fill="white", width=225, justify="center")

        if max_stats_ready:
            #draw the max stats for each level
            # for i in range(len(self.max_stats)):
            #     overlevel = ""
            #     if i > 0:
            #         overlevel = " (+" + str(i) + ")"
            #     t = "Level " + str(self.card.maxlevel) + overlevel + ": " + str(self.max_stats[i])
            x = ""
            for i in range(len(self.max_stats)):
                overlevel = ""
                if i > 0:
                    overlevel = " (+" + str(i) + ")"
                x +=  str(self.card.maxlevel) + overlevel + ": "
                for j in range(len(self.max_stats[i])):
                    if type(self.max_stats[i][j]) == str:
                        x += self.max_stats[i][j] + "\n"
                    else:
                        x += str(self.max_stats[i][j]) + "\n"
                x += "\n"

            canvas.create_text(25, 160, text=x, anchor="nw", fill="white", width=225, justify="left")

        #show the canvas on the bottom left of the main window
        canvas.grid(row=999, column=0, columnspan=2, sticky="nsew")

        return canvas