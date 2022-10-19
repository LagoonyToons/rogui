#a gui program for creating cards for rogue genesia's mod easy cards
import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk
import json
import os

#constant lists for dropdown menus/json generation
RARITIES = ["Tainted", "Normal", "Uncommon", "Rare", "Epic", "Heroic", "Ascended", "Evolution"]
TAGS = ["Order", "Critical", "Defense", "Body", "Might", "Evolution"]
NAMELOCALIZATION = ["en", "fr", "zh-Hans", "ko", "pt","ja","de","es","ru","tr","da"]
MODIFIERTYPE = ["Additional", "Multiplier", "Compound"]
STATS = ["MaxHealth","HealthRegen","Defence","DamageMitigation","XPMultiplier","PickUpDistance","AdditionalProjectile","ProjectilePiercing","ProjectileLifeTime","ProjectileSpeed","ProjectileSize","AreaSize","KnockBack","MoveSpeed","AttackCoolDown","AttackDelay","Damage","CriticalChance","CriticalMultiplier","DashSpeed","DashDuration","DashDelay","DashCoolDown","DashCharge","DashChargePerCoolDown","GoldMultiplier","SoulCoinMultiplier","DefencePiercing","Corruption"]
ALLOCATED_MODIFIER_SLOTS = 10 #max number of modifiers is 10 (because I'm lazy)
ALLOCATED_LOCALIZATION_SLOTS=len(NAMELOCALIZATION) #still lazy

class CardMaker:
    def __init__(self, master):
        #gui setup
        self.master = master
        master.title("Card Maker")
        master.geometry("800x700")
        master.resizable(True, True)

        #data
        self.card = [] #potentially load an entire folder of cards and move between them with a dropdown menu, but for now just one card
        self.modifier_row_start = 6
        self.modifier_row_end = self.modifier_row_start + ALLOCATED_MODIFIER_SLOTS
        self.modifier_row_next = self.modifier_row_start
        self.modifiers = []

        self.localization_row_start = self.modifier_row_end + 2
        self.localization_row_end = self.localization_row_start + ALLOCATED_LOCALIZATION_SLOTS
        self.localization_row_next = self.localization_row_start
        self.localizations = []

        #add save and load drop down menu
        self.menubar = tkinter.Menu(master)
        self.filemenu = tkinter.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Load", command=self.load)
        self.filemenu.add_command(label="Save", command=self.save)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=master.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        master.config(menu=self.menubar)

        #widget for getting card name
        self.name_label = tkinter.Label(master, text="Card Name")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tkinter.Entry(master)
        self.name_entry.grid(row=0, column=1)

        #widget for getting card image path and button to open file dialog
        self.path_label = tkinter.Label(master, text="Image Path")
        self.path_label.grid(row=1, column=0)
        self.path_entry = tkinter.Entry(master)
        self.path_entry.grid(row=1, column=1)
        self.path_button = tkinter.Button(master, text="Browse", command=self.browse_image)
        self.path_button.grid(row=1, column=2)

        #widget for previewing card image, leave it blank for now
        #place it in the top right of the window without using grid
        self.image_label = tkinter.Label(master, text="Image Preview")
        self.image_label.place(relx=1, rely=1, anchor=tkinter.SE)

        #widget for getting card rarity, dropdown menu using RARITIES list
        self.rarity_label = tkinter.Label(master, text="Rarity")
        self.rarity_label.grid(row=2, column=0)
        self.rarity_var = tkinter.StringVar(master)
        self.rarity_var.set(RARITIES[0])
        self.rarity_menu = tkinter.OptionMenu(master, self.rarity_var, *RARITIES)
        self.rarity_menu.grid(row=2, column=1)

        #widgets for getting card tags, multiple checkboxes using TAGS list
        self.tag_label = tkinter.Label(master, text="Tags")
        self.tag_label.grid(row=3, column=0)
        self.tag_var = []
        self.tag_check = []
        for i in range(len(TAGS)):
            self.tag_var.append(tkinter.IntVar())
            self.tag_check.append(tkinter.Checkbutton(master, text=TAGS[i], variable=self.tag_var[i]))
            self.tag_check[i].grid(row=3, column=i+1)

        #Widget for getting drop weight and levelupweight
        self.weight_label = tkinter.Label(master, text="Drop Weight")
        self.weight_label.grid(row=4, column=0)
        self.weight_entry = tkinter.Entry(master)
        self.weight_entry.grid(row=4, column=1)
        self.levelupweight_label = tkinter.Label(master, text="Level Up Weight")
        self.levelupweight_label.grid(row=4, column=2)
        self.levelupweight_entry = tkinter.Entry(master)
        self.levelupweight_entry.grid(row=4, column=3)

        #widget for getting maxlevel
        self.maxlevel_label = tkinter.Label(master, text="Max Level")
        self.maxlevel_label.grid(row=5, column=0)
        self.maxlevel_entry = tkinter.Entry(master)
        self.maxlevel_entry.grid(row=5, column=1)

        #widget for getting modifiers
        self.modifiers = []
        self.create_modifier()

        #widget button for creating a new modifier or removing the last one
        self.modifier_button = tkinter.Button(master, text="Add Modifier", command=self.create_modifier)
        self.modifier_button.grid(row=self.modifier_row_end+1, column=0)
        self.modifier_remove_button = tkinter.Button(master, text="Remove Modifier", command=self.remove_modifier)
        self.modifier_remove_button.grid(row=self.modifier_row_end+1, column=1)

        #widget for card localization
        self.localizations = []
        self.create_localization()

        #widget button for creating a new localization or removing the last one
        self.localization_button = tkinter.Button(master, text="Add Localization", command=self.create_localization)
        self.localization_button.grid(row=self.localization_row_end+1, column=0)
        self.localization_remove_button = tkinter.Button(master, text="Remove Localization", command=self.remove_localization)
        self.localization_remove_button.grid(row=self.localization_row_end+1, column=1)

    def create_modifier(self):
        #widget for getting modifier value, type(MODIFERTYPE), and stat(STATS)
        self.modifiers.append([])
        self.modifiers[-1].append(tkinter.Entry(self.master))
        self.modifiers[-1][0].grid(row=self.modifier_row_next, column=0)
        self.modifiers[-1].append(tkinter.StringVar(self.master))
        self.modifiers[-1][1].set(MODIFIERTYPE[0])
        self.modifiers[-1].append(tkinter.OptionMenu(self.master, self.modifiers[-1][1], *MODIFIERTYPE))
        self.modifiers[-1][2].grid(row=self.modifier_row_next, column=1)
        self.modifiers[-1].append(tkinter.StringVar(self.master))
        self.modifiers[-1][3].set(STATS[0])
        self.modifiers[-1].append(tkinter.OptionMenu(self.master, self.modifiers[-1][3], *STATS))
        self.modifiers[-1][4].grid(row=self.modifier_row_next, column=2)
        self.modifier_row_next += 1

    def remove_modifier(self):
        if len(self.modifiers) > 0:
            #remove the last modifier
            #remove value
            self.modifiers[-1][0].grid_forget()
            #remove type
            self.modifiers[-1][2].grid_forget()
            #remove stat
            self.modifiers[-1][4].grid_forget()

            #remove the modifier from the list
            self.modifiers.pop()
        
    def create_localization(self):
        #widget for getting localization name(NAMELOCALIZATION) and description
        self.localizations.append([])
        self.localizations[-1].append(tkinter.StringVar(self.master))
        self.localizations[-1][0].set(NAMELOCALIZATION[0])
        self.localizations[-1].append(tkinter.OptionMenu(self.master, self.localizations[-1][0], *NAMELOCALIZATION))
        self.localizations[-1][1].grid(row=self.localization_row_next, column=0)
        self.localizations[-1].append(tkinter.Entry(self.master))
        self.localizations[-1][2].grid(row=self.localization_row_next, column=1)

        self.localization_row_next += 1

    def remove_localization(self):
        if len(self.localizations) > 0:
            #remove the last localization
            #remove name
            self.localizations[-1][1].grid_forget()
            #remove description
            self.localizations[-1][2].grid_forget()

            #remove the localization from the list
            self.localizations.pop()
    def save(self):
        #get card name
        name = self.name_entry.get()

        #get card image path
        path_entry = self.path_entry.get()

        #get card rarity
        rarity = self.rarity_var.get()

        #get card tags
        tags = []
        for i in range(len(TAGS)):
            if self.tag_var[i].get() == 1:
                tags.append(TAGS[i])

        #get card drop weight
        weight = float(self.weight_entry.get())

        #get card level up weight
        levelupweight = float(self.levelupweight_entry.get())

        #get card max level
        maxlevel = int(self.maxlevel_entry.get())

        #get card modifiers
        #"ModifierValue": "ModifierType": "Stat":
        modifiers = []
        for i in range(len(self.modifiers)):
            modifiers.append({"ModifierValue": float(self.modifiers[i][0].get()), "ModifierType": self.modifiers[i][1].get(), "Stat": self.modifiers[i][3].get()})

        #get card localizations
        #language, name
        localizations = {}
        for i in range(len(self.localizations)):
            localizations[self.localizations[i][0].get()] = self.localizations[i][2].get()


        #save card
        card = Card()
        card.name = name
        card.path = path_entry
        card.rarity = rarity
        card.tags = tags
        card.dropweight = weight
        card.levelupweight = levelupweight
        card.maxlevel = maxlevel
        card.modifiers = modifiers
        card.namelocalization = localizations

        save_card(card)

    def load(self): #fill in the widgets with the card data
        #open file dialog
        filename = filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (("json files","*.json"),("all files","*.*")))
        if filename != "":
            self.card = load_card(filename)
        #get card name
        self.name_entry.delete(0, tkinter.END)
        self.name_entry.insert(0, self.card.name)

        #get card image path
        self.path_entry.delete(0, tkinter.END)
        self.path_entry.insert(0, self.card.path)

        #get card rarity
        self.rarity_var.set(self.card.rarity)

        #get card tags
        for i in range(len(TAGS)):
            self.tag_var[i].set(0)
        for i in range(len(self.card.tags)):
            self.tag_var[TAGS.index(self.card.tags[i])].set(1)

        #get card drop weight
        self.weight_entry.delete(0, tkinter.END)
        self.weight_entry.insert(0, self.card.dropweight)

        #get card level up weight
        self.levelupweight_entry.delete(0, tkinter.END)
        self.levelupweight_entry.insert(0, self.card.levelupweight)

        #get card max level
        self.maxlevel_entry.delete(0, tkinter.END)
        self.maxlevel_entry.insert(0, self.card.maxlevel)

        #get card modifiers
        #"ModifierValue": "ModifierType": "Stat":
        for i in range(len(self.modifiers)):
            self.remove_modifier()
        for i in range(len(self.card.modifiers)):
            self.create_modifier()
            self.modifiers[-1][0].delete(0, tkinter.END)
            self.modifiers[-1][0].insert(0, self.card.modifiers[i]["ModifierValue"])
            self.modifiers[-1][1].set(self.card.modifiers[i]["ModifierType"])
            self.modifiers[-1][3].set(self.card.modifiers[i]["Stat"])

        #get card localizations
        #language, name
        for i in range(len(self.localizations)):
            try:
                self.remove_localization()
            except:
                pass
        if len(self.card.namelocalization) > 0:
            for i in range(len(self.card.namelocalization)):
                self.create_localization()
                self.localizations[-1][0].set(list(self.card.namelocalization.keys())[i])
                self.localizations[-1][2].delete(0, tkinter.END)
                self.localizations[-1][2].insert(0, list(self.card.namelocalization.values())[i])


    def browse_image(self):
        #open file dialog and get image
        filename = filedialog.askopenfilename(initialdir = "./assets/",title = "Select file",filetypes = (("png files","*.png"),("all files","*.*")))
        if filename != "":
            self.image = Image.open(filename)
            self.image = self.image.resize((256, 256), Image.ANTIALIAS)
            self.image = ImageTk.PhotoImage(self.image)
            self.image_label.configure(image=self.image)
            #convert path to relative path
            self.image_path = filename[filename.find("assets"):]
            #remove "assets/" from the path
            self.image_path = self.image_path[7:]
            print(self.image_path)
            #fill in the image path
            self.path_entry.delete(0, tkinter.END)
            self.path_entry.insert(0, self.image_path)

class Card:
    def __init__(self):
        self.name = "" #string
        self.path = "" #string
        self.rarity = "" #string
        self.tags = [] #list of strings
        self.dropweight = 0 #float
        self.levelupweight = 0 #float
        self.maxlevel = 0 #int
        
        self.modifiers = [] #list of dictionaries (3 values: stat, type, value)
        self.namelocalization = {} #dictionary of strings to strings (language to name)
    
    def print_info(self):
        print(self.name)
        print(self.path)
        print(self.rarity)
        print(self.tags)
        print(self.dropweight)
        print(self.levelupweight)
        print(self.maxlevel)
        print(self.modifiers)
        print(self.namelocalization)

def load_card(filename): #loads a SINGLE card from a json file
    card = Card()
    f = open(filename, "r")
    f = json.load(f)

    data = f["Stats"][0] #remove top level of json

    card.name = data["Name"]
    card.path = data["TexturePath"]
    card.rarity = data["Rarity"]
    card.tags = data["Tags"]
    card.dropweight = data["DropWeight"]
    card.levelupweight = data["LevelUpWeight"]
    card.maxlevel = data["MaxLevel"]
    card.modifiers = data["Modifiers"]
    card.namelocalization = data["NameLocalization"]

    return card

def save_card(card, output_file=""): #Saves a SINGLE card into a json file
    save_path = "data/"
    if output_file == "":
        output_file = card.name + ".json"

    if card.path == "":
        card.path = "placeholder.png"
    
    data = {}
    data["Stats"] = []
    data["Stats"].append({
        "Name": card.name,
        "TexturePath": card.path,
        "Rarity": card.rarity,
        "Tags": card.tags,
        "DropWeight": card.dropweight,
        "LevelUpWeight": card.levelupweight,
        "MaxLevel": card.maxlevel,
        "Modifiers": card.modifiers,
        "NameLocalization": card.namelocalization
    })
    # print(card.namelocalization)

    with open(save_path + output_file, 'w') as outfile:
        json.dump(data, outfile, indent=4)
    

if __name__ == '__main__':
    root = tkinter.Tk()
    my_gui = CardMaker(root)
    root.mainloop()
        